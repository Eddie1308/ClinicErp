import frappe
from frappe.model.document import Document

class $(echo $d | sed 's/_/ /g' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) substr($i,2); print}' | tr -d ' ')(Document):
    pass
