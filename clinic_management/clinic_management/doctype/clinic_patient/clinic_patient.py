import frappe
from frappe.model.document import Document
from frappe.utils import date_diff, nowdate, getdate


class ClinicPatient(Document):

    def before_save(self):
        self.calculate_age()
        self.create_customer_if_not_exists()

    def calculate_age(self):
        if self.date_of_birth:
            self.age = int(date_diff(nowdate(), self.date_of_birth) / 365)

    def create_customer_if_not_exists(self):
        """Create ERPNext Customer automatically for billing"""
        if not self.linked_customer and self.patient_name:
            if not frappe.db.exists("Customer", {"customer_name": self.patient_name}):
                customer = frappe.new_doc("Customer")
                customer.customer_name = self.patient_name
                customer.customer_type = "Individual"
                customer.customer_group = "Individual"
                customer.territory = "All Territories"
                customer.mobile_no = self.mobile
                customer.email_id = self.email or ""
                customer.insert(ignore_permissions=True)
                self.linked_customer = customer.name
                frappe.msgprint(f"تم إنشاء حساب عميل تلقائياً: {customer.name}")

    def get_appointment_history(self):
        return frappe.get_all(
            "Clinic Appointment",
            filters={"patient": self.name},
            fields=["name", "appointment_date", "session_type", "doctor", "status", "total_amount"],
            order_by="appointment_date desc",
        )

    def get_total_balance(self):
        result = frappe.db.sql("""
            SELECT SUM(balance_amount) as total_balance
            FROM `tabClinic Appointment`
            WHERE patient = %s AND docstatus = 1
        """, self.name, as_dict=True)
        return result[0].total_balance or 0
