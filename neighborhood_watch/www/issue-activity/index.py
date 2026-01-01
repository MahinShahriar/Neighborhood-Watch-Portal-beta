import frappe

def get_context(context):
    context.no_cache = 1

    # Only logged-in Residents
    user = frappe.session.user
    if user == "Guest":
        frappe.local.flags.redirect_location = "/login?redirect-to=issue-activity"
        raise frappe.Redirect

    # Get activity of Issue Report Doctype
    activities = frappe.get_all(
        "Activity Log",
        filters={"reference_doctype": "Issue Report", "owner": user},
        fields=["owner", "modified", "content"],
        order_by="modified desc"
    )

    context.activities = activities
    print("\n\n",'hello=====================',"\n\n", context.activities,"\n\n\nhello=====================\n\n")
    return context
