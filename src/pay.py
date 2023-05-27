from fastapi import FastAPI
import pyotp
import time

app = FastAPI()

# Generate a secret key
secret_key = pyotp.random_base32()

# Create a TOTP object
totp = pyotp.TOTP(secret_key)


@app.get("/otp")
def get_otp():
    # Get the current TOTP code
    otp = totp.now()
    return {"otp": otp}


@app.get("/verify/{otp}")
def verify_otp(otp: str):
    # Verify the TOTP code
    is_valid = totp.verify(otp)
    return {"valid": is_valid}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
