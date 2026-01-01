import frappe
from frappe import _
#### notification exist in site ####
def notify_admin_new_issue(doc, method):
    # Get all Admin users
    admin_users = frappe.get_all(
        "Has Role",
        filters={"role": "Admin"},
        fields=["parent as user"]
    )

    for admin in admin_users:
        user = admin.user

        # 1. Desktop notification
        frappe.publish_realtime(
            "new_issue_alert",
            {
                "title": "New Issue Reported",
                "message": f"Issue #{doc.name}: {doc.category}",
                "issue": doc.name
            },
            user=user
        )

        # 2. Email
        # frappe.sendmail(
        #     recipients=[user],
        #     subject=f"New Issue Reported: {doc.category}",
        #     message=f"""
        #         A new issue has been created.<br><br>
        #         <b>Category:</b> {doc.category}<br>
        #         <b>Description:</b> {doc.description}<br>
        #         <b>Severity:</b> {doc.severity}<br>
        #         <b>Resident:</b> {doc.resident}<br><br>
        #         <a href='{frappe.utils.get_url_to_form("Issue Report", doc.name)}'>
        #             View Issue
        #         </a>
        #     """
        # )


def validate_issue(doc, method):
    # Check if description is empty or only whitespace
    if not doc.description or not doc.description.strip():
        frappe.throw(_("Description cannot be empty."), frappe.ValidationError)
    

###### created notification in UI 
def notify_status_change(doc, method):
    # Get previous document to compare changes
    previous = doc.get_doc_before_save()

    # If no previous doc (new document), do nothing
    if not previous:
        return

    # Check if status changed
    if previous.status != doc.status:

        # Message to send
        subject = _("Your issue has been updated")
        message = _(
            f"Hello,<br><br>"
            f"Your issue <b>{doc.name}</b> status changed from "
            f"<b>{previous.status}</b> to <b>{doc.status}</b>.<br><br>"
            "Thank you!"
        )

        # Send notification email to the resident (issue owner)
        # if doc.resident:
        #     frappe.sendmail(
        #         recipients=[doc.resident],
        #         subject=subject,
        #         message=message,
        #     )

        # # Optional: Notification Log entry
        frappe.publish_realtime(
            event='msgprint',
            message=f"Issue {doc.name} updated to '{doc.status}'.",
            user=doc.resident
        )

# set resolved_at timestamp if status is Resolved
def set_resolved_time(doc, method):
     if doc.status == "Resolved" and not doc.resolved_time:
        created_at = frappe.utils.get_datetime(doc.creation)
        resolved_at = frappe.utils.now_datetime()
        delta = resolved_at - created_at

        # Convert total seconds to decimal hours
        total_hours = delta.total_seconds() / 3600
        print("Total hours to resolve:", total_hours, "\n\n\n\n")
        doc.resolved_time = total_hours
        print("Resolved time set to:", doc.resolved_time, "\n\n\n\n")
        doc.save() 

