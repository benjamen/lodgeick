import frappe
from frappe.utils import cstr

# Allow guest access to the landing page
no_cache = 1

def get_context(context):
	# Allow guest users to access the page
	frappe.flags.ignore_permissions = True

	# Get the boot data for the frontend
	context.boot = frappe._dict({
		"session": {
			"user": frappe.session.user,
			"csrf_token": frappe.session.data.csrf_token if frappe.session.data else "",
		},
		"sitename": frappe.local.site,
	})
	context.no_cache = 1
	return context
