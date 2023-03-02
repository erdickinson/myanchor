from flask import Flask, request

import serial

ser = serial.Serial('/dev/ttyACM0', 9600)

myanchor = Flask(__name__)

@myanchor.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form.get('direction') == 'forward':
            ser.write(b'F')
        elif request.form.get('direction') == 'reverse':
            ser.write(b'R')
        elif request.form.get('direction') == 'off':
            ser.write(b'O')
        elif request.form.get('speed') is not None:
            speed = int(request.form.get('speed'))
            ser.write(str(speed).encode())

    return """
    <html>
        <body>
            <h1>DC Motor Controller</h1>
            <form id="motor-form" method="POST">
                <label>Direction:</label>
                <input type="radio" name="direction" value="forward"> Forward
                <input type="radio" name="direction" value="reverse"> Reverse
                <input type="radio" name="direction" value="off"> Off
                <br>
                <label>Speed:</label>
                <input type="range" min="0" max="510" value="0" class="slider" name="speed">
            </form>
            <script>
                var form = document.getElementById("motor-form");
                var slider = document.querySelector(".slider");
                form.addEventListener("input", function() {
                    var xhttp = new XMLHttpRequest();
                    xhttp.open("POST", "/", true);
                    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
                    xhttp.send(new FormData(form));
                });
            </script>
        </body>
    </html>
    """


@myanchor.route("/send/<int:value>")
def send(value):
    send_to_arduino(str(value))
    return "Sent value {}".format(value)

def send_to_arduino(value):
    ser.write(value.encode())

if __name__ == "__main__":
    myanchor.run(host="0.0.0.0")
