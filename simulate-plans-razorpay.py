import requests
from requests.auth import HTTPBasicAuth

RAZORPAY_KEY_ID = "rzp_test_0sG9GaeyZZl8OV"
RAZORPAY_KEY_SECRET = "pl3911fUchI0Xdm3394KCbqf"

auth = HTTPBasicAuth(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET)

import time

def create_customer():
    timestamp = int(time.time())  # Use current time as part of email
    data = {
        "name": "Test Founder",
        "email": f"founder{timestamp}@example.com",  # Unique email
        "contact": f"98765{timestamp % 100000}"      # Unique contact number
    }
    res = requests.post("https://api.razorpay.com/v1/customers", auth=auth, data=data)
    response_json = res.json()

    if 'id' in response_json:
        return response_json['id']
    else:
        print("❌ Failed to create customer.")
        print("Response from Razorpay:", response_json)
        exit()

def create_plan():
    data = {
        "period": "monthly",
        "interval": 1,
        "item[name]": "SaaS Pro Plan",
        "item[amount]": 9900,
        "item[currency]": "INR"
    }
    res = requests.post("https://api.razorpay.com/v1/plans", auth=auth, data=data)
    return res.json()["id"]

def create_subscription(customer_id, plan_id):
    data = {
        "plan_id": plan_id,
        "customer_notify": 1,
        "customer_id": customer_id,
        "total_count": 12  # Billing cycle count (e.g., 12 months)
    }
    res = requests.post("https://api.razorpay.com/v1/subscriptions", auth=auth, data=data)
    return res.json()


def fetch_metrics():
    subs = requests.get("https://api.razorpay.com/v1/subscriptions", auth=auth).json()
    pays = requests.get("https://api.razorpay.com/v1/payments", auth=auth).json()

    mrr, active = 0, 0
    for sub in subs['items']:
        if sub['status'] == 'active':
            try:
                amount = sub['plan']['item']['amount'] / 100
                mrr += amount
                active += 1
            except KeyError:
                print(f"⚠️ Skipping a subscription due to missing plan data: {sub['id']}")
                continue

    revenue = sum

def main():
    print("Setting up Razorpay Test Subscription...\n")

    customer_id = create_customer()
    print(f"✅ Created Customer: {customer_id}")

    plan_id = create_plan()
    print(f"✅ Created Plan: {plan_id}")

    subscription = create_subscription(customer_id, plan_id)

    # Safe access to response
    if 'id' in subscription:
        print(f"✔ Created Subscription: {subscription['id']}")
        fetch_metrics()  # Optional: Only if you want to show dashboard
    else:
        print("❌ Failed to create subscription.")
        print("Response from Razorpay:", subscription)

main()
