import frappe

def get_context(context):
	# Serve the built frontend index.html
	frappe_boot = frappe.sessions.get()
	context.boot = frappe_boot
	context.no_cache = 1
	return context
