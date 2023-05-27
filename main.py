from datetime import datetime, timedelta
import os

import pyotp
import requests

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()
secret_key = pyotp.random_base32()
totp = pyotp.TOTP(secret_key, interval=120)
class VerifyOTPRequest(BaseModel):
    merchid: str
    otp: str
    userid: str
    amount: float

class UserIDRequest(BaseModel):
    merchid: str
    userid: str
    amount: float

def send_sms(userid, message):
    cred = os.getenv('ADASMS_CRED')
    if cred:
        payload = {
            '_token': cred,
            'phone': userid,
            'message': message,
        }
        response = requests.post('https://terminal.adasms.com/api/v1/send', files=payload)
        if response.status_code == 200:
            return "SMS sent successfully."
        else:
            return f'Failed to send SMS. Status code: {response.status_code}'
    else:
        return "cred is empty"

@app.get("/health")
def get_health():
    return {"health": "ok"}

@app.post("/otp")
def get_otp(request: UserIDRequest):
    otp = totp.now()
    merchid = request.merchid
    userid = request.userid
    amount = request.amount
    current_datetime = datetime.now()
    new_datetime = current_datetime + timedelta(seconds=120)
    formatted_amount = "{:.2f}".format(amount)
    formatted_datetime = new_datetime.strftime("%H:%M:%S %d %B %Y")
    message = f'[DuitNow SMS] Merchant {merchid} RM {formatted_amount} - OTP code {otp} - expires on {formatted_datetime}'
    status = send_sms(userid, message)
    return {
        "otp" : otp,
        "phone" : userid,
        "amount" : amount,
        "message" : message,
        "sms_status" : status,
        }

@app.post("/verify")
def verify_otp(request: VerifyOTPRequest):
    otp = request.otp
    is_valid = totp.verify(otp)
    if not is_valid:
        raise HTTPException(status_code=400, detail="Invalid OTP")
    userid = request.userid
    merchid = request.merchid
    amount = request.amount
    formatted_amount = "{:.2f}".format(amount)
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%H:%M:%S %d %B %Y")
    message = f'[DuitNow SMS] Payment RM {formatted_amount} to Merchant {merchid} - {formatted_datetime}'
    status = send_sms(userid, message)
    return {
        "valid": True,
        "message": message,
        "sms_status": status,
        }