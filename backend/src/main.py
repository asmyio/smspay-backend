from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pyotp

app = FastAPI()
secret_key = pyotp.random_base32()
totp = pyotp.TOTP(secret_key)
class VerifyOTPRequest(BaseModel):
    otp: str

class UserIDRequest(BaseModel):
    userid: str

@app.get("/health")
def get_health():
    return {"health": "ok"}

@app.post("/otp")
def get_otp(request: UserIDRequest):
    otp = totp.now()
    userid = request.userid
    return {
        "otp" : otp,
        "phone" : userid,
        "message" : "You have 30 seconds before the token expires."}

@app.post("/verify")
def verify_otp(request: VerifyOTPRequest):
    otp = request.otp
    is_valid = totp.verify(otp)
    if not is_valid:
        raise HTTPException(status_code=400, detail="Invalid OTP")
    return {"valid": True}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)