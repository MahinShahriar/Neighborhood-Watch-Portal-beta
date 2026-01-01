import frappe
import json
from frappe import _

def get_context(context):
    context.no_cache = 1
    issue_name = frappe.form_dict.get("name")
    issue = frappe.get_doc("Issue Report", issue_name, fields=[
        "name", "resident", "description", "category", "severity",
        "status", "review_comment", "rating", "photos",
        "assigned_guard", "creation", "resolved_at"
    ])
    context.issue = issue

    versions = frappe.get_all(
        "Version",
        filters={"ref_doctype": "Issue Report", "docname": issue_name},
        fields=["owner", "creation", "data"],
        order_by="creation desc"
    )

    activities = []
    for v in versions:
        changes = []
        if v.data:
            data = frappe.parse_json(v.data)
            changes = data.get("changed", [])
        activities.append({"owner": v.owner, "creation": v.creation, "changes": changes})

    context.activities = activities

    if frappe.request.method == "PUT":
        submit_review(issue_name)
        # frappe.local.response["type"] = "redirect"
        # frappe.local.response["location"] = f"/issue-detail?name={issue_name}"

    return context


def submit_review(issue_name):
    """Handle resident review submission"""
    rating = frappe.form_dict.get("rating")
    review_comment = frappe.form_dict.get("review_comment")
    print("\n\n\n\n","Submitting review with rating:", rating, "and comment:", review_comment, "\n\n\n\n")
    if not rating or not review_comment:
        frappe.throw(_("Rating and comment are required"))

    doc = frappe.get_doc("Issue Report", issue_name, fields=["resident", "status", "rating", "review_comment"])

    # Only resident can submit and only if resolved
    if frappe.session.user != doc.resident:
        frappe.throw(_("Not allowed"))
    if doc.status != "Resolved":
        frappe.throw(_("Review not allowed"))

    doc.rating = float(rating)
    print("\n\n\n\n","Converted rating to float:", doc.rating,"\n\n\n\n")
    doc.review_comment = review_comment
    doc.save()
    frappe.db.commit()

"""
sudo fuser -k 8000/tcp
sudo fuser -k 13000/tcp
sudo fuser -k 11000/tcp
sudo pkill -9 -f frappe
sudo pkill -9 -f redis
sudo pkill -9 -f node

"""
