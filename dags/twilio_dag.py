from datetime import timedelta
from collections import defaultdict

import requests
import aiohttp
import json
import asyncio

from twilio.rest import Client

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators; we need this to operate!
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from airflow.models import Variable


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


def calculate_net_worth(**context):
    # Get all crypto assets from LunchMoney
    all_crypto_assets = requests.get(
        "https://dev.lunchmoney.app/v1/crypto",
        headers={"Authorization": Variable.get("LUNCH_MONEY_TOKEN")},
    ).json()["crypto"]

    # Get all other managed assets from LunchMoney
    all_other_assets = requests.get(
        "https://dev.lunchmoney.app/v1/assets",
        headers={"Authorization": Variable.get("LUNCH_MONEY_TOKEN")},
    ).json()["assets"]

    crypto_balances = defaultdict(list)
    urls = []
    networth = 0

    # Build list of all Coinbase API URLs
    for asset in all_crypto_assets:
        balance = asset["balance"]
        currency = asset["currency"]

        crypto_balances[currency.upper()] = {"balance": balance}

        urls.append(
            "https://api.coinbase.com/v2/exchange-rates?currency={}".format(currency)
        )

    # Asynchrously make requests to all exchange rate urls
    async def get(url, session):
        try:
            async with session.get(url=url) as response:
                resp = await response.read()

                coinbase_response = json.loads(resp)
                exchange_rate = coinbase_response["data"]["rates"]["USD"]
                currency = coinbase_response["data"]["currency"]

                crypto_balances[currency]["exchange_rate"] = exchange_rate

        except Exception as e:
            print("Unable to get url {} due to {}.".format(url, e.__class__))

    async def main(urls):
        async with aiohttp.ClientSession() as session:
            await asyncio.gather(*[get(url, session) for url in urls])

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(urls))

    # Add crypto asset balances to networth
    for token in crypto_balances:
        token_info = crypto_balances[token]
        balance = float(token_info["balance"])
        exchange_rate = float(token_info["exchange_rate"])

        print(
            f"""
        -----------
        Token: {token}
        Balance: {balance}
        {token}/USD: ${exchange_rate}
        Total: ${balance * exchange_rate}
        -----------
        """
        )
        networth += balance * exchange_rate

    # Add other managed assets to networth
    for asset in all_other_assets:
        asset_type = asset["type_name"]
        balance = float(asset["balance"])

        if asset_type == "loan":
            networth -= balance
        else:
            networth += balance

    print("Net Worth: {}".format(int(networth)))

    context["ti"].xcom_push(key="net_worth", value=int(networth))


def send_message(**context):
    net_worth = context["ti"].xcom_pull(task_ids="networth_calculate", key="net_worth")

    account_sid = Variable.get("TWILIO_ACCOUNT_SID")
    auth_token = Variable.get("TWILIO_AUTH_TOKEN")
    client = Client(account_sid, auth_token)

    net_worth = context["ti"].xcom_pull(
        key="net_worth", task_ids=["networth_calculate"]
    )

    fetched_message = "Hey! Today, your net worth is ${val:,}".format(val=net_worth[0])

    client.messages.create(
        body=fetched_message,
        from_=Variable.get("TWILIO_NUMBER_FROM"),
        to=Variable.get("TWILIO_NUMBER_TO"),
    )

    print("Sent Message!")


with DAG(
    "net_worth_notifier",
    default_args=default_args,
    description="A DAG to send daily crypto net worth notifications",
    schedule_interval="@daily",
    start_date=days_ago(2),
) as dag:

    networth_calculator = PythonOperator(
        task_id="networth_calculate",
        python_callable=calculate_net_worth,
        provide_context=True,
    )

    sms_sender = PythonOperator(
        task_id="sms_sender",
        python_callable=send_message,
        provide_context=True,
    )

    networth_calculator >> sms_sender
