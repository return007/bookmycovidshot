import boto3
def delete_after_sending_email(table, email_address):
    return
    table.delete_item(Key={
        'email_address': email_address
    }
    )