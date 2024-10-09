document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('executeButton').addEventListener('click', addElement);
    document.getElementById('deleteButton').addEventListener('click', delElement);
    document.getElementById('updateButton').addEventListener('click', updElement);
});

// Reusable function to send POST requests
function sendRequest(url, body, resultDiv) {
    document.getElementById(resultDiv).innerText = 'Processing...'; // Show a loading message
    fetch(url, {
        signal: AbortSignal.timeout(5000),
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(body)
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
        document.getElementById(resultDiv).innerText = 'Result: ' + data.result;
    })
    .catch(error => {
        console.error('Error:', error);
        let errorMessage = 'An error occurred';
        if (error.message.includes('Network response')) {
            errorMessage = 'Failed to reach the server. Please try again.';
        } else if (error.message.includes('token')) {
            errorMessage = 'Invalid GitHub token.';
        }
        document.getElementById(resultDiv).innerText = errorMessage;
    });
}

// Add element function
function addElement() {
    const token = document.getElementById('addtoken').value;
    const ID = document.getElementById('addID').value;

    // Form validation for required fields
    if (!token || !ID) {
        alert('GitHub token and Element ID are required.');
        return;
    }

    const body = {
        token: token,
        ID: ID,
        location: document.getElementById('addlocation').value || "0",
        amount: document.getElementById('addamount').value || "1",
        parent: document.getElementById('addparent').value || "Trastero",
        Type: document.getElementById('addwhichType').value || "Item"
    };

    sendRequest('/add_item', body, 'resultDivAdd');
}

// Delete element function
function delElement() {
    const token = document.getElementById('deltoken').value;
    const ID = document.getElementById('delID').value;

    // Form validation for required fields
    if (!token || !ID) {
        alert('GitHub token and Element ID are required.');
        return;
    }

    const body = {
        token: token,
        ID: ID,
        location: document.getElementById('dellocation').value || "0",
        amount: document.getElementById('delamount').value || "1"
    };

    sendRequest('/del_item', body, 'resultDivSub');
}

// Update element function
function updElement() {
    const token = document.getElementById('updtoken').value;
    const pastID = document.getElementById('pastID').value;
    const newID = document.getElementById('newID').value;

    // Form validation for required fields
    if (!token || !pastID || !newID) {
        alert('GitHub token, Past ID, and New ID are required.');
        return;
    }

    const body = {
        token: token,
        pastID: pastID,
        pastLocation: document.getElementById('pastLocation').value || "0",
        pastAmount: document.getElementById('pastAmount').value || "1",
        pastParent: document.getElementById('pastParent').value || "Trastero",
        pastType: document.getElementById('pastWhichType').value || "Item",
        newID: newID,
        newLocation: document.getElementById('newLocation').value || "0",
        newAmount: document.getElementById('newAmount').value || "1",
        newParent: document.getElementById('newParent').value || "Trastero",
        newType: document.getElementById('newWhichType').value || "Item"
    };

    sendRequest('/update_item', body, 'resultDivUpd');
}

async function loadCSV() {
    try {
        const response = await fetch('./csvs/inventory.csv');
        const csvText = await response.text();

        const rows = csvText.split('\n').slice(1); // Remove the header row
        const tableBody = document.getElementById('table-body');

        // Iterate over each row in the CSV and use helper function
        rows.forEach(row => {
            const columns = row.split(',');
            if (columns.length === 6) {
                addTransaction(tableBody, columns);
            }
        });
    } catch (error) {
        console.error('Error loading CSV:', error);
    }
}

// Helper function to add a transaction row to the table
function addTransaction(tableBody, columns) {
    const newRow = document.createElement('tr');
    newRow.innerHTML = `
        <td>${columns[0]}</td>
        <td>${columns[1]}</td>
        <td>${columns[2]}</td>
        <td>${columns[3]}</td>
        <td>${columns[4]}</td>
    `;
    tableBody.appendChild(newRow);
}

// Load CSV once the DOM is fully loaded
document.addEventListener('DOMContentLoaded', loadCSV);