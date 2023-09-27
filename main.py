import time
from datetime import datetime
import sys
import signal
import threading
import json
import microdot
import requests
from microdot_cors import CORS

# EDIT NEXT THREE LINES
LAT = ''
LON = ''
OPENWEATHERMAP_API_KEY = ''

# Setup OpenWeatherMap
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
ONE_HIT_URL = 'https://api.openweathermap.org/data/2.5/onecall?lat=' + LAT + '&lon=' + LON + '&units=metric&appid=' + OPENWEATHERMAP_API_KEY
owm_cache = ''

def get_weather():
    while True:
        global owm_cache
        response = requests.get(ONE_HIT_URL)
        if response.status_code != 200:
            # show the error message
            print("Error in the HTTP request")
        owm_cache = response.content
        time.sleep(900)

def rounder(t):
    return t.replace(second=0, microsecond=0, minute=0)

# define the exit handler
def exit_handler(signal, frame):
    print()
    sys.exit(0)

# Attach a signal handler to catch SIGINT (Ctrl+C) and exit gracefully
signal.signal(signal.SIGINT, exit_handler)

# Start a thread to get the openweathermap data
thread1 = threading.Thread(target=get_weather)
thread1.start()
now = datetime.now()
print (now.strftime("%Y-%m-%d %H:%M:%S") + " - Started background process")
time.sleep(5)

# Setup and run Microdot
app = microdot.Microdot()
cors = CORS(app, allowed_origins=['*'])

@app.route('/')
def index(request):
    return microdot.Response(body=owm_cache, headers={'Access-Control-Allow-Origin': '*'})

@app.route('/short')
def short(request):
    data = json.loads(owm_cache)
    del data['minutely']
    del data['alerts']
    del data['daily']
    return microdot.Response(body=data, headers={'Access-Control-Allow-Origin': '*'})

@app.route('/current')
def current(request):
    data = json.loads(owm_cache)
    return microdot.Response(body=data['current'], headers={'Access-Control-Allow-Origin': '*'})

@app.route('/hour/<hourcount>')
def hour(request, hourcount):
    if 1 <= int(hourcount) <= 47:
        pass
    else:
        found = '{"error":"invalid request"}'
    data = json.loads(owm_cache)
    current_ts = int(rounder(now).timestamp())
    future = current_ts + (int(hourcount) * 3600)
    for i in data['hourly']:
        if i['dt'] == future:
            found = i
    return microdot.Response(body=found, headers={'Access-Control-Allow-Origin': '*'})

app.run(port=8888)
