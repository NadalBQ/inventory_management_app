document.addEventListener('DOMContentLoaded', () => {
    loadTableData();
    document.getElementById('executeButton').addEventListener('click', addElement);
    document.getElementById('deleteButton').addEventListener('click', delElement);
    document.getElementById('updateButton').addEventListener('click', updElement);

    // Attach filter listeners
    document.getElementById('amountFilter').addEventListener('change', applyFilters);
    document.getElementById('locationFilter').addEventListener('change', applyFilters);
    document.getElementById('parentFilter').addEventListener('change', applyFilters);
    document.getElementById('typeFilter').addEventListener('change', applyFilters);
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
        loadTableData(); // Reload table data after any change
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

// Load table data
async function loadTableData() {
    try {
        const response = await fetch('../static/csvs/inventory.csv');
        const csvText = await response.text();
        const rows = csvText.split('\n').slice(1);

        const tableBody = document.getElementById('table-body');
        tableBody.innerHTML = '';

        rows.forEach(row => {
            const columns = row.split(',');
            if (columns.length >= 5) {
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
        });
        
        populateFilters(); // Refresh filters based on updated data
    } catch (error) {
        console.error("Error loading CSV data: ", error);
    }
}

// Function to populate filters based on table data
function populateFilters() {
    const table = document.getElementById('table-body');
    const rows = Array.from(table.getElementsByTagName('tr'));

    const amounts = new Set();
    const locations = new Set();
    const parents = new Set();
    const types = new Set();

    rows.forEach(row => {
        const cells = row.getElementsByTagName('td');
        amounts.add(cells[1].textContent.trim());
        locations.add(cells[2].textContent.trim());
        parents.add(cells[3].textContent.trim());
        types.add(cells[4].textContent.trim());
    });

    populateDropdown('amountFilter', amounts);
    populateDropdown('locationFilter', locations);
    populateDropdown('parentFilter', parents);
    populateDropdown('typeFilter', types);
}

function populateDropdown(filterId, uniqueValues) {
    const filterDropdown = document.getElementById(filterId);
    filterDropdown.innerHTML = '';
    const defaultOption = document.createElement('option');
    defaultOption.value = '';
    defaultOption.textContent = 'Select';
    filterDropdown.appendChild(defaultOption);

    uniqueValues.forEach(value => {
        const option = document.createElement('option');
        option.value = value;
        option.textContent = value;
        filterDropdown.appendChild(option);
    });
}

function applyFilters() {
    const table = document.getElementById('table-body');
    const rows = Array.from(table.getElementsByTagName('tr'));

    const amountFilterValue = document.getElementById('amountFilter').value;
    const locationFilterValue = document.getElementById('locationFilter').value;
    const parentFilterValue = document.getElementById('parentFilter').value;
    const typeFilterValue = document.getElementById('typeFilter').value;

    rows.forEach(row => {
        const cells = row.getElementsByTagName('td');
        const amount = cells[1].textContent.trim();
        const location = cells[2].textContent.trim();
        const parent = cells[3].textContent.trim();
        const type = cells[4].textContent.trim();

        const matchesAmount = !amountFilterValue || amount === amountFilterValue;
        const matchesLocation = !locationFilterValue || location === locationFilterValue;
        const matchesParent = !parentFilterValue || parent === parentFilterValue;
        const matchesType = !typeFilterValue || type === typeFilterValue;

        row.style.display = matchesAmount && matchesLocation && matchesParent && matchesType ? '' : 'none';
    });
}
