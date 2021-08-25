# Crypto Net Worth Tracker

![](https://img.shields.io/badge/Twilio-SMS%20API-darkgreen?style=for-the-badge)
![](https://img.shields.io/badge/Coinbase-Pricing%20API-blue?style=for-the-badge)
![](https://img.shields.io/badge/Apache%20Airflow-v2.1.2-red?style=for-the-badge)
![](https://img.shields.io/badge/LunchMoney-Integration-yellow?style=for-the-badge)

Track your net worth every day from all of your crypto assets. 
This services automatically integrates with LunchMoney, a budgeting and finance tool.

<img src="https://user-images.githubusercontent.com/13546028/130805020-1c6a0df7-b336-496a-955e-a50eda6ad4a9.png" width="350">

### Required Airflow Variables

Twilio

```
TWILIO_ACCOUNT_SID
TWILIO_AUTH_TOKEN
TWILIO_NUMBER_TO
TWILIO_NUMBER_FROM
```

LunchMoney

```
LUNCH_MONEY_TOKEN
```

### Initialize AirFlow

---

`docker-compose up airflow-init`

### Start

---

`docker-compose up`
