// Copyright (c) 2025, Mahin Shahriar and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Issue Report", {
// 	refresh(frm) {

// 	},
// });


frappe.ui.form.on("Issue Report", {
    
    onload: function(frm) {
        if (frm.is_new()) {
            frm.set_value("resident", frappe.session.user);
        }
    },

    on_submit(frm) {
        frappe.show_alert({
            message: __("Issue Submitted"),
            indicator: "green"
        })
    }
});