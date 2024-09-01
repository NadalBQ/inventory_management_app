from flask import Flask, request, jsonify, render_template
import pandas as pd
# from typing import List, Dict


app = Flask(__name__, static_url_path='/static')
# Web addresses


@app.route('/')
def index():
    return render_template('index.html')
@app.route('/home')
def home():
    return render_template('index.html')
@app.route('/explain')
def explain():
    return render_template('explain.html')
@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')
@app.route('/filesUsed')
def filesUsed():
    return render_template('filesUsed.html')
@app.route('/theProject')
def theProject():
    return render_template('theProject.html')

@app.route('/isabelle')
def isabelle():
    return render_template('isabelle.html')
@app.route('/nadal')
def nadal():
    return render_template('nadal.html')
@app.route('/fernanda')
def fernanda():
    return render_template('fernanda.html')
@app.route('/carla')
def carla():
    return render_template('carla.html')
@app.route('/michele')
def michele():
    return render_template('michele.html')




@app.route('/add_item', methods=['POST'])

def add_item():
    data = request.json
    df = pd.read_csv('./static/csvs/inventory.csv', index_col=False)
    
    
    pais = str(data['pais'])
    fuma = str(data['fuma'])


    data = {'Age': [pais], 'Location': [fuma]}
    new_row = pd.DataFrame(data, index=[len(df)])

    
    print("data", data)
    print("pais", pais)
    print("fuma", fuma)

    df = pd.concat([df, new_row])

    df.to_csv('./static/csvs/inventory.csv', index=False)

    return jsonify({'result': "Elemento añadido con éxito"})


    
    
    
    
'''
def add_item():

    data = request.json
    
    df = pd.read_csv('./static/csvs/inventory.csv', index_col=False)

    # data = {'Age': ['edad'], 'Location': ['lugar'], 'Name': ['nombre']}
    # new_row = pd.DataFrame({'Age': ['edad'], 'Location': ['lugar'], 'Name': ['nombre']}, index=[len(df)],)
    new_row = pd.DataFrame(data, index=[len(df)])

    df = pd.concat([df, new_row])

    df.to_csv('./static/csvs/inventory.csv', index=False)

    return "Elemento añadido con éxito"
'''

@app.route('/edit_item', methods=['POST'])

def edit_item():
    data = request.json
    past_df_element, new_df_element = data[0], data[1]
    df.replace(past_df_element, new_df_element)
    df = pd.read_csv('./static/csvs/inventory.csv', index_col=False)

    df.to_csv('./static/csvs/inventory.csv', index=False)

    return "Atributo/s cambiado/s con éxito"
