import frappe

def get_context(context):
    context.no_cache = 1

    # If guest → force login
    if frappe.session.user == "Guest":
        frappe.local.flags.redirect_location = "/login?redirect-to=my-issues"
        raise frappe.Redirect

    # Fetch only user's issues
    context.issues = frappe.get_all(
        "Issue Report",
        filters={"resident": frappe.session.user},
        fields=["name", "category", "description", "status", "modified"],
        order_by="modified desc"
    )


    return context
