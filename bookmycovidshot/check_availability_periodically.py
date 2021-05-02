import boto3
from get_availability_from_cowin import get_availability
from delete_from_table import delete_after_sending_email
from send_email import send_email_update

dynamodb = boto3.resource('dynamodb')


def check_availability_for_db():
    table = dynamodb.Table('Vaccination_Details_Table')

    resp = table.scan()

    for item in resp['Items']:
        print(item)
        shot_details = get_availability(age=item['age'], pin_codes=item['pin_codes'],
                                        start_date_str=item['start_date'],
                                        end_date_str=item['end_date'], fee_type=item['fee_type'],
                                        vaccine=item['vaccine'])
        if len(shot_details) == 0:
            continue
        else:
            send_email_update(shot_details)
            delete_after_sending_email(table, email_address=item['email_address'])