# Razorpay SaaS Metrics Dashboard 📊

A Python toolkit for simulating SaaS subscriptions and tracking business metrics using Razorpay API in test mode.

## Features

- Create test customers and subscription plans
- Simulate subscription payments via Razorpay dashboard
- Track MRR, active customers, and total revenue
- Calculate churn rate and customer lifetime value

## Installation

```bash
git clone https://github.com/0xarun/razorpay-saas-metrics-dashboard.git
cd razorpay-saas-metrics-dashboard
pip install requests
```

## Setup

Add your Razorpay test credentials to both Python files:

```python
RAZORPAY_KEY_ID = "your_test_key_id"
RAZORPAY_KEY_SECRET = "your_test_key_secret"
```

## Usage

1. **Create subscriptions**:
   ```bash
   python simulate-plans-razorpay.py
   ```

2. **Capture payment manually**:
   - Go to Razorpay Test Dashboard → Subscriptions
   - See Created Subscriptions
   - Click "Start Subscription" on the created subscription

3. **View metrics**:
   ```bash
   python python-razorpay.py
   ```

## Sample Output

```
📊 SaaS Metrics Dashboard (Razorpay)
----------------------------------------
MRR: ₹99.0
Active Customers: 1
Churned Customers: 0
Total Revenue: ₹99.0
CLTV: ₹99.0
Churn Rate (%): 0.0
----------------------------------------
```
