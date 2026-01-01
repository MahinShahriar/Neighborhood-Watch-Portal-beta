import frappe

def get_context(context):
    context.no_cache = 1

    context.contacts = frappe.get_all(
        "Emergency Contact",
        fields=["title", "phone_number"]
    )

    return context
