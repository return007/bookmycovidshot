import requests
import json
import datetime


def get_availability(age, pin_codes, start_date_str='',
                     end_date_str='', fee_type='',vaccine=''):

    query_date = datetime.datetime.today().strftime('%Y-%m-%d')
    date_today = datetime.datetime.strptime(query_date, '%Y-%m-%d')
    start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.datetime.today()

    if end_date_str != '':
        end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d')
        if end_date < date_today:
            print("We are past the end date.")
            return
    if start_date > date_today:
        query_date = start_date_str

    query_date = datetime.datetime.strptime(query_date, '%Y-%m-%d').strftime('%d-%m-%Y')
    shot_details = []
    covid_center_details = {}
    for pin_code in pin_codes:
        try:
            print (query_date)
            r = requests.get \
                ('https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={0}&date={1}'.
                 format(pin_code, query_date), timeout=1)
        except requests.exceptions.Timeout as e:
            print(e)
        resp_json = json.loads(r.text)
        given_age = age
        for covid_center in resp_json["centers"]:
            if len(covid_center) == 0:
                print("Vaccine schedule not available.")
                return
            if fee_type == 'any' or fee_type == covid_center['fee_type']:
                for session in covid_center['sessions']:
                    dt_str = session['date'] + ' '+ session['slots'][len(session['slots'])-1].split('-')[1]
                    start_timing = datetime.datetime.strptime(dt_str, "%d-%m-%Y %I:%M%p")
                    if start_timing > datetime.datetime.today() and session['min_age_limit'] <= given_age and \
                            (vaccine == 'any' or vaccine == session['vaccine']) and \
                            (datetime.datetime.strptime(session['date'], "%d-%m-%Y") <= end_date):
                        covid_center_details['center_name'] = covid_center['name']
                        covid_center_details['date'] = session['date']
                        covid_center_details['slots'] = session['slots']
                        shot_details.append(covid_center_details)
                        covid_center_details = {}

    # if len(shot_details) == 0:
    #     print("No vaccines data available for your age group in your area for the next seven days")
    # for i in range(0, len(shot_details)):
    #     print("Vaccines for your age group are available at {0} on date {1} slots available = {2}".
    #           format(shot_details[i]['center_name'], shot_details[i]['date'], shot_details[i]['slots']))
    return shot_details


#print(get_availability(age = 45, pin_codes=[333504], start_date_str='01-05-2021', end_date_str='05-05-2021'))
