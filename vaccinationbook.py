from datetime import datetime
import requests
import time
import gc

def create_session_info(center, session):
    return {"name": center["name"],
            "state": center["state_name"],
            "pincode": center["pincode"],
            "date": session["date"],
            "capacity": session["available_capacity"],
            "age_limit": session["min_age_limit"]}

def get_sessions(data):
    for center in data["centers"]:
        for session in center["sessions"]:

            yield create_session_info(center, session)

def is_available(session):
    return session["capacity"] > 0

def is_eighteen_plus(session):
    return session["age_limit"] == 18

def get_for_seven_days(start_date,idofdistrict):
    url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict"
    district_id=idofdistrict
    params = {"district_id": district_id, "date": start_date.strftime("%d-%m-%Y")}
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"}
    resp = requests.get(url, params=params, headers=headers)
    data = resp.json()

    return [session for session in get_sessions(data) if is_eighteen_plus(session) and is_available(session)]

def create_output(session_info):
    return f"Slot available for date:{session_info['date']} - Centre Name: {session_info['name']}- State: {session_info['state']}- Pincode: {session_info['pincode']} Available capacity: {session_info['capacity']}"

def telemsg(msg):
    base_url1='https://api.telegram.org/bot1714825395:AAFwuf6U4uBIJdy4OkwNiNYJLUYnvQzXIno/sendMessage?chat_id=-516635996&text={}'.format(msg)
    base_url='https://api.telegram.org/bot1768956750:AAEdnsklexjnIKgBti24Vvo1E_tWzvGsLkg/sendMessage?chat_id=-455242448&text={}'.format(msg)
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"}
    requests.get(base_url,headers=headers)
x=1
while x>0:
    idofdistrict=[199,85]
    for i in idofdistrict:
        content = "\n""\n".join([create_output(session_info) for session_info in get_for_seven_days(datetime(2021, 5, 28),i)])
        if not content:
            print(x)
        else:
            telemsg(content)
            print("Yes available")
    time.sleep(30)
    x=x+1

    



