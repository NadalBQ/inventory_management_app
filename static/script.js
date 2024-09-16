document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('executeButton').addEventListener('click', addElement);
    document.getElementById('deleteButton').addEventListener('click', delElement);
    document.getElementById('updateButton').addEventListener('click', updElement);
});

function addElement() {
    const token = document.getElementById('token').value;
    const ID = document.getElementById('ID').value;
    const location = document.getElementById('location').value;
    const amount = document.getElementById('amount').value;
    const parent = document.getElementById('parent').value;
    const Type = document.getElementById('whichType').value;

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
    const token = document.getElementById('token').value;
    const ID = document.getElementById('ID').value;
    const location = document.getElementById('location').value;
    const amount = document.getElementById('amount').value;
    

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
    const token = document.getElementById('token').value;
    const pastID = document.getElementById('pastID').value;
    const pastLocation = document.getElementById('pastLocation').value;
    const pastAmount = document.getElementById('pastAmount').value;
    const pastParent = document.getElementById('pastParent').value;
    const pastType = document.getElementById('pastWhichType').value;

    const newID = document.getElementById('newID').value;
    const newLocation = document.getElementById('newLocation').value;
    const newAmount = document.getElementById('newAmount').value;
    const newParent = document.getElementById('newParent').value;
    const newType = document.getElementById('newWhichType').value;

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
