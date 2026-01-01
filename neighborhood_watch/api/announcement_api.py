import frappe
from frappe.utils import nowdate

@frappe.whitelist()
def get_announcements():
    today = nowdate()

    announcements = frappe.get_all(
        "Announcement",
        filters={
            "is_active": 1,
            "valid_till": [">=", today]
        },
        fields=[
            "title",
            "description",
            "priority",
            "expiry_date",
            "attachments",
            "valid_till",
            "creation"
        ],
        order_by="""
            FIELD(priority, 'High', 'Medium', 'Low'),
            valid_till asc
        """
    )

    return announcements
