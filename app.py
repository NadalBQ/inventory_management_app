from flask import Flask, request, jsonify, render_template
import pandas as pd
from github import Github
import base64
import io


repository_name = "nadalbq/inventory_management_app"
csv_file_path = "./static/csvs/inventory.csv"
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


    # df = pd.read_csv('./static/csvs/inventory.csv', index_col=False)
    
    token = str(data['token'])
    ID = str(data['ID'])
    Location = str(data['location'])
    Amount = str(data['amount'])
    Parent = str(data['parent'])
    Type = str(data['Type']).lower().capitalize()
    g = Github(token)
    repository = g.get_repo(repository_name)
    csv = repository.get_contents(csv_file_path)
    decoded_csv = base64.b64decode(csv.content).decode('utf-8')
    csv_io = io.StringIO(decoded_csv)
    df = pd.read_csv(csv_io)

    data = {'ID': [ID], 'Amount': [Amount], 'Location': [Location], 'Parent': [Parent], 'Type': [Type]}
    new_row = pd.DataFrame(data, index=[len(df)])

    
    print("data", data)
    print("__" + ID + "__")

    df = pd.concat([df, new_row])

    # df.to_csv('./static/csvs/inventory.csv', index=False)

    new_csv_content = df.to_csv(index=False)

    repository.update_file(csv_file_path, "Updating CSV content", new_csv_content, csv.sha)

    return jsonify({'result': "Elemento añadido con éxito"})


    
    
    
    


@app.route('/edit_item', methods=['POST'])

def edit_item():
    data = request.json
    past_df_element, new_df_element = data[0], data[1]
    df.replace(past_df_element, new_df_element)
    df = pd.read_csv('./static/csvs/inventory.csv', index_col=False)

    df.to_csv('./static/csvs/inventory.csv', index=False)

    return "Atributo/s cambiado/s con éxito"
