import frappe
from frappe.utils import get_datetime

def get_avg_resolution_time():
    issues = frappe.get_all(
        "Issue Report",
        filters={"status": "Resolved"},
        fields=["creation", "resolved_at"]
    )

    if not issues:
        return 0

    total = 0
    count = 0

    for i in issues:
        if not i.resolved_at:   
            continue
        created = get_datetime(i.creation)
        resolved = get_datetime(i.resolved_at)
        total += (resolved - created).total_seconds()
        count += 1

    return total / count if count else 0


@frappe.whitelist()
def avg_resolution_api():
    avg_seconds = get_avg_resolution_time()
    avg_hours = avg_seconds / 3600

    return {"avg_hours": avg_hours}

