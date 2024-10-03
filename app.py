from flask import Flask, request, jsonify, render_template
import pandas as pd
from github import Github
import base64
import io

"""***LOGGER***"""
import logging
from bisect import bisect
from logging import getLogger, Formatter, LogRecord, StreamHandler
from typing import Dict


class LevelFormatter(Formatter):
    def __init__(self, formats: Dict[int, str], **kwargs):
        super().__init__()

        if 'fmt' in kwargs:
            raise ValueError(
                'Format string must be passed to level-surrogate formatters, '
                'not this one'
            )

        self.formats = sorted(
            (level, Formatter(fmt, **kwargs)) for level, fmt in formats.items()
        )

    def format(self, record: LogRecord) -> str:
        idx = bisect(self.formats, (record.levelno,), hi=len(self.formats)-1)
        level, formatter = self.formats[idx]
        return formatter.format(record)
    

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

if not logger.hasHandlers():
    handler = StreamHandler()
    formatter = LevelFormatter(
        {
            logging.DEBUG: '\033[94m[%(asctime)s - %(lineno)d] DEBUG\033[0m: %(message)s',
            logging.INFO: '\033[94mINFO\033[0m: %(message)s',
            logging.WARNING: '\033[93mWARNING\033[0m: %(message)s',
            logging.ERROR: '\033[91mERROR\033[0m: %(message)s',
            logging.CRITICAL: '\033[91mCRITICAL\033[0m: %(message)s'
        }
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

logger.info("Logger set up successfully")



repository_name = "nadalbq/inventory_management_app"
csv_file_path = "./static/csvs/inventory.csv"
app = Flask(__name__, static_url_path='/static')
logger.info("Flask app set up correctly")

# Web addresses
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/finder')
def finder():
    return render_template('finder.html')

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
def updateDataframe(repository, df, csv, commit="Updating CSV content"):
    
    new_csv_content = df.to_csv(index=False)
    repository.update_file(csv_file_path, commit, new_csv_content, csv.sha)
    logger.debug("updateDataframe function saved the dataframe with commit= \"" + commit + "\"")

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

    logger.info(f"Adding item: Token={token}, ID={ID}, Location={Location}, Amount={Amount}, Parent={Parent}, Type={Type}")

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
        logger.info("\nItem already exists, amounts were added together\n")
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
        logger.info("Added a new item to the database")

    updateDataframe(repository, df, csv)
    
    if not edit:
        return jsonify({'result': "Element added successfully"})
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

    logger.info("delete item: " + token, ID, Location, Amount)

    g = Github(token)
    repository = g.get_repo(repository_name)
    csv = repository.get_contents(csv_file_path)
    decoded_csv = base64.b64decode(csv.content).decode('utf-8')
    csv_io = io.StringIO(decoded_csv)
    df = pd.read_csv(csv_io)
    logger.debug(df)
    logger.debug("dataframe taken from github successfully " + "_"*30)
    # If User does not provide an ID:
    if not ID:
        logger.info("Tried to delete element without ID reference")
        return jsonify({'result': "No ID was received, could not delete element."})

    # Filter the DataFrame to get matching rows
    matching_rows = df.loc[df['ID'].eq(ID) & df['Location'].eq(Location)]
    logger.debug(matching_rows, "Matching rows " + "_"*30)
    # Check if there are any matching rows before proceeding
    if matching_rows.empty:
        return jsonify({'result': f"No elements with ID={ID} and Location={Location} found in the database."})

    # If User provides ID, Location and the exact Amount there is of that element:
    elif int(Amount) == int(matching_rows["Amount"].iloc[0]):
        df = df[~(df['ID'].eq(ID) & df['Location'].eq(Location))]
        logger.info(f"Deleted every element with ID={ID} and Location={Location}")
        updateDataframe(repository, df, csv)
        if not edit:
            return jsonify({'result': "Element deleted successfully."})
        return "Done"

    # If User provides ID, Location and a different Amount of element:
    else:
        df.loc[df['ID'].eq(ID) & df['Location'].eq(Location), "Amount"] = (
            int(matching_rows["Amount"].iloc[0]) - int(Amount)
        )
        logger.info(f"Deleted {Amount} units of element with ID={ID} and Location={Location}")
        updateDataframe(repository, df, csv)
        if not edit:
            return jsonify({'result': "Element amount updated successfully."})
        return "Done"


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
    
    if delete_result == "Done":
        logger.info("Deletion successful, now adding the new item.")
        
        # Add the new item after successful deletion
        add_item(edit=True, adddata=adddata)
        
        return jsonify({'result': "Item updated successfully."})
    
    else:
        logger.info("Deletion failed. Skipping the addition of the new item.")
        return jsonify({'error': "Failed to delete the old item."}), 400

# Start the Flask app
if __name__ == '__main__':
    app.run(debug=True)
