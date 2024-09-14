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

function updElement() {
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
