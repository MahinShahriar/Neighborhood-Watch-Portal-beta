import frappe


# Submit Issue (POST)
ALLOWED_EXT = {"jpg", "jpeg", "png", "pdf"}
MAX_SIZE_MB = 5

@frappe.whitelist()
def submit_issue(description, category, severity):
    user = frappe.session.user
    if user == "Guest":
        frappe.throw("Login required")

    doc = frappe.new_doc("Issue Report")
    doc.resident = user
    doc.description = description
    doc.category = category
    doc.severity = severity
    doc.status = "Open"
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
                "attached_to_doctype": "Issue Report",
                "attached_to_name": doc.name,
                "content": f.read(),
                "is_private": 0
            }).insert(ignore_permissions=True)

            doc.photos = file_doc.file_url
            doc.save(ignore_permissions=True)

    return {"success": True, "issue_name": doc.name}

# List Issues (GET)
@frappe.whitelist()
def list_issues():
    user = frappe.session.user
    if user == "Guest":
        frappe.throw("Login required")


    if "System Manager" in frappe.get_roles(user):
        filters = {}
    else:
        filters = {"resident": user}

    issues = frappe.get_all(
        "Issue Report",
        filters=filters,
        fields=[
            "name",
            "resident",
            "description",
            "attachment",
            "category",
            "severity",
            "status",
            "creation"
        ],
        order_by="creation desc"
    )

    return issues
