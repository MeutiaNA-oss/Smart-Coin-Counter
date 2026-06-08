from flask import Flask, render_template, request, redirect
import serial
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HOST = "0.0.0.0"
PORT = 5000

app = Flask(__name__)

# CONNECT ESP32
#esp32 = serial.Serial('COM3', 9600)

# TOTAL COIN PER JENIS
coin_100 = 0
coin_500 = 0
coin_1000 = 0

# TOTAL UANG
total_money = 0
total_coin = 0
# MODE COIN AKTIF
coin_value = 100

# TARGET
target_money = 0

target_status = target_money - total_money
if target_status < 0:
    target_status = 0
    
# DASHBOARD
@app.route("/")
def home():

    global coin_100
    global coin_500
    global coin_1000
    global total_money

    global coin_value

    # CEK DATA ESP32
    if esp32.in_waiting: 

        data = esp32.readline().decode().strip()

        # JIKA ADA COIN
        if data == "COIN":

            # MODE 100
            ##GIMANA DARI WEB MEMBERI SINYAL UNTUK MEMBEDAKAN PENAMBAHAN 100 500 1000??
            if coin_value == 100:

                coin_100 += 1

            # MODE 500
            elif coin_value == 500:

                coin_500 += 1

            # MODE 1000
            elif coin_value == 1000:

                coin_1000 += 1

            # TOTAL UANG
            total_money += coin_value

            print("Coin detected!")


    return render_template(

        "index.html",

        coin_100=coin_100,
        coin_500=coin_500,
        coin_1000=coin_1000,

        total_coin=total_coin,
        total_money=total_money,

        coin_value=coin_value,
        target_money=target_money,
        target_status=target_status
    )
# SET TARGET
@app.route('/set_target', methods=['POST'])
def set_target():

    global target_money

    target_money = int(request.form['target_money'])

    return redirect('/')

# MODE COIN
@app.route('/set_coin/<int:value>')
def set_coin(value):

    global coin_value

    coin_value = value

    return redirect('/')

# RESET TARGET
@app.route('/reset_target')
def reset_target():

    global target_money

    target_money = 0

    return redirect('/')

# RESET ALL
@app.route('/reset_all')
def reset_all():

    global coin_100
    global coin_500
    global coin_1000

    global total_coin
    global total_money

    coin_100 = 0
    coin_500 = 0
    coin_1000 = 0

    total_coin = 0
    total_money = 0

    return redirect('/')

app.run(debug=True)
