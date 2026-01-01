import frappe

def get_context(context):
    context.no_cache = 1
    user = frappe.session.user

    announcement_name = frappe.form_dict.get("name")
    announcement = frappe.get_doc("Announcement", announcement_name)
    context.announcement = announcement
    return context