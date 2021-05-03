from util import is_empty
from insert_to_table import insert_user_data_to_db
from flask import Flask, render_template, request
from apscheduler.schedulers.background import BackgroundScheduler
from check_availability_periodically import check_availability_for_db
from datetime import datetime, timedelta

app = Flask(__name__)
"""
Flask app instance.
"""

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    # On submit, check if the mandatory fields exists or not
    form_data = request.form
    should_error = False
    if is_empty(form_data, "email"):
        # User hasn't provided Email ID
        # I hate the user, let me show my hatred real quick
        should_error = True
        error_msg = "No EMAIL ID was provided, cannot schedule alert"
    if is_empty(form_data, "age"):
        # User hasn't provided age
        # Are you kidding me!!!
        should_error = True
        error_msg = "No age was provided, cannot schedule alert"
    if is_empty(form_data, "pincode"):
        # User hasn't provided pincode
        should_error = True
        error_msg = "No pincode was provided, cannot schedule alert"
    if should_error:
        return error_msg, 400

    email = form_data.get("email")
    age = int(form_data.get("age"))
    pincode = form_data.get("pincode")
    username = form_data.get("username", "user")

    start_date = form_data.get("start_date")
    if not start_date:
        start_date = datetime.today().strftime('%Y-%m-%d')

    end_date = form_data.get("end_date")

    if not end_date:
        end_date = (datetime.today() + timedelta(days=365)).strftime('%Y-%m-%d')

    cvc_type = form_data.get("cvc_type", "any")
    if cvc_type not in ("any", "Free", "Paid"):
        should_error = True
        error_msg = "Hey, please don't play around with the inputs you lil piece of shit"

    vaccine_choice = form_data.get("vaccine_choice", "any")
    if vaccine_choice not in ("any", "COVISHIELD", "COVAXIN"):
        should_error = True
        error_msg = "Hey, please don't play around with the inputs you lil piece of shit"

    pincode_set = set(pincode.split(";"))
    if should_error:
        return error_msg, 400

    insert_user_data_to_db(email, age, pincode_set, start_date=start_date, end_date=end_date, fee_type=cvc_type, vaccine=vaccine_choice)

    return render_template("alert_success.html", username=username)


sched = BackgroundScheduler()
sched.add_job(check_availability_for_db,'cron', minute='*')
sched.start()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)


