# from . import app    # For application discovery by the 'flask' command. 
import telemeter
from string import Template
import os
from sys import exit


from flask import Flask  # Import the Flask class
app = Flask(__name__)

TEMPLATE = """{
        "period_start": "$start",
        "period_end": "$end",
        "product": "$product",
        "usage_peak": $peak,
        "usage_offpeak": $offpeak,
        "total_usage": $total
    }"""

TELENET_USERNAME = os.environ.get("TELENET_USERNAME")
TELENET_PASSWORD = os.environ.get("TELENET_PASSWORD")

if TELENET_USERNAME is None:
    print("Missing configuration: ENV TELENET_USERNAME")

if TELENET_PASSWORD is None:
    print("Missing configuration: ENV TELENET_PASSWORD")

if TELENET_USERNAME is None or TELENET_PASSWORD is None:
    exit()

telenet_session = telemeter.TelenetSession()
telenet_session.login(TELENET_USERNAME, TELENET_PASSWORD)


@app.route("/")
def current_period():
    print('GET current_period()')
    my_telemeter = telenet_session.telemeter()  

    current_period_start = my_telemeter.period_start.strftime("%d/%m/%Y")
    current_period_end = my_telemeter.period_end.strftime("%d/%m/%Y")
    current_period_product = my_telemeter.products[0].product_type
    current_period_usage_peak = my_telemeter.products[0].peak_usage
    current_period_usage_offpeak = my_telemeter.products[0].offpeak_usage
    current_period_usage_total = my_telemeter.products[0].total_usage
    
    return Template(TEMPLATE).substitute(
        start=current_period_start,
        end=current_period_end,
        product=current_period_product,
        peak=current_period_usage_peak,
        offpeak=current_period_usage_offpeak,
        total=current_period_usage_total
    )