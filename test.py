from flask import Flask, request
import serial
import time

ser = serial.Serial('/dev/ttyACM0', 9600,timeout=1)

def send_to_arduino(speed):
    speed_str = "S{:03d}".format(speed) # convert the speed to a 3-digit string
    checksum = sum(map(ord, speed_str)) % 256
    message = "{}{:02X}\n".format(speed_str, checksum)
    ser.write(message.encode())
    print("Sent value: {}".format(speed_str))


myanchor = Flask(__name__)

@myanchor.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form.get('speed') is not None:
            speed = int(request.form.get('speed'))
            send_to_arduino("S{:03d}".format(speed))
            print("Received speed value: {}".format(speed))

    return """
    <html>
        <body>
            <h1>DC Motor Controller</h1>
            <form id="motor-form" method="POST">
                <label>Speed:</label>
                <input type="range" min="0" max="255" value="0" class="slider" name="speed">
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


if __name__ == "__main__":
    myanchor.run(host="0.0.0.0")
