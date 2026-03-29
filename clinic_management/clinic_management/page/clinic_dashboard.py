import frappe
from frappe.utils import nowdate, add_days, getdate


@frappe.whitelist()
def get_dashboard_data():
    today = nowdate()

    # Today's appointments
    today_appointments = frappe.db.count("Clinic Appointment", {
        "appointment_date": today,
        "docstatus": ["!=", 2]
    })

    # Completed today
    completed_today = frappe.db.count("Clinic Appointment", {
        "appointment_date": today,
        "status": "مكتمل"
    })

    # Total revenue this month
    month_start = today[:8] + "01"
    revenue = frappe.db.sql("""
        SELECT SUM(net_amount) as total
        FROM `tabClinic Appointment`
        WHERE appointment_date BETWEEN %s AND %s
        AND status = 'مكتمل'
        AND docstatus = 1
    """, (month_start, today), as_dict=True)

    # Pending balance
    pending_balance = frappe.db.sql("""
        SELECT SUM(balance_amount) as total
        FROM `tabClinic Appointment`
        WHERE docstatus = 1
        AND balance_amount > 0
    """, as_dict=True)

    # Upcoming appointments (next 7 days)
    upcoming = frappe.get_all(
        "Clinic Appointment",
        filters={
            "appointment_date": ["between", [today, add_days(today, 7)]],
            "status": "مجدول",
        },
        fields=["name", "patient_name", "appointment_date", "appointment_time", "doctor", "session_type"],
        order_by="appointment_date asc, appointment_time asc",
        limit=10,
    )

    return {
        "today_appointments": today_appointments,
        "completed_today": completed_today,
        "month_revenue": revenue[0].total or 0,
        "pending_balance": pending_balance[0].total or 0,
        "upcoming": upcoming,
    }
