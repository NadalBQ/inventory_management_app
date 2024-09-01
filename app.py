from flask import Flask, request, jsonify, render_template
import pandas as pd
# from typing import List, Dict

# i am trying
app = Flask(__name__, static_url_path='/static')

@app.route('/add_item', methods=['POST'])

def add_item():
    data = request.json
    pais = str(data['pais'])
    
    fuma = str(data['fuma']).lower()
    print("data", data)
    print("pais", pais)
    print("fuma", fuma)
    return jsonify({'result': data})
    
    
    
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
