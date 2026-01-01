import frappe


def get_context(context):
    context.no_cache = 1

    # Guest → redirect to login
    if frappe.session.user == "Guest":
        frappe.local.flags.redirect_location = "/login?redirect-to=community-feed"
        raise frappe.Redirect

    user = frappe.session.user
    
    # Fetch recent community posts
    context.posts = frappe.get_all(
        "Community Feed Post",
        fields=["name", "posted_by", "message", "attachments", "creation"],
        order_by="creation desc",
        limit=5
    )

    context.user = user
    return context