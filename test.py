from flask import Flask, request
import serial
import time

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

def send_to_arduino(value):
    checksum = sum(map(ord, value)) % 256
    message = "{}{:02X}\n".format(value, checksum)
    ser.write(message.encode())
    print("Sent value: {}".format(value))

myanchor = Flask(__name__)

@myanchor.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form.get('speed') is not None:
            speed = int(request.form.get('speed'))
            send_to_arduino("S{:03d}".format(speed))
            print("Speed value:", speed)

    return """
    <html>
        <body>
            <h1>DC Motor Controller</h1>
            <form id="motor-form" method="POST">
                <label>Speed:</label>
                <input type="range" min="0" max="255" value="0" class="slider" name="speed">
                <br>
                <span id="speed-value">0</span>
            </form>
            <script>
                var form = document.getElementById("motor-form");
                var slider = document.querySelector(".slider");
                var speedValue = document.getElementById("speed-value");
                form.addEventListener("input", function() {
                    var xhttp = new XMLHttpRequest();
                    xhttp.open("POST", "/", true);
                    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
                    xhttp.send(new FormData(form));
                    speedValue.textContent = slider.value;
                });
            </script>
        </body>
    </html>
    """

if __name__ == "__main__":
    myanchor.run(host="0.0.0.0")
