# DuitNowSMS

- Verify Payment Through SMS
- ID & Password verification for vendors
- Only Registered SME is able to use this service
- For Old People, day to day transaction
- No MORE multiple apps

# Use Case Scenario

- Go to Shop
- Tell what they want
- Read the SMS
- ID & Key
- Approve Payment.

# TechStacks 

- Vendor ask for Phone Number / IC
- Dashboard for Payment
- SMS for Users / Clients

# Tech Requirements

- pyotp
- qrcode
- adasms
- fastapi
  
# flow

- verify via otp, simulate auth, simulating the paynet API
- then show as if money has been deducted
- 24 hour to dispute
- need to draw the mechanism