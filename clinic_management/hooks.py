app_name = "clinic_management"
app_title = "Clinic Management"
app_publisher = "Clinic"
app_description = "Dental & Laser Clinic Management System - ERPNext v16"
app_email = "admin@clinic.com"
app_license = "MIT"
app_version = "1.0.0"

required_apps = ["frappe", "erpnext"]

app_include_css = "/assets/clinic_management/css/clinic.css"
app_include_js  = "/assets/clinic_management/js/clinic.js"

doc_events = {
    "Clinic Appointment": {
        "on_submit": "clinic_management.clinic_management.doctype.clinic_appointment.clinic_appointment.on_submit",
        "on_cancel": "clinic_management.clinic_management.doctype.clinic_appointment.clinic_appointment.on_cancel",
        "validate":  "clinic_management.clinic_management.doctype.clinic_appointment.clinic_appointment.validate",
    }
}

scheduler_events = {
    "daily": [
        "clinic_management.clinic_management.doctype.clinic_appointment.clinic_appointment.send_appointment_reminders"
    ]
}

workspaces = [
    {
        "doctype": "Workspace",
        "name": "Clinic Management",
        "label": "إدارة العيادة",
        "icon": "health-reconnect",
        "module": "Clinic Management",
        "category": "Modules",
        "is_hidden": 0,
    }
]

after_install = "clinic_management.setup.install.after_install"

fixtures = [
    {
        "dt": "Role",
        "filters": [["name", "in", ["Clinic Doctor", "Clinic Receptionist", "Clinic Manager"]]]
    },
    {
        "dt": "Workspace",
        "filters": [["module", "=", "Clinic Management"]]
    }
]

global_search_doctypes = {
    "Clinic Management": [
        {"doctype": "Clinic Patient"},
        {"doctype": "Clinic Appointment"},
    ]
}
