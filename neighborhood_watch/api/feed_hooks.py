import frappe


def auto_hide_post(doc, method):
    if doc.flags_count >= 3:
        doc.is_hidden = 1

# def after_insert(doc, method=None):
#     frappe.publish_realtime(
#         event="new_feed_post",
#         message={
#             "name": doc.name,
#             "message": doc.message,
#             "owner": doc.owner,
#             "creation": doc.creation
#         },
#         broadcast=True   # send to all users
#     )