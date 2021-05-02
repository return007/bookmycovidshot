from util import is_empty

from flask import Flask, render_template, request


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

    email    = form_data.get("email")
    age      = form_data.get("age")
    pincode  = form_data.get("pincode")
    username = form_data.get("username", "User")

    # TODO: Decide start date (should be today, if not provided)
    start_date = form_data.get("start_date")
    # TODO: Decide end date (should be infinite, if not provided)
    end_date = form_data.get("end_date")

    cvc_type = form_data.get("cvc_type", "any")
    if cvc_type not in ("any", "govt", "pvt"):
        should_error = True
        error_msg = "Hey, please don't play around with the inputs you lil piece of shit"

    vaccine_choice = form_data.get("vaccine_choice", "any")
    if vaccine_choice not in ("any", "covishield", "covaxin"):
        should_error = True
        error_msg = "Hey, please don't play around with the inputs you lil piece of shit"

    if should_error:
        return error_msg, 400

    return "Email ID: %s" % email


@app.route('/alert')
def alert():
    return render_template('alert.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
