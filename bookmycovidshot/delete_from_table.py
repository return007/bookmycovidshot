def delete_after_sending_email(table, email_address):
    table.delete_item(Key={
        'email_address': email_address
    }
    )
