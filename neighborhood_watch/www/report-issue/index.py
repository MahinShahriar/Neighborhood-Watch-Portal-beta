import frappe

def get_context(context):
    context.no_cache = 1

    # Redirect guest users
    if frappe.session.user == "Guest":
        frappe.local.flags.redirect_location = "/login?redirect-to=report-issue"
        raise frappe.Redirect
    
    # Pass CSRF token to template
    # context.csrf_token = frappe.form_dict.csrf_token or frappe.local.session_csrf
    return context
