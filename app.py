from flask import Flask, render_template, request, redirect
from crawler import dorkSearch, map_gen
import crawler
import subprocess
import csv
from datetime import datetime

app = Flask(__name__)

id_value = 10
def get_row_id():
    global id_value
    id_value += 1
    return str(id_value)

headers = ['Select', 'Name', 'Link']

csvReader = csv.DictReader(open("presets.csv"))
presetData = []
tableData = []
for row in csvReader:
    presetData.append(row)    

@app.route('/delete', methods=['POST'])
def delete():
    
    if request.method == 'POST':
        global tableData
        ids = request.form.getlist("row_checkboxes")
        for id in ids:
            for d in tableData:
                if d['id'] == id:
                    tableData.remove(d)

    return render_template(
        'index.html', 
        headers=headers,
        tableData=tableData
    )

@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        global tableData
        global presetData
        ids = request.form.getlist("presets")
        for id in ids:
            for d in presetData:
                if d['id'] == str(id):
                    tableData.append(d)
    return render_template(
        'presets.html',
        headers=headers,
        tableData=tableData,
        presetData=presetData
    )
    
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template(
        'index.html',
        headers=headers,
        tableData=tableData
    )

@app.route('/custom', methods=('GET', 'POST'))
def custom():
    if request.method == 'POST':
        name = request.form['name']
        link = request.form['link']
        tableData.append({'Link': link, 'Name': name, 'id':get_row_id()})

    return render_template(
        'custom.html',
        headers=headers,
        tableData=tableData
    )

@app.route('/presets', methods=('GET', 'POST'))
def presets():
    return render_template(
        'presets.html',
        headers=headers,
        tableData=tableData,
        presetData=presetData
    )

res_table = []
@app.route('/run', methods=('GET', 'POST'))
def run():
    global res_table
    for d in tableData:
        for r in dorkSearch(d['Link']):
            try:
                r['Name'] = d['Name']
                res_table.append(r)
            except:
                res_table.append(r)

    return render_template(
        'run.html',
        headers=['Name', 'Link', 'IP', 'Decription'],
        tableData=res_table
    )
@app.route('/save', methods=('GET', 'POST'))
def save():
    if request.method == 'POST':
        current_datetime = str(datetime.now().strftime("%Y-%m-%d %H-%M-%S"))
        file_name = current_datetime+".csv"
        csv_file = open(file_name, 'w')
        writer = csv.writer(csv_file)
        for r in res_table:
            writer.writerow(r.values())  
            
    return render_template(
        'run.html',
        headers=['Name', 'Link', 'IP', 'Decription'],
        tableData=res_table
    )

@app.route('/map', methods=('GET', 'POST'))
def map():
    if request.method == 'POST':
        #try:
        # Run the mapCrawler.py script using subprocess
        map_gen()
        #except:
        #    print("ERROR: Subprocess failure")
    return redirect(
        '/results'
    )
        
@app.route('/results', methods=('GET', 'POST'))
def results():
    return render_template(
        'run.html',
        headers=['Name', 'Link', 'IP', 'Decription'],
        tableData=res_table
    )
    
@app.route('/about', methods=('GET', 'POST'))
def about():
    return render_template(
        'about.html'
    )
    
if __name__ == '__main__':
    app.run(port=5000)