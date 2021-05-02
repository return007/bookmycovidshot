import smtplib
import os
def send_email_update(shot_details, to_email):
    print(shot_details)
    gmail_user = 'bookmycovid19shot@gmail.com'
    gmail_password = os.environ["GMAIL_PASSWORD"]

    sent_from = gmail_user
    subject = ''
    body = 'Please vaccinate yourself\n'

    for i in range(0, len(shot_details)):
        body += "Vaccines for your age group are available at {0} on date {1} slots available = {2}\n".format(shot_details[i]['center_name'], shot_details[i]['date'], shot_details[i]['slots'])

    email_text = """\
    From: %s
    To: %s
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

