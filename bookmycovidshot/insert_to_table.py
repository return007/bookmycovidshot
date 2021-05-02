import boto3


def insert_user_data_to_db(email_address, age, pin_codes, start_date='', end_date='', fee_type='', vaccine=''):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Vaccination_Details_Table')
    response = table.put_item(
        Item={
            'email_address': email_address,
            'age': age,
            'pin_codes': pin_codes,
            'start_date': start_date,
            'end_date': end_date,
            'fee_type': fee_type,
            'vaccine': vaccine
        }
    )

    print(response)


#insert_user_data_to_db(email_address="kumar@gmail.com", age=50, pin_codes={560042}, vaccine='')
