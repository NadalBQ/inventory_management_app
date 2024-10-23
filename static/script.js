document.addEventListener('DOMContentLoaded', () => {
    loadTableData();
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

async function loadTableData() {
    try {
        // Assuming you have a CSV file in the same directory, replace with your source file if different
        const response = await fetch('../static/csvs/inventory.csv');
        const csvText = await response.text();

        // Parse CSV text into an array of rows
        const rows = csvText.split('\n').slice(1); // Skip the header row

        // Reference to table body element
        const tableBody = document.getElementById('table-body');

        // Clear existing rows (if any) except for the example row
        tableBody.innerHTML = '';

        rows.forEach(row => {
            // Split the row by commas to get each column value
            const columns = row.split(',');

            if (columns.length >= 5) { // Ensure there are enough columns in the row
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

        // Populate the filters once the table data has been loaded
        populateFilters();
    } catch (error) {
        console.error("Error loading CSV data: ", error);
    }
}

// TABLE IN FINDER.HTML

// Function to sort table by the selected column (A-Z or Z-A)
function sortTable(columnIndex, order) {
    const table = document.getElementById("table-body");
    let rows = Array.from(table.rows);
    
    rows.sort((a, b) => {
        let aText = a.cells[columnIndex].innerText.toLowerCase();
        let bText = b.cells[columnIndex].innerText.toLowerCase();
        if (order === 'asc') {
            return aText.localeCompare(bText);
        } else {
            return bText.localeCompare(aText);
        }
    });

    // Re-append sorted rows
    rows.forEach(row => table.appendChild(row));
}

// Function to filter the table based on dropdown values
function filterTable(columnIndex) {
    const table = document.getElementById("table-body");
    const rows = table.rows;
    const filters = [
        document.getElementById("amountFilter").value,
        document.getElementById("locationFilter").value,
        document.getElementById("parentFilter").value,
        document.getElementById("typeFilter").value
    ];

    // Loop through each row and hide/show based on the filter
    for (let i = 0; i < rows.length; i++) {
        let showRow = true;
        for (let j = 0; j < filters.length; j++) {
            if (filters[j] && rows[i].cells[j + 1].innerText !== filters[j]) {
                showRow = false;
                break;
            }
        }
        rows[i].style.display = showRow ? "" : "none";
    }
}

// Populate the filters dynamically based on unique values in each column
function populateFilters() {
    const table = document.getElementById("table-body");
    const rows = table.rows;

    // Collect unique values for each column
    const amountSet = new Set();
    const locationSet = new Set();
    const parentSet = new Set();
    const typeSet = new Set();

    for (let i = 0; i < rows.length; i++) {
        amountSet.add(rows[i].cells[1].innerText);
        locationSet.add(rows[i].cells[2].innerText);
        parentSet.add(rows[i].cells[3].innerText);
        typeSet.add(rows[i].cells[4].innerText);
    }

    // Populate filter dropdowns with unique values
    addOptionsToFilter("amountFilter", amountSet);
    addOptionsToFilter("locationFilter", locationSet);
    addOptionsToFilter("parentFilter", parentSet);
    addOptionsToFilter("typeFilter", typeSet);
}

// Utility function to add options to a dropdown filter
function addOptionsToFilter(filterId, valueSet) {
    const filter = document.getElementById(filterId);
    valueSet.forEach(value => {
        let option = document.createElement("option");
        option.value = value;
        option.innerText = value;
        filter.appendChild(option);
    });
}

// Run populateFilters on page load to fill the dropdowns with values
window.onload = populateFilters;


document.addEventListener('DOMContentLoaded', () => {
    // Build the initial grid with 25 tiles (indices 0-24)
    const grid = document.getElementById('grid');
    for (let i = 0; i < 25; i++) {
        const tile = document.createElement('div');
        tile.classList.add('tile');
        tile.textContent = i;  // Each tile shows its index
        grid.appendChild(tile);
    }

    // Attach filter listeners
    document.getElementById('amountFilter').addEventListener('change', applyFilters);
    document.getElementById('locationFilter').addEventListener('change', applyFilters);
    document.getElementById('parentFilter').addEventListener('change', applyFilters);
    document.getElementById('typeFilter').addEventListener('change', applyFilters);
});

// Function to apply filters and update the grid
function applyFilters() {
    const table = document.getElementById('table-body');
    const rows = Array.from(table.getElementsByTagName('tr'));

    // Get the filter values
    const amountFilterValue = document.getElementById('amountFilter').value;
    const locationFilterValue = document.getElementById('locationFilter').value;
    const parentFilterValue = document.getElementById('parentFilter').value;
    const typeFilterValue = document.getElementById('typeFilter').value;

    // Clear previous enlarged tiles
    const allTiles = document.querySelectorAll('.tile');
    allTiles.forEach(tile => tile.classList.remove('enlarged'));

    rows.forEach(row => {
        const cells = row.getElementsByTagName('td');
        const amount = cells[1].textContent.trim();    // Assuming Amount is the 2nd column
        const location = cells[2].textContent.trim();  // Assuming Location is the 3rd column
        const parent = cells[3].textContent.trim();    // Assuming Parent is the 4th column
        const type = cells[4].textContent.trim();      // Assuming Type is the 5th column

        // Check if the row matches the filter criteria
        const matchesAmount = amountFilterValue === '' || amount === amountFilterValue;
        const matchesLocation = locationFilterValue === '' || location === locationFilterValue;
        const matchesParent = parentFilterValue === '' || parent === parentFilterValue;
        const matchesType = typeFilterValue === '' || type === typeFilterValue;

        // If all filters match, show the row, else hide it
        if (matchesAmount && matchesLocation && matchesParent && matchesType) {
            row.style.display = ''; // Show row
        } else {
            row.style.display = 'none'; // Hide row
        }
    });

    // After filtering rows, enlarge the grid tiles for visible locations
    rows.forEach(row => {
        // Check if the row is visible
        if (row.style.display !== 'none') {
            const cells = row.getElementsByTagName('td');
            const location = cells[2].textContent.trim(); // Assuming Location is the 3rd column

            // Get the location index and enlarge the corresponding tile
            const locationIndex = parseInt(location, 10);
            if (!isNaN(locationIndex) && locationIndex >= 0 && locationIndex < 25) {
                const tile = document.querySelector(`.tile:nth-child(${locationIndex + 1})`);
                if (tile) {
                    tile.classList.add('enlarged');
                }
            }
        }
    });
}
