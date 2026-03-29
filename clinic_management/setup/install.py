import frappe


def after_install():
    """Run after app installation - create roles and default items"""
    create_roles()
    create_default_items()
    frappe.db.commit()
    print("✅ Clinic Management installed successfully!")


def create_roles():
    roles = ["Clinic Doctor", "Clinic Receptionist", "Clinic Manager"]
    for role_name in roles:
        if not frappe.db.exists("Role", role_name):
            role = frappe.new_doc("Role")
            role.role_name = role_name
            role.desk_access = 1
            role.insert(ignore_permissions=True)
            print(f"  ✅ Role created: {role_name}")


def create_default_items():
    """Create default service items for billing"""
    items = [
        {"item_name": "كشف أسنان", "item_group": "Services", "rate": 100},
        {"item_name": "حشو عادي", "item_group": "Services", "rate": 150},
        {"item_name": "حشو ضوئي", "item_group": "Services", "rate": 250},
        {"item_name": "خلع سن", "item_group": "Services", "rate": 200},
        {"item_name": "علاج عصب", "item_group": "Services", "rate": 800},
        {"item_name": "تلبيس", "item_group": "Services", "rate": 600},
        {"item_name": "تنظيف جير", "item_group": "Services", "rate": 300},
        {"item_name": "زراعة أسنان", "item_group": "Services", "rate": 3000},
        {"item_name": "جلسة ليزر", "item_group": "Services", "rate": 500},
        {"item_name": "استشارة", "item_group": "Services", "rate": 100},
    ]

    for item_data in items:
        if not frappe.db.exists("Item", {"item_name": item_data["item_name"]}):
            item = frappe.new_doc("Item")
            item.item_name = item_data["item_name"]
            item.item_code = item_data["item_name"]
            item.item_group = item_data.get("item_group", "Services")
            item.is_sales_item = 1
            item.is_service_item = 1
            item.standard_rate = item_data.get("rate", 0)
            try:
                item.insert(ignore_permissions=True)
                print(f"  ✅ Item created: {item_data['item_name']}")
            except Exception:
                pass  # Item group might not exist, skip
