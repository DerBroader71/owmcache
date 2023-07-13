import time
from datetime import datetime
import sys
import signal
import threading
import microdot
import requests

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

@app.route('/')
def index(request):
    return owm_cache

app.run(port=8080)
