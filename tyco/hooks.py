# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "tyco"
app_title = "Tyco"
app_publisher = "Finbyz Tech Pvt Ltd"
app_description = "Custom App for Tyco"
app_icon = "octicon octicon-briefcase"
app_color = "orange"
app_email = "info@finbyz.com"
app_license = "GPL 3.0"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/tyco/css/tyco.css"
# app_include_js = "/assets/tyco/js/tyco.js"

# include js, css files in header of web template
# web_include_css = "/assets/tyco/css/tyco.css"
# web_include_js = "/assets/tyco/js/tyco.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "tyco.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "tyco.install.before_install"
# after_install = "tyco.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "tyco.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }
doc_events = {
	"Issue": {
 		"before_save": "tyco.api.issue_before_save"
 	}
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"tyco.tasks.all"
# 	],
# 	"daily": [
# 		"tyco.tasks.daily"
# 	],
# 	"hourly": [
# 		"tyco.tasks.hourly"
# 	],
# 	"weekly": [
# 		"tyco.tasks.weekly"
# 	]
# 	"monthly": [
# 		"tyco.tasks.monthly"
# 	]
# }
scheduler_events = {
	"cron":{
		"0/1 * * * *": [
            "tyco.api.issue_reports"
        ]
	}
}
# Testing
# -------

# before_tests = "tyco.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "tyco.event.get_events"
# }

