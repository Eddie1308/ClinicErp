import frappe
from frappe.model.document import Document
from frappe.utils import nowdate, add_days, flt, getdate


class ClinicAppointment(Document):

    def validate(self):
        self.calculate_totals()
        self.validate_installments()
        self.check_doctor_availability()

    def calculate_totals(self):
        """Calculate total, discount, net, and balance"""
        total = 0
        if self.services_table:
            for service in self.services_table:
                total += flt(service.amount)

        self.total_amount = total
        self.discount_amount = flt(total) * flt(self.discount_percent) / 100
        self.net_amount = flt(total) - flt(self.discount_amount)
        self.balance_amount = flt(self.net_amount) - flt(self.paid_amount)

    def validate_installments(self):
        """Validate installments sum equals balance"""
        if self.payment_method == "أقساط" and self.installments_table:
            total_installments = sum(flt(i.amount) for i in self.installments_table)
            if abs(total_installments - flt(self.balance_amount)) > 1:
                frappe.throw(
                    f"مجموع الأقساط ({total_installments}) لا يساوي الرصيد المتبقي ({self.balance_amount})"
                )
            # Number the installments
            for idx, inst in enumerate(self.installments_table, 1):
                inst.installment_number = idx

    def check_doctor_availability(self):
        """Check if doctor has another appointment at the same time"""
        if self.doctor and self.appointment_date and self.appointment_time:
            conflict = frappe.db.sql("""
                SELECT name FROM `tabClinic Appointment`
                WHERE doctor = %s
                AND appointment_date = %s
                AND appointment_time = %s
                AND name != %s
                AND status NOT IN ('ملغي', 'غائب')
                AND docstatus != 2
            """, (self.doctor, self.appointment_date, self.appointment_time, self.name or ""))
            if conflict:
                frappe.throw(f"الدكتور لديه موعد آخر في نفس الوقت: {conflict[0][0]}")

    def on_submit(self):
        """Auto-create Sales Invoice on submit"""
        self.create_sales_invoice()

    def on_cancel(self):
        """Cancel linked invoice if exists"""
        if self.sales_invoice:
            inv = frappe.get_doc("Sales Invoice", self.sales_invoice)
            if inv.docstatus == 1:
                inv.cancel()

    def create_sales_invoice(self):
        """Create Sales Invoice linked to this appointment"""
        if self.sales_invoice:
            return

        if not self.net_amount or flt(self.net_amount) == 0:
            return

        patient = frappe.get_doc("Clinic Patient", self.patient)
        if not patient.linked_customer:
            frappe.throw("المريض ليس لديه حساب عميل مرتبط. برجاء حفظ ملف المريض أولاً.")

        inv = frappe.new_doc("Sales Invoice")
        inv.customer = patient.linked_customer
        inv.due_date = nowdate()
        inv.clinic_appointment = self.name

        # Add services as invoice items
        if self.services_table:
            for svc in self.services_table:
                inv.append("items", {
                    "item_code": svc.item_code or svc.service_name,
                    "item_name": svc.service_name,
                    "description": f"جلسة {self.session_type} - {self.appointment_date}",
                    "qty": 1,
                    "rate": flt(svc.amount),
                    "amount": flt(svc.amount),
                })
        else:
            # Add generic item if no services
            inv.append("items", {
                "item_name": f"جلسة {self.session_type}",
                "description": f"موعد {self.appointment_date} - الدكتور {self.doctor}",
                "qty": 1,
                "rate": flt(self.net_amount),
            })

        # Apply discount
        if self.discount_amount and flt(self.discount_amount) > 0:
            inv.discount_amount = flt(self.discount_amount)
            inv.apply_discount_on = "Grand Total"

        # Add next appointment as remark
        if self.next_appointment_date:
            inv.remarks = f"الموعد القادم: {self.next_appointment_date}"

        inv.insert(ignore_permissions=True)
        inv.submit()

        self.db_set("sales_invoice", inv.name)
        self.db_set("invoice_status", "مُصدرة")
        frappe.msgprint(f"✅ تم إنشاء الفاتورة تلقائياً: {inv.name}", alert=True)


# ---------- Scheduled Task ----------

def send_appointment_reminders():
    """Run daily: send reminder for tomorrow's appointments"""
    tomorrow = add_days(nowdate(), 1)
    appointments = frappe.get_all(
        "Clinic Appointment",
        filters={
            "appointment_date": tomorrow,
            "status": "مجدول",
            "reminder_sent": 0,
            "docstatus": ["!=", 2],
        },
        fields=["name", "patient_name", "patient_mobile", "appointment_time", "doctor"],
    )

    for appt in appointments:
        try:
            send_whatsapp_reminder(appt)
            frappe.db.set_value("Clinic Appointment", appt.name, {
                "reminder_sent": 1,
                "reminder_date": frappe.utils.now(),
            })
            frappe.db.commit()
        except Exception as e:
            frappe.log_error(str(e), "Clinic Reminder Error")


def send_whatsapp_reminder(appt):
    """
    Placeholder for WhatsApp/SMS integration.
    Replace this with your actual WhatsApp API (Twilio, WhatsApp Business API, etc.)
    """
    message = (
        f"عزيزنا {appt.patient_name}،\n"
        f"نذكركم بموعدكم غداً الساعة {appt.appointment_time}\n"
        f"مع الدكتور {appt.doctor}\n"
        f"نتمنى لكم الشفاء العاجل 🦷"
    )
    frappe.log_error(f"Reminder for {appt.patient_mobile}: {message}", "Clinic Reminder")
    # TODO: Integrate with WhatsApp Business API here


# ---------- API Endpoints ----------

@frappe.whitelist()
def get_patient_appointments(patient):
    return frappe.get_all(
        "Clinic Appointment",
        filters={"patient": patient},
        fields=["name", "appointment_date", "appointment_time", "session_type",
                "doctor", "status", "net_amount", "paid_amount", "balance_amount"],
        order_by="appointment_date desc",
    )


@frappe.whitelist()
def get_doctor_schedule(doctor, date):
    appointments = frappe.get_all(
        "Clinic Appointment",
        filters={
            "doctor": doctor,
            "appointment_date": date,
            "status": ["not in", ["ملغي", "غائب"]],
        },
        fields=["name", "appointment_time", "patient_name", "session_type", "status"],
        order_by="appointment_time asc",
    )
    return appointments
