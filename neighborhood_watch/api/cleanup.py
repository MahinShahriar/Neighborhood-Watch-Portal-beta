import frappe
from frappe.utils import today

def delete_expired_announcements():
    frappe.db.delete("Announcement", {"valid_till": ("<", today())})
    frappe.db.commit()

def delete_attachments(doc, method):
    files = frappe.get_all(
        "File",
        filters={
            "attached_to_doctype": doc.doctype,
            "attached_to_name": doc.name
        }
    )
    for f in files:
        frappe.delete_doc("File", f.name, ignore_permissions=True)