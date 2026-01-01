import frappe
from datetime import datetime

def get_context(context):
    # Get active announcements
    context.announcements = frappe.get_all(
        "Announcement",
        # filters={"published": 1},
        fields=["title", "description", "attachments", "priority", "valid_till"],
        order_by="priority desc, valid_till asc",
        limit=5
    )

    # Show counts only for logged-in users
    if not frappe.session.user == "Guest":
        context.open_issues = frappe.db.count("Issue Report", {"status": "Open", "resident": frappe.session.user})
        context.in_progress = frappe.db.count("Issue Report", {"status": "In Progress", "resident": frappe.session.user})
        context.resolved = frappe.db.count("Issue Report", {"status": "Resolved", "resident": frappe.session.user})
        context.closed = frappe.db.count("Issue Report", {"status": "Closed", "resident": frappe.session.user})

    return context
