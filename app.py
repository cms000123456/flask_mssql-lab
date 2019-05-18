#!flask/bin/python
from flask import Flask, request, url_for, redirect, render_template, jsonify
import json
import requests
import urllib
import pyodbc 

app = Flask(__name__)

connection = pyodbc.connect('Driver={SQL Server};Server=.;Database=testdb01;Trusted_Connection=yes')# Creating Cursor  
cursor = connection.cursor()  
cursor.execute("SELECT * FROM testtable")
column_names = [d[0] for d in cursor.description] 
s = "<table id='tab01'><tr>"
for col in column_names:
    s = s + "<th>" + col + "</th>"
s = s + "</tr>"  
for row in cursor:  
    s = s + "<tr>"  
    for x in row:  
        s = s + "<td>" + str(x) + "</td>"  
s = s + "</tr>"  

css = """<head><style>
#tab01 {border-collapse: collapse;width: 100%;}
#tab01 td, #tab01 th {border: 1px solid #ddd;padding: 8px;}
#tab01 tr:nth-child(even){background-color: #f2f2f2;}
#tab01 tr:hover {background-color: #ddd;}
#tab01 th {padding-top: 12px;padding-bottom: 12px;text-align: left;background-color: #4CAF50;color: white;}
</style></head>"""

connection.close()  

@app.route('/')
def wanip():
    response = requests.get('https://httpbin.org/ip')
    return 'Your IP is {0}'.format(response.json()['origin'])

@app.route('/db01')
def db01():
    return "<html>" + css + "<body>" + s + "</body></html>"
    #return jsonify(column_names)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)