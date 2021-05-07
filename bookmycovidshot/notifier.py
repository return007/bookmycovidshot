import smtplib
import os


class Notifier(object):

    def notify(self):
        raise NotImplemented


class EmailNotifier(Notifier):

    def __init__(self):
        self.email_user = "bookmycovid19shot@gmail.com"
        self.email_password = os.environ["GMAIL_PASSWORD"]
        self.server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        self.server.ehlo()
        self.server.login(self.email_user, self.email_password)

    def format(self, details, to):
        subject = 'Covid19 vaccine slot available for you!'
        body = (
            '<h3>Hi user,</h3>'
            '<p style="font-size: 14px">We have found the following vaccine available per your preferences. Please refer to the following table:</p>'
            '<table style="font-size: 14px; border: 1px solid black; border-collapse: collapse; width: 80%;">'
            '<tr style="border: 1px solid black;">'
            '<th style="border: 1px solid black; padding: 5px;">S. No.</th>'
            '<th style="border: 1px solid black; padding: 5px;">Center Name</th>'
            '<th style="border: 1px solid black; padding: 5px;">Pin Code</th>'
            '<th style="border: 1px solid black; padding: 5px;">Date</th>'
            '<th style="border: 1px solid black; padding: 5px;">Slots</th>'
            '</tr>'
        )

        for i in range(0, len(details)):
            body += (
                "<tr style='border: 1px solid black;'>"
                "<td style='border: 1px solid black; padding: 5px;'>{}</td>"
                "<td style='border: 1px solid black; padding: 5px;'>{}</td>"
                "<td style='border: 1px solid black; padding: 5px;'>{}</td>"
                "<td style='border: 1px solid black; padding: 5px;'>{}</td>"
                "<td style='border: 1px solid black; padding: 5px;'>{}</td>"
                "</tr>\n".format(i+1, details[i]['center_name'], details[i]['pin_code'], details[i]['date'],
                                 details[i]['slots'])
            )

        body += (
            "</table>"
            "<p style='font-size: 14px; font-weight: bold'>Please visit the <a href='https://selfregistration.cowin.gov.in/'>Cowin website</a> and book your slot immediately!</p>"
            "<p style='font-size: 14px'>We hope you get vaccinated.<br><br>"
            "Stay safe,<br>"
            "Your caring buddies <a href='http://bookmycovidshot.com'>@BookMyCovidShot</a></p>"
            "<br>"
            "<p style='font-style: italic'>The moment we send you this email, we delete all your information from our records. "
            "In case you couldn't book a slot, please reschedule an alert with us @http://bookmycovidshot.com to get notified again!</p>"
        )

        email_text = """\
From: %s
To: %s
MIME-Version: 1.0
Content-type: text/html
Subject: %s

%s
        """ % (self.email_user, ", ".join(to), subject, body)

        return email_text


    def notify(self, details, to):
        if isinstance(to, (str, bytes)):
            to = [to]
        email_text = self.format(details, to)
        try:
            self.server.sendmail(self.email_user, to, email_text)
            print("Email sent to '%s'" % to)
            return True
        except Exception as e:
            print("Couldn't send email to '%s'\nException occurred: %s" % (to, e))
            return False
