import boto3


def make_entry_to_success_db(item):
    dynamodb = boto3.resource('dynamodb')
    try:
        table = dynamodb.Table('Success_DB')

        response = table.put_item(
            Item={
                'email_address': item['email_address'],
                'age': item['age'],
                'pin_codes': item['pin_codes'],
                'start_date': item['start_date'],
                'end_date': item['end_date'],
                'fee_type': item['fee_type'],
                'vaccine': item['vaccine']
            }
        )
        print(response)
    except:
        pass
