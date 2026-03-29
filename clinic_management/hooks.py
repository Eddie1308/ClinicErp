app_name = "clinic_management"
app_title = "Clinic Management"
app_publisher = "Clinic"
app_description = "Dental & Laser Clinic Management System"
app_icon = "octicon octicon-heart"
app_color = "#2196F3"
app_email = "admin@clinic.com"
app_license = "MIT"

# Includes in <head>
app_include_css = "/assets/clinic_management/css/clinic.css"
app_include_js = "/assets/clinic_management/js/clinic.js"

# Document Events
doc_events = {
    "Clinic Appointment": {
        "on_submit": "clinic_management.clinic_management.doctype.clinic_appointment.clinic_appointment.on_submit",
        "on_cancel": "clinic_management.clinic_management.doctype.clinic_appointment.clinic_appointment.on_cancel",
    }
}

# Scheduled Tasks
scheduler_events = {
    "daily": [
        "clinic_management.clinic_management.doctype.clinic_appointment.clinic_appointment.send_appointment_reminders"
    ]
}

# Fixtures
fixtures = [
    {"dt": "Custom Field"},
    {"dt": "Property Setter"},
]
