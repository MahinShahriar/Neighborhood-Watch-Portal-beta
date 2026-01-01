import frappe
from frappe.utils import today

def get_context(context):
    context.no_cache = 1

    # Fetch all announcements with expiry date in future or empty
    announcements = frappe.get_all(
            "Announcement",
            filters={"valid_till": [">=", today()]},
            fields=["name","title", "description", "attachments", "priority", "valid_till"]  # use the correct field name
        )

    # Manual sorting by priority: High > Medium > Low, then expiry_date
    priority_order = {"High": 0, "Medium": 1, "Low": 2}
    announcements.sort(key=lambda x: (priority_order.get(x.priority, 3), x.valid_till or "9999-12-31"))

    context.announcements = announcements
    return context
