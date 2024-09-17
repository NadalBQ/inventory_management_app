document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('executeButton').addEventListener('click', addElement);
    document.getElementById('deleteButton').addEventListener('click', delElement);
    document.getElementById('updateButton').addEventListener('click', updElement);
});

function addElement() {
    const token = document.getElementById('addtoken').value;
    const ID = document.getElementById('addID').value;
    const location = document.getElementById('addlocation').value || "0";
    const amount = document.getElementById('addamount').value || "1";
    const parent = document.getElementById('addparent').value || "Trastero";
    const Type = document.getElementById('addwhichType').value || "Item";

    fetch('/add_item', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ token: token, ID: ID, location: location, amount: amount, parent: parent, Type: Type })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.error) {
            throw new Error(data.error);
        }
        document.getElementById('resultDivAdd').innerText = 'Result: ' + data.result;
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('resultDivAdd').innerText = 'An error occurred: ' + error.message;
    });
}

function delElement() {
    const token = document.getElementById('deltoken').value;
    const ID = document.getElementById('delID').value;
    const location = document.getElementById('dellocation').value || "0";
    const amount = document.getElementById('delamount').value || "1";
    

    fetch('/del_item', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ token: token, ID: ID, location: location, amount: amount})
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.error) {
            throw new Error(data.error);
        }
        document.getElementById('resultDivSub').innerText = 'Result: ' + data.result;
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('resultDivSub').innerText = 'An error occurred: ' + error.message;
    });
}

function updElement() {
    const token = document.getElementById('updtoken').value;
    const pastID = document.getElementById('pastID').value;
    const pastLocation = document.getElementById('pastLocation').value || "0";
    const pastAmount = document.getElementById('pastAmount').value || "1";
    const pastParent = document.getElementById('pastParent').value || "Trastero";
    const pastType = document.getElementById('pastWhichType').value || "Item";

    const newID = document.getElementById('newID').value;
    const newLocation = document.getElementById('newLocation').value || "0";
    const newAmount = document.getElementById('newAmount').value || "1";
    const newParent = document.getElementById('newParent').value || "Trastero";
    const newType = document.getElementById('newWhichType').value || "Item";

    fetch('/add_item', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ token: token, pastID: pastID, newID: newID, pastLocation: pastLocation, newLocation: newLocation, pastAmount: pastAmount, newAmount: newAmount, pastParent: pastParent, newParent: newParent, pastType: pastType, newType: newType })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.error) {
            throw new Error(data.error);
        }
        document.getElementById('resultDivUpd').innerText = 'Result: ' + data.result;
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('resultDivUpd').innerText = 'An error occurred: ' + error.message;
    });
}
