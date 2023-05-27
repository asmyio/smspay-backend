from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pyotp
from mangum import Mangum


app = FastAPI()
secret_key = pyotp.random_base32()
totp = pyotp.TOTP(secret_key)
class VerifyOTPRequest(BaseModel):
    otp: str

class UserIDRequest(BaseModel):
    userid: str
    amount: int

@app.get("/health")
def get_health():
    return {"health": "ok"}

@app.post("/otp")
def get_otp(request: UserIDRequest):
    otp = totp.now()
    userid = request.userid
    amount = request.amount
    return {
        "otp" : otp,
        "phone" : userid,
        "amount" : amount,
        "message" : "You have 30 seconds before the token expires."}

@app.post("/verify")
def verify_otp(request: VerifyOTPRequest):
    otp = request.otp
    is_valid = totp.verify(otp)
    if not is_valid:
        raise HTTPException(status_code=400, detail="Invalid OTP")
    return {"valid": True}

handler = Mangum(app)