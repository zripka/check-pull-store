import json
import subprocess

toronto_weather = json.loads(subprocess.check_output('curl "http://api.weatherapi.com/v1/current.json?key=$(cat .config)&q=toronto&aqi=no"', shell=True))

print(toronto_weather)
