# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask,render_template, send_file
from flask import request
import db
import io
import csv

# Flask constructor takes the name of 
# current module (__name__) as argument.
app = Flask(__name__)
 
# The route() function of the Flask class is a decorator, 
# which tells the application which URL should call 
# the associated function.
@app.route('/')
# ‘/’ URL is bound with hello_world() function.
def hello_world():
    return 'Hello World'

@app.route('/savetemp')
def save_temp():
    temp = request.args.get('temp')
    deviceID = request.args.get('id')
    if temp and deviceID: 
        db.saveTemp(float(temp),int(deviceID))
        return ('>:3 Successful entry',200)
    else:
        print("no data in request")
        return ('>:3 no data in request',400)

@app.route('/app')
def viewer(window=50):
    data = db.getTemps('0')
    if len(data)>window:
        data = data[-window:]
    labels = [item[1] for item in data]
    values = [item[2] for item in data]
    return render_template('graph.html', labels=labels, values=values)

@app.route('/download')
def downloadData(deviceID=0):
    data = db.getTemps(deviceID)
    proxy = io.StringIO()
    
    writer = csv.writer(proxy)
    writer.writerow(['ID','Timestamp','Temperature (C)'])
    for row in data:
        writer.writerow(row)
    
    # Creating the byteIO object from the StringIO Object
    mem = io.BytesIO()
    mem.write(proxy.getvalue().encode())
    # seeking was necessary. Python 3.5.2, Flask 0.12.2
    mem.seek(0)
    proxy.close()

    return send_file(
        mem,
        as_attachment=True,
        download_name='data.csv',
        mimetype='text/csv'
    )


# main driver function
if __name__ == '__main__':
 
    # run() method of Flask class runs the application 
    # on the local development server.
    app.run(host='0.0.0.0')

