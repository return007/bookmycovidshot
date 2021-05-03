import smtplib
import os


def send_email_update(shot_details, to_email):
    print(shot_details)
    gmail_user = 'bookmycovid19shot@gmail.com'
    gmail_password = os.environ["GMAIL_PASSWORD"]

    sent_from = gmail_user
    subject = 'Covid19 vaccine slot available for you!'
    body = (
        '<h3>Hi user,</h3>'
        '<p style="font-size: 14px">We have found the following vaccine available per your preferences. Please refer to the following table:</p>'
        '<table style="font-size: 14px; border: 1px solid black; border-collapse: collapse; width: 80%;">'
        '<tr style="border: 1px solid black;">'
        '<th style="border: 1px solid black; padding: 5px;">S. No.</th>'
        '<th style="border: 1px solid black; padding: 5px;">Center Name</th>'
        '<th style="border: 1px solid black; padding: 5px;">Date</th>'
        '<th style="border: 1px solid black; padding: 5px;">Slots</th>'
        '</tr>'
    )

    for i in range(0, len(shot_details)):
        body += (
            "<tr style='border: 1px solid black;'>"
            "<td style='border: 1px solid black; padding: 5px;'>{}</td>"
            "<td style='border: 1px solid black; padding: 5px;'>{}</td>"
            "<td style='border: 1px solid black; padding: 5px;'>{}</td>"
            "<td style='border: 1px solid black; padding: 5px;'>{}</td>"
            "</tr>\n".format(i+1, shot_details[i]['center_name'], shot_details[i]['date'], shot_details[i]['slots'])
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
""" % (sent_from, ", ".join(to_email), subject, body)

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to_email, email_text)
        server.close()
        print('Email sent!')
    except Exception as e:
        print(e)
        print('Something went wrong...')

