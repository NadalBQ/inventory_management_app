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
@app.route('/theProject')
def theProject():
    return render_template('theProject.html')


@app.route('/nadal')
def nadal():
    return render_template('nadal.html')



def updateDataframe(repository, df, csv):
    new_csv_content = df.to_csv(index=False)
    repository.update_file(csv_file_path, "Updating CSV content", new_csv_content, csv.sha)

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

    updateDataframe(repository, df, csv)
    return jsonify({'result': "Element added effectively"})





@app.route('/del_item', methods=['POST'])

def del_item():
    data = request.json


    # df = pd.read_csv('./static/csvs/inventory.csv', index_col=False)
    
    token = str(data['token'])
    ID = str(data['ID'])
    Location = str(data['location'])
    Amount = str(data['amount'])
    

    g = Github(token)
    repository = g.get_repo(repository_name)
    csv = repository.get_contents(csv_file_path)
    decoded_csv = base64.b64decode(csv.content).decode('utf-8')
    csv_io = io.StringIO(decoded_csv)
    df = pd.read_csv(csv_io)

    # data = {'ID': [ID], 'Amount': [Amount], 'Location': [Location]}

    # If User does not provide an ID:
    if not ID:
        print("Tried to delete element without ID reference")
        return jsonify({'result': "No ID was received, could not delete element."})
    
    # If User provides ID but no further information:
    if not Location:
        if not Amount:
            try:
                df = df[~(df['ID'].eq(ID))]
                print(f"Deleted every element with ID={ID}")
                updateDataframe(repository, df, csv)
                return jsonify({'result': "Element deleted effectively."})
            except:
                print(Exception)
                return jsonify({'result': "The specified ID was not found in the database\nException: {Exception.__name__}"})
        
        
        # If User provides ID and The exact amount there is of that element:
        elif int(Amount) == df.loc[df['ID'].eq(ID),"Amount"]:
            try:
                df = df[~(df['ID'].eq(ID))]
                print(f"Deleted every element with ID={ID}")
                updateDataframe(repository, df, csv)
                return jsonify({'result': "Element deleted effectively."})
            except:
                print(Exception)
                return jsonify({'result': "The specified ID was not found in the database\nException: {Exception.__name__}"})
        # .loc[row_indexer,col_indexer] = value
        
        
        # If the User provides ID and the amount to delete of that element:
        try:
            df.loc[df['ID'].eq(ID),"Amount"] -= int(Amount)
            print(f"Deleted {Amount} units of element with ID={ID}")
            updateDataframe(repository, df, csv)
            return jsonify({'result': "Element amount updated effectively."})
        except:
            print(Exception)
            return jsonify({'result': "The specified ID was not found in the database\nException: {Exception.__name__}"})
    # Finish these lines!!!
    # check if df.loc[df['ID'].eq(ID),"Amount"] is an int or convertible to int
    
    
    
    # If User provides ID and Location of element:
    elif not Amount:
        try:
            df = df[~(df['ID'].eq(ID) & df['Location'].eq(Location))]
            print(f"Deleted every element with ID={ID} and Location={Location}")
            updateDataframe(repository, df, csv)
            return jsonify({'result': "Element deleted effectively."})
        except:
            print(Exception)
            return jsonify({'result': "The specified ID or Location was not found in the database\nException: {Exception.__name__}"})
    
    # If User provides ID, Location and the exact Amount there is of that element:
    elif int(Amount) == df.loc[df['ID'].eq(ID) & df['Location'].eq(Location),"Amount"]:
            try:
                df = df[~(df['ID'].eq(ID) & df['Location'].eq(Location))]
                print(f"Deleted every element with ID={ID} and Location={Location}")
                updateDataframe(repository, df, csv)
                return jsonify({'result': "Element deleted effectively."})
            except:
                print(Exception)
                return jsonify({'result': "The specified ID or Location was not found in the database\nException: {Exception.__name__}"})
  
    
    #If User provides ID, Location and Amount of element:
    else:
        try:
            df.loc[df['ID'].eq(ID) & df['Location'].eq(Location),"Amount"] -= int(Amount)
            print(f"Deleted {Amount} units of element with ID={ID} and Location={Location}")
            updateDataframe(repository, df, csv)
            return jsonify({'result': "Element amount updated effectively."})
        except:
            print(Exception)
            return jsonify({'result': "The specified ID or Location was not found in the database\nException: {Exception.__name__}"})
        
        
        
    # df = df[~(df['ID'].eq(ID) & df['Location'].eq(Location) & df['Amount'].eq(Amount))]


    
    
    
    


@app.route('/edit_item', methods=['POST'])

def edit_item():
    data = request.json
    past_df_element, new_df_element = data[0], data[1]
    df.replace(past_df_element, new_df_element)
    df = pd.read_csv('./static/csvs/inventory.csv', index_col=False)

    df.to_csv('./static/csvs/inventory.csv', index=False)

    return "Atributo/s cambiado/s con éxito"
