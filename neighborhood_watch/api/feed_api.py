import frappe

# Submit Post(POST)
ALLOWED_EXT = {"jpg", "jpeg", "png", "pdf"}
MAX_SIZE_MB = 5

@frappe.whitelist()
def post_feed_message( message):
    if frappe.session.user == "Guest":
        frappe.throw("Login required")

    if not message:
        frappe.throw("Message is required")

    doc = frappe.new_doc("Community Feed Post")
    doc.posted_by = frappe.session.user  
    doc.message = message
    doc.is_hidden = 0
    doc.flag_count = 0
    doc.insert(ignore_permissions=True)
    
    if frappe.request.files:
            f = frappe.request.files.get("file")
            if f:
                ext = f.filename.split(".")[-1].lower()
                size_mb = len(f.read()) / (1024 * 1024)
                f.stream.seek(0)

                if ext not in ALLOWED_EXT:
                    frappe.throw("Only JPG, PNG, PDF allowed")

                if size_mb > MAX_SIZE_MB:
                    frappe.throw("File size must be under 5MB")

                file_doc = frappe.get_doc({
                    "doctype": "File",
                    "file_name": f.filename,
                    "attached_to_doctype": "Community Feed Post",
                    "attached_to_name": doc.name,
                    "content": f.read(),
                    "is_private": 0
                }).insert(ignore_permissions=True)

                doc.attachments = file_doc.file_url
                print(doc.attachments,"\n\n\n")
                doc.save(ignore_permissions=True)
    return {
        "success": True,
        "message": "Feed message posted",
        "post_id": doc.name
    }

# List Posts (GET)
@frappe.whitelist()
def list_posts():
    user = frappe.session.user
    if user == "Guest":
        frappe.throw("Login required")

    posts = frappe.get_all(
        "Community Feed Post",
        fields=[
            "posted_by",
            "message",
            "attachments",
            "flag_count",
            "is_hidden",
            "creation"
        ],
        order_by="creation desc"
    )

    return posts