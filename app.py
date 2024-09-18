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
    return render_template('home.html')
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

def add_item(edit: bool=False, data=None):
    if not edit:
        data = request.json


    # df = pd.read_csv('./static/csvs/inventory.csv', index_col=False)
    
    token = str(data['token'])
    ID = str(data['ID'])
    Location = str(data['location'])
    Amount = str(data['amount'])
    Parent = str(data['parent'])
    Type = str(data['Type']).lower().capitalize()

    print("add item: " + token, ID, Location, Amount, Parent, Type)

    g = Github(token)
    repository = g.get_repo(repository_name)
    csv = repository.get_contents(csv_file_path)
    decoded_csv = base64.b64decode(csv.content).decode('utf-8')
    csv_io = io.StringIO(decoded_csv)
    df = pd.read_csv(csv_io)

    
    # If given element already exists in the database, only add amount to the stored amount
    try:
        if df.loc[df['ID'].eq(ID) & df['Location'].eq(Location) & df['Parent'].eq(Parent) & df['Type'].eq(Type),"Amount"].iloc[0] != None:
            df.loc[df['ID'].eq(ID) & df['Location'].eq(Location) & df['Parent'].eq(Parent) & df['Type'].eq(Type),"Amount"] = int(df.loc[df['ID'].eq(ID) & df['Location'].eq(Location) & df['Parent'].eq(Parent) & df['Type'].eq(Type),"Amount"].iloc[0]) + int(Amount)
            print("\nThe element was already part of the database so amounts were added together\n")
    
    # If given element does not already exist in the database, append a new line to it.
    except Exception as e:
        print("User tried adding new element to the database")
        data = {'ID': [ID], 'Amount': [Amount], 'Location': [Location], 'Parent': [Parent], 'Type': [Type]}
        new_row = pd.DataFrame(data, index=[len(df)])
        df = pd.concat([df, new_row])

        # df.to_csv('./static/csvs/inventory.csv', index=False)

    updateDataframe(repository, df, csv)
    if not edit:
        return jsonify({'result': "Element added effectively"})
    return None





@app.route('/del_item', methods=['POST'])

def del_item(edit: bool=False, data=None):
    if not edit:
        data = request.json
        
    print("DATA_____________________________", data)
    token = str(data['token'])
    ID = str(data['ID'])
    Location = str(data['location'])
    Amount = str(data['amount'])
    print("delete item: " + token, ID, Location, Amount)

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
    
    # If User provides ID, Location and the exact Amount there is of that element:
    elif int(Amount) == int(df.loc[df['ID'].eq(ID) & df['Location'].eq(Location),"Amount"].iloc[0]):
            try:
                df = df[~(df['ID'].eq(ID) & df['Location'].eq(Location))]
                print(f"Deleted every element with ID={ID} and Location={Location}")
                updateDataframe(repository, df, csv)
                if not edit:
                    return jsonify({'result': "Element deleted effectively."})
                return None
            except:
                print(Exception)
                return jsonify({'result': "The specified ID or Location was not found in the database\nException: {Exception.__name__}"})
  
    
    #If User provides ID, Location and Amount of element:
    else:
        try:
            df.loc[df['ID'].eq(ID) & df['Location'].eq(Location),"Amount"] = int(df.loc[df['ID'].eq(ID) & df['Location'].eq(Location),"Amount"].iloc[0]) - int(Amount)
            print(f"Deleted {Amount} units of element with ID={ID} and Location={Location}")
            updateDataframe(repository, df, csv)
            if not edit:
                return jsonify({'result': "Element amount updated effectively."})
            return None
        except:
            print(Exception)
            return jsonify({'result': "The specified ID or Location was not found in the database\nException: {Exception.__name__}"})
        
        
        
    # df = df[~(df['ID'].eq(ID) & df['Location'].eq(Location) & df['Amount'].eq(Amount))]


@app.route('/edit_item', methods=['POST'])

def edit_item():
    data = request.json

    token = str(data['token'])
    pastID = str(data['pastID'])
    newID = str(data['newID'])
    pastLocation = str(data['pastLocation'])
    newLocation = str(data['newLocation'])
    pastAmount = str(data['pastAmount'])
    newAmount = str(data['newAmount'])
    pastParent = str(data['pastParent'])
    newParent = str(data['newParent'])
    pastType = str(data['pastType']).lower().capitalize()
    newType = str(data['newType']).lower().capitalize()

    deldata = {'token': [token], 'ID': [pastID], 'amount': [pastAmount], 'location': [pastLocation]}
    adddata = {'token': [token], 'ID': [newID], 'amount': [newAmount], 'location': [newLocation], 'parent': [newParent], 'Type': [newType]}

    # Update all values to the new attributes
    a = del_item(True, deldata)
    if a != None:
        add_item(True, adddata)
    else: return "An exception occured while deleting past element"
    
    # Save the csv to github and close the function (both del_item and add_item update that)
    
    # Post the action status on the web.
    return "Atribute/s updated effectively"
