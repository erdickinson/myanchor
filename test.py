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

    # Counter functionality
    counter = int(time.time() % 100)
    send_to_arduino("C{:03d}".format(counter))
    
    return """
    <html>
        <body>
            <h1>DC Motor Controller</h1>
            <form id="motor-form" method="POST">
                <label>Speed:</label>
                <input type="range" min="0" max="255" value="0" class="slider" name="speed">
            </form>
            <div id="counter">Counter: {}</div>
            <script>
                var form = document.getElementById("motor-form");
                var slider = document.querySelector(".slider");
                form.addEventListener("input", function() {
                    var xhttp = new XMLHttpRequest();
                    xhttp.open("POST", "/", true);
                    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
                    xhttp.send(new FormData(form));
                });

                setInterval(function() {{
                    var counterDiv = document.getElementById("counter");
                    counterDiv.innerHTML = "Counter: " + parseInt(counterDiv.innerHTML.split(":")[1].trim()) + 1;
                }}, 1000);
            </script>
        </body>
    </html>
    """.format(counter)


if __name__ == "__main__":
    myanchor.run(host="0.0.0.0")
