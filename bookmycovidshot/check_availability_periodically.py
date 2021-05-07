import boto3
from get_availability_from_cowin import get_availability
from delete_from_table import delete_after_sending_email
from notifier import EmailNotifier
from success_db_update import make_entry_to_success_db
import traceback

dynamodb = boto3.resource('dynamodb')


def check_availability_for_db():
    table = dynamodb.Table('Vaccination_Details_Table')
    resp = table.scan()
    en = EmailNotifier()
    success_count = 0
    total_count = 0
    for item in resp['Items']:
        total_count += 1
        try:
            shot_details = get_availability(age=item['age'], pin_codes=item['pin_codes'],
                                            start_date_str=item['start_date'],
                                            end_date_str=item['end_date'], fee_type=item['fee_type'],
                                            vaccine=item['vaccine'])
            if not shot_details:
                continue
            else:
                if not en.notify(shot_details, [item['email_address']]):
                    en = EmailNotifier()
                    if not en.notify(shot_details, [item['email_address']]):
                        print("Retry failed too. Some thing is wrong")
                        continue
                make_entry_to_success_db(item)
                delete_after_sending_email(table, email_address=item['email_address'])
            success_count += 1
        except:
            print("Some error occurred {0}".format(traceback.format_exc()))
            pass
    print("Success: %s/%s" % (success_count, total_count))
