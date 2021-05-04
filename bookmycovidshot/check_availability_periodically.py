import boto3
from get_availability_from_cowin import get_availability
from delete_from_table import delete_after_sending_email
from notifier import EmailNotifier

dynamodb = boto3.resource('dynamodb')


def check_availability_for_db():
    table = dynamodb.Table('Vaccination_Details_Table')
    resp = table.scan()
    en = EmailNotifier()
    for item in resp['Items']:
        try:
            shot_details = get_availability(age=item['age'], pin_codes=item['pin_codes'],
                                            start_date_str=item['start_date'],
                                            end_date_str=item['end_date'], fee_type=item['fee_type'],
                                            vaccine=item['vaccine'])
            if not shot_details:
                continue
            else:
                en.notify(shot_details, [item['email_address']])
                delete_after_sending_email(table, email_address=item['email_address'])
        except:
            pass

#check_availability_for_db()