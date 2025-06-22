import requests
from requests.auth import HTTPBasicAuth

# ==== CONFIGURATION ====
RAZORPAY_KEY_ID = "YOUR-TEST-KEY"
RAZORPAY_KEY_SECRET = "YOUR-SECRET-KEY"
auth = HTTPBasicAuth(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET)

BASE_URL = "https://api.razorpay.com/v1"

def fetch_subscriptions():
    url = f"{BASE_URL}/subscriptions"
    response = requests.get(url, auth=auth)
    return response.json() if response.status_code == 200 else {"items": []}

def fetch_payments():
    url = f"{BASE_URL}/payments"
    response = requests.get(url, auth=auth)
    return response.json() if response.status_code == 200 else {"items": []}

def fetch_plan(plan_id):
    url = f"{BASE_URL}/plans/{plan_id}"
    response = requests.get(url, auth=auth)
    return response.json() if response.status_code == 200 else None

def calculate_metrics(subscriptions, payments):
    mrr = 0
    active_customers = set()
    churned_customers = set()

    for sub in subscriptions.get('items', []):
        status = sub.get('status')
        customer_id = sub.get('customer_id')
        plan_id = sub.get('plan_id')

        # Fetch plan data manually
        plan = fetch_plan(plan_id)
        if not plan or 'item' not in plan:
            print(f"⚠️ Skipping subscription due to missing plan: {sub.get('id')}")
            continue

        amount = plan['item'].get('amount', 0) / 100
        interval = plan.get('period', 'monthly')

        if status == 'active' and interval == 'monthly':
            mrr += amount
            active_customers.add(customer_id)
        elif status == 'cancelled':
            churned_customers.add(customer_id)

    total_revenue = sum(p['amount'] / 100 for p in payments.get('items', []) if p['status'] == 'captured')
    cltv = total_revenue / len(active_customers) if active_customers else 0
    churn_rate = (len(churned_customers) / (len(active_customers) + len(churned_customers))) * 100 if (active_customers or churned_customers) else 0

    return {
        "MRR": round(mrr, 2),
        "Active Customers": len(active_customers),
        "Churned Customers": len(churned_customers),
        "Total Revenue": round(total_revenue, 2),
        "CLTV": round(cltv, 2),
        "Churn Rate (%)": round(churn_rate, 2)
    }

def main():
    print("Fetching data from Razorpay...\n")
    subscriptions = fetch_subscriptions()
    payments = fetch_payments()

    metrics = calculate_metrics(subscriptions, payments)

    print("\n📊 SaaS Metrics Dashboard (Razorpay)\n" + "-" * 40)
    for k, v in metrics.items():
        print(f"{k}: ₹{v}" if isinstance(v, float) else f"{k}: {v}")
    print("-" * 40)

if __name__ == "__main__":
    main()
