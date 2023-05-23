from flask import current_app, session, redirect, url_for
from database.mysql_implementation.user import *
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Asm, GroupId

class MailService:
    def send(self, to_email, template_id, dynamic_template_data={}):
        message = Mail(
            from_email=os.getenv('FROM_EMAIL'),
            to_emails=to_email,
        )
        message.dynamic_template_data = dynamic_template_data
        message.asm = Asm(GroupId(os.getenv('SENDGRID_ASM_GROUP')))
        message.template_id = template_id
        try:
            sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
            response = sg.send(message)
        except Exception as e:
            print(e.message)