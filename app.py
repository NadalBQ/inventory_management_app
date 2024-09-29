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

# Utility function to update the CSV file in the GitHub repository
def updateDataframe(repository, df, csv):
    new_csv_content = df.to_csv(index=False)
    repository.update_file(csv_file_path, "Updating CSV content", new_csv_content, csv.sha)

# Add Item
@app.route('/add_item', methods=['POST'])
def add_item(edit: bool=False, adddata=None):
    if not edit:
        adddata = request.json

    token = str(adddata['token'])
    ID = str(adddata['ID'])
    Location = str(adddata['location'])
    Amount = str(adddata['amount'])
    Parent = str(adddata['parent'])
    Type = str(adddata['Type']).lower().capitalize()

    print(f"Adding item: Token={token}, ID={ID}, Location={Location}, Amount={Amount}, Parent={Parent}, Type={Type}")

    g = Github(token)
    repository = g.get_repo(repository_name)
    csv = repository.get_contents(csv_file_path)
    decoded_csv = base64.b64decode(csv.content).decode('utf-8')
    csv_io = io.StringIO(decoded_csv)
    df = pd.read_csv(csv_io)

    # Check if the item already exists
    try:
        existing_amount = df.loc[df['ID'].eq(ID) & df['Location'].eq(Location) & df['Parent'].eq(Parent) & df['Type'].eq(Type), "Amount"].iloc[0]
        df.loc[df['ID'].eq(ID) & df['Location'].eq(Location) & df['Parent'].eq(Parent) & df['Type'].eq(Type), "Amount"] = int(existing_amount) + int(Amount)
        print("\nItem already exists, amounts were added together\n")
    except:
        # Add new item
        new_row = pd.DataFrame({
            'ID': [ID],
            'Amount': [Amount],
            'Location': [Location],
            'Parent': [Parent],
            'Type': [Type]
        })
        df = pd.concat([df, new_row])
        print("Added a new item to the database")

    updateDataframe(repository, df, csv)
    
    if not edit:
        return jsonify({'result': "Element added effectively"})
    return None

# Delete Item
@app.route('/del_item', methods=['POST'])
def del_item(edit: bool=False, deldata=None):
    if not edit:
        deldata = request.json

    token = str(deldata['token'])
    ID = str(deldata['ID'])
    Location = str(deldata['location'])
    Amount = str(deldata['amount'])

    print("delete item: " + token, ID, Location, Amount)

    g = Github(token)
    repository = g.get_repo(repository_name)
    csv = repository.get_contents(csv_file_path)
    decoded_csv = base64.b64decode(csv.content).decode('utf-8')
    csv_io = io.StringIO(decoded_csv)
    df = pd.read_csv(csv_io)

    # If User does not provide an ID:
    if not ID:
        print("Tried to delete element without ID reference")
        return jsonify({'result': "No ID was received, could not delete element."})

    # Filter the DataFrame to get matching rows
    matching_rows = df.loc[df['ID'].eq(ID) & df['Location'].eq(Location)]

    # Check if there are any matching rows before proceeding
    if matching_rows.empty:
        return jsonify({'result': f"No elements with ID={ID} and Location={Location} found in the database."})

    # If User provides ID, Location and the exact Amount there is of that element:
    elif int(Amount) == int(matching_rows["Amount"].iloc[0]):
        df = df[~(df['ID'].eq(ID) & df['Location'].eq(Location))]
        print(f"Deleted every element with ID={ID} and Location={Location}")
        updateDataframe(repository, df, csv)
        if not edit:
            return jsonify({'result': "Element deleted effectively."})
        return None

    # If User provides ID, Location and a different Amount of element:
    else:
        df.loc[df['ID'].eq(ID) & df['Location'].eq(Location), "Amount"] = (
            int(matching_rows["Amount"].iloc[0]) - int(Amount)
        )
        print(f"Deleted {Amount} units of element with ID={ID} and Location={Location}")
        updateDataframe(repository, df, csv)
        if not edit:
            return jsonify({'result': "Element amount updated effectively."})
        return None


# Edit Item
@app.route('/update_item', methods=['POST'])
def update_item(data=None):
    if data is None:
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

    # Data structure for del_item and add_item
    deldata = {
        'token': token,
        'ID': pastID,
        'amount': pastAmount,
        'location': pastLocation
    }
    adddata = {
        'token': token,
        'ID': newID,
        'amount': newAmount,
        'location': newLocation,
        'parent': newParent,
        'Type': newType
    }

    # First, attempt to delete the past item
    delete_result = del_item(edit=True, deldata=deldata)
    
    if delete_result == None:
        print("Deletion successful, now adding the new item.")
        
        # Add the new item after successful deletion
        add_item(edit=True, adddata=adddata)
        
        return jsonify({'result': "Item updated successfully."})
    
    else:
        print("Deletion failed. Skipping the addition of the new item.")
        return jsonify({'error': "Failed to delete the old item."}), 400

# Start the Flask app
if __name__ == '__main__':
    app.run(debug=True)
