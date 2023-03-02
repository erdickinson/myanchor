from flask import Flask, request
import serial

ser = serial.Serial('/dev/ttyACM1', 9600)

def send_to_arduino(value):
    checksum = sum(map(ord, value)) % 256
    message = "{}{:02X}\n".format(value, checksum)
    ser.write(message.encode())

myanchor = Flask(__name__)

@myanchor.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form.get('direction') == 'forward':
            send_to_arduino("F00")
        elif request.form.get('direction') == 'reverse':
            send_to_arduino("R00")
        elif request.form.get('direction') == 'off':
            send_to_arduino("O00")
        elif request.form.get('speed') is not None:
            speed = int(request.form.get('speed'))
            send_to_arduino("S{:03d}".format(speed))

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
