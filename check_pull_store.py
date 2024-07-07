import json
import subprocess
import pprint
import sqlite3

toronto_weather = json.loads(subprocess.check_output('curl "http://api.weatherapi.com/v1/current.json?key=$(cat .config)&q=toronto&aqi=no"', shell=True))

try:
    connection = sqlite3.connect("file:temperature.db?mode=rw", uri=True)
    cursor = connection.cursor()
except sqlite3.OperationalError:
    connection = sqlite3.connect("temperature.db")
    cursor = connection.cursor()
    cursor.execute("""
        create table temperature (
            record_id integer, 
            last_updated text, 
            temperature_c real, 
            primary key (record_id), 
            unique (last_updated)
        );
    """)
    connection.commit()

query = """
    insert or ignore into temperature (last_updated, temperature_c)
    values
    ('{}', '{}')
"""
cursor.execute(query.format(toronto_weather['current']['last_updated'], toronto_weather['current']['temp_c']))

connection.commit()

subprocess.run('sqlite3 -column -header temperature.db "select * from temperature;"', shell=True)

cursor.close()
connection.close()
