import frappe

def get_context(context):
    context.no_cache = 1

    if frappe.session.user == "Guest":
        frappe.throw("Login required")

    post_name = frappe.form_dict.get("name")
    if not post_name:
        frappe.throw("Post not found")

    # # context.post = frappe.get_doc("Community Feed Post", post_name, fields=[
    #     "name",
    #     "posted_by",
    #     "message",
    #     "attachments",
    #     "creation"
    # ]))

    post = frappe.get_doc("Community Feed Post", post_name)
    context.post = post
    
    return context