from flask import Flask, render_template, request
import serial

app = Flask(__name__)
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
ser.reset_input_buffer()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        number = request.form['number']
        ser.write(number.encode('utf-8'))
        arduino_response = ser.read().decode('utf-8')
        print("Received number from Arduino:", arduino_response)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

    
    <!DOCTYPE html>
<html>
<head>
    <title>Send Number to Arduino</title>
</head>
<body>
    <h1>Send Number to Arduino</h1>
    <form method="POST">
        <label for="number">Enter a number:</label>
        <input type="text" id="number" name="number">
        <input type="submit" value="Submit">
    </form>
</body>
</html>
