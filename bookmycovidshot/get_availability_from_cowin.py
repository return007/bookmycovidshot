import requests
import json
import datetime
import time


BASE_URL = (
    "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin"
    "?pincode=%s&date=%s"
)


def slots_to_str(session_slots):
    slots_str = ''
    for slot in session_slots:
        slots_str = slots_str + slot + '\n'
    return slots_str


def fetch_from_cowin(url):
    try:
        r = requests.get(
            url,
            headers={
                'Origin': 'https://www.cowin.gov.in',
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                              '(KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
                'Referer': 'https://www.cowin.gov.in/'
            }, timeout=3
        )
    except requests.exceptions.RequestException as e:
        print(e)
    return r.json()


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
        # Between two consecutive requests, wait for 3 seconds.
        resp_json = fetch_from_cowin(BASE_URL % (pin_code, query_date))
        given_age = age
        for covid_center in resp_json["centers"]:
            if len(covid_center) == 0:
                print("Vaccine schedule not available.")
                return
            if fee_type == 'any' or fee_type == covid_center['fee_type']:
                for session in covid_center['sessions']:
                    start_timing = datetime.datetime.today()
                    if len(session['slots']) > 0:
                        dt_str = session['date'] + ' '+ session['slots'][len(session['slots'])-1].split('-')[1]
                        start_timing = datetime.datetime.strptime(dt_str, "%d-%m-%Y %I:%M%p")
                    if (len(session['slots']) == 0 or start_timing > datetime.datetime.today()) and \
                            session['min_age_limit'] <= given_age and \
                            (vaccine == 'any' or vaccine == session['vaccine']) and \
                            (datetime.datetime.strptime(session['date'], "%d-%m-%Y") <= end_date) and \
                            session['available_capacity'] > 0:
                        covid_center_details['center_name'] = covid_center['name']
                        covid_center_details['date'] = session['date']
                        covid_center_details['slots'] = slots_to_str(session['slots'])
                        covid_center_details['pin_code'] = pin_code
                        shot_details.append(covid_center_details)
                        covid_center_details = {}

        time.sleep(3)
    return shot_details


#print(get_availability(age = 45, pin_codes=[333504], start_date_str='01-05-2021', end_date_str='05-05-2021'))
