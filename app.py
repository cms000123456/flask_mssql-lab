#!flask/bin/python
from flask import Flask, request, url_for, redirect, render_template, jsonify
import json
import requests
import urllib
import pyodbc 

app = Flask(__name__)

class data:
    def __init__(self, name, number, id):
        self.name = name
        self.number = number

def listdb():
    connection = pyodbc.connect('Driver={SQL Server};Server=.;Database=testdb01;Trusted_Connection=yes')
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
    connection.close()
    return str("<html>" + css + "<body>" + s )

def inserttodb(name,number):
    connection = pyodbc.connect('Driver={SQL Server};Server=.;Database=testdb01;Trusted_Connection=yes')
    cursor = connection.cursor()  
    cursor.execute("insert into testtable(name, number) values (?, ?)", name, number)
    connection.commit()	
    connection.close()
    return (name,number)	
	
def updatedb(id,name,number):
    connection = pyodbc.connect('Driver={SQL Server};Server=.;Database=testdb01;Trusted_Connection=yes')
    cursor = connection.cursor()
    query = "UPDATE testtable SET " 
    if (name):
        query = query + "name = '{}'".format(name)
        if (number):
            query = query + ","
    if (number):
        query = query + "number = '{}'".format(number)    
    query = query + " WHERE ID = {}".format(id)
    cursor.execute(query)
    connection.commit()
    connection.close()
    return (query)
	
css = """<head><style>
#tab01 {border-collapse: collapse;width: 100%;}
#tab01 td, #tab01 th {border: 1px solid #ddd;padding: 8px;}
#tab01 tr:nth-child(odd){background-color: #f2f2f2;}
#tab01 tr:hover {background-color: #ddd;}
#tab01 th {padding-top: 12px;padding-bottom: 12px;text-align: left;background-color: #d580ff;color: white;}
</style></head>"""

#connection.close()  

@app.route('/')
def wanip():
    response = requests.get('https://httpbin.org/ip')
    return 'Your IP is {0}'.format(response.json()['origin'])

@app.route('/list')
def list():
    list = listdb()  + "</body></html>"
    return list

@app.route('/insert', methods=['GET', 'POST'])
def insert():
    if request.method == 'GET':
        out = listdb()
        out = out + render_template('insert.html') + "</body></html>"
        return out
    if request.method == 'POST':		
        result = inserttodb(name=request.form["name"],number=request.form["number"])
        out = listdb()
        out = out + render_template('insert.html') + "</body></html>"
        return out

@app.route('/update', methods=['GET','POST'])
def update():
    if request.method == 'GET':
        out = listdb()
        out = out + render_template('update.html') + "</body></html>"
        return out
    if request.method == 'POST':
        result = updatedb(id=request.form["id"],name=request.form["name"],number=request.form["number"])
        out = listdb()
        out = out + render_template('update.html') + "</body></html>"
        #return result
        return out
 
@app.route('/insupd',methods=['GET','POST'])
def insupd():
    pass #insupd.html
 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)
