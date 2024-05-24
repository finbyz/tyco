# -*- coding: utf-8 -*-
import frappe
from frappe import _, sendmail, db
from frappe.utils import nowdate, add_days, getdate, get_time, add_months
from frappe.core.doctype.communication.email import make
from frappe.utils.background_jobs import enqueue
from datetime import timedelta, date, datetime, time
from frappe.desk.reportview import get_match_cond, get_filters_cond
import datetime as datetime

def time_tango(date, time):
    return datetime.datetime.strptime("{}, {}".format(date, time), "%Y-%m-%d, %H:%M:%S")

@frappe.whitelist()
def issue_before_save(self, method): 
	opening_datetime = time_tango(self.opening_date,self.opening_time)
	self.due_date = opening_datetime + (timedelta(minutes=30))
	frappe.db.commit()

@frappe.whitelist()
def issue_reports():
	enqueue(issue_delay_reports, queue='long', timeout=2000)
@frappe.whitelist()
def issue_delay_reports():
	data = db.sql("""
			SELECT
				name, subject, project, status, engineer_name, email_sent, due_date, escalation_mail_to
			FROM
				`tabIssue`
			WHERE
				(status = 'Open') and
				email_sent = 0 and
				CASE WHEN due_date IS NOT NULL THEN 
					due_date < NOW()
				END
			""", as_dict=1)

	if data:
		for row in data:
			if not row.escalation_mail_to:
				row.escalation_mail_to = "shubham.dhamija@ibtevolve.com"
			frappe.db.set_value("Issue", row.name, "email_sent", 1)
			# frappe.db.set_value("Issue", row.name, "status", "Overdue")
			if row.engineer_name:
				msg = "The issue " + row.name+ "#"+ row.subject + " that was assigned to " + row.engineer_name +" is overdue"
			else:
				msg = "The issue " + row.name+ "#"+ row.subject +" is overdue"
			sendmail(recipients = [row.escalation_mail_to],
					subject = 'Issue '+ row.name + ' is Overdue', 
					message = msg,
					now= 1)
			frappe.db.commit()


# searches for customer
@frappe.whitelist()
def customer_query1(doctype, txt, searchfield, start, page_len, filters):
	conditions = []
	cust_master_name = frappe.defaults.get_user_default("cust_master_name")

	if cust_master_name == "Customer Name":
		fields = ["name", "unique_ref_num", "site_address", "territory"]
	else:
		fields = ["name", "customer_name", "unique_ref_num", "site_address", "territory"]

	meta = frappe.get_meta("Customer")
	searchfields = meta.get_search_fields()
	searchfields = searchfields + [f for f in [searchfield or "name", "customer_name"] \
			if not f in searchfields]
	fields = fields + [f for f in searchfields if not f in fields]
	fields = ", ".join(fields)
	searchfields = " or ".join([field + " like %(txt)s" for field in searchfields])

	return frappe.db.sql("""select {fields} from `tabCustomer`
		where docstatus < 2
			and ({scond}) and disabled=0
			{fcond} {mcond}
		order by
			if(locate(%(_txt)s, name), locate(%(_txt)s, name), 99999),
			if(locate(%(_txt)s, customer_name), locate(%(_txt)s, customer_name), 99999),
			idx desc,
			name, customer_name
		limit %(start)s, %(page_len)s""".format(**{
			"fields": fields,
			"scond": searchfields,
			"mcond": get_match_cond(doctype),
			"fcond": get_filters_cond(doctype, filters, conditions).replace('%', '%%'),
		}), {
			'txt': "%%%s%%" % txt,
			'_txt': txt.replace("%", ""),
			'start': start,
			'page_len': page_len
		})