from rtkit.resource import RTResource
from rtkit.authenticators import BasicAuthenticator
from rtkit.authenticators import CookieAuthenticator
from rtkit.errors import RTResourceError
from rtkit import set_logging

import logging

set_logging('debug')
logger = logging.getLogger('rtkit')

DEBUGGING=True

def read_credentials(credentials_file):
    with open(credentials_file) as f:
        content = f.readlines()
    return content[0], content[1]

username, password = read_credentials("credentials.txt")
resource = RTResource('https://help.rice.edu/REST/1.0/', username, password, CookieAuthenticator)

def submit_ticket(queue, status, requestor, subject, text):
    global resource, DEBUGGING
    content = {
        'content' : {
            'Queue' : queue,
            'Status' : status,
            'Requestor' : requestor,
            'Subject' : subject,
            'Text' : text
        }
    }
    if DEBUGGING:
        print "DEBUGGING - sent response with content:"
        print content
    else:
        try:
            response = resource.post(path='ticket/new', payload=content,)
            logger.info(response.parsed)
        except RTResourceError as e:
            print "ERROR"
            logger.error(e.response.status_int)
            logger.error(e.response.status)
            logger.error(e.response.parsed)

def submit_walkin_ticket(form_response):
    name = form_response['name']
    net_id = form_response['net_id']
    service = form_response['service']
    submit_ticket("SC: Repair Center",
                  "resolved",
                  net_id + "@rice.edu",
                  "Auto Walk-In Ticket",
                  "The following user was helped at the Help Desk:" +
                  "\nName: " + name +
                  "\nNetID: " + net_id +
                  "\n" + name + " was helped with " + service)

def submit_print_refund(form_response):
    fields = ["name", "net_id", "student_id", "date_of_print", "time_of_print", "printer_name", "file_name", "num_pages", "plot_attached", "header_attached", "converted_to_pdf", "downsampled", "explanation"]
    net_id = form_response['net_id']
    body = "\n".join(map(lambda field: field + ":" + form_response[field], fields))
    submit_ticket("SC: Printing Refund",
                  "resolved",
                  net_id + "@rice.edu",
                  "Auto Print Refund",
                  body)
