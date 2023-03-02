from flask import Flask

import serial

ser = serial.Serial('/dev/ttyACM0', 9600)

myanchor = Flask(__name__)

@myanchor.route("/")
def index():
    return """
    <html>
        <body>
            <h1>DC Motor Controller</h1>
            <input type="range" min="0" max="255" value="0" class="slider" id="myRange" oninput="send()">
            <script>
                function send() {
                    var sliderValue = document.getElementById("myRange").value;
                    var xhttp = new XMLHttpRequest();
                    xhttp.open("GET", "/send/" + sliderValue, true);
                    xhttp.send();
                }
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
