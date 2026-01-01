# import frappe

# def get_notifications():
#     if frappe.session.user == "Guest":
#         return []

#     frappe.logger().info("Website notifications loaded")

#     return frappe.get_all(
#         "Notification Log",
#         filters={"for_user": frappe.session.user},
#         fields=["name", "subject", "creation"],
#         order_by="creation desc",
#         limit_page_length=10
#     )
# 