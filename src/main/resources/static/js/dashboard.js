const API_URL = 'http://localhost:8080/api/expenses';
var currentUserId = sessionStorage.getItem('userId');
var currentUsername = sessionStorage.getItem('username');

if (!currentUserId) {
    window.location.href = 'index.html';
}

document.getElementById('welcome-user').textContent = 'Welcome, ' + currentUsername + '!';

function logout() {
    sessionStorage.clear();
    window.location.href = 'index.html';
}

async function addExpense() {
    var dateInput = document.getElementById('expense-date').value;
    var category = document.getElementById('expense-category').value;
    var description = document.getElementById('expense-description').value;
    var amount = document.getElementById('expense-amount').value;
    
    if (!dateInput || !amount) {
        alert('Date and amount are required');
        return;
    }

    var expenseData = {
        user: {id: parseInt(currentUserId)},
        date: dateInput,
        category: category,
        description: description,
        amount: parseFloat(amount)
    };

    try {
        var response = await fetch(API_URL, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(expenseData)
        });
        
        var text = await response.text();
        if (!response.ok) {
            throw new Error(text || 'Failed to add expense');
        }
        
        document.getElementById('expense-date').value = '';
        document.getElementById('expense-description').value = '';
        document.getElementById('expense-amount').value = '';
        
        alert('Expense added successfully!');
        loadExpenses();
    } catch (err) {
        alert('Error: ' + err.message);
    }
}

async function loadExpenses() {
    var start = document.getElementById('filter-start').value;
    var end = document.getElementById('filter-end').value;
    var category = document.getElementById('filter-category').value;
    
    var url = API_URL + '?userId=' + currentUserId;
    if (start && end) {
        url = API_URL + '/filter/date?userId=' + currentUserId + '&start=' + start + '&end=' + end;
    }
    if (category) {
        url = API_URL + '/filter/category?userId=' + currentUserId + '&category=' + category;
    }

    try {
        var response = await fetch(url);
        if (!response.ok) throw new Error('Failed to load expenses');
        
        var expenses = await response.json();
        
        var tbody = document.getElementById('expenses-body');
        tbody.innerHTML = '';
        
        if (!expenses || expenses.length === 0) {
            tbody.innerHTML = '<tr><td colspan="4" style="text-align:center;padding:20px;color:#666;">No expenses found</td></tr>';
            return;
        }
        
        expenses.forEach(function(e) {
            var dateStr = e.date || 'N/A';
            var cat = e.category || 'N/A';
            var desc = e.description || 'N/A';
            var amount = (e.amount !== null && e.amount !== undefined) ? parseFloat(e.amount).toFixed(2) : '0.00';
            
            var row = '<tr>' +
                '<td>' + dateStr + '</td>' +
                '<td>' + cat + '</td>' +
                '<td>' + desc + '</td>' +
                '<td>₹' + amount + '</td>' +
            '</tr>';
            tbody.innerHTML += row;
        });

        if (start && end) {
            var totalResp = await fetch(API_URL + '/total?userId=' + currentUserId + '&start=' + start + '&end=' + end);
            var total = await totalResp.json();
            document.getElementById('total-expense').textContent = 'Total: ₹' + parseFloat(total).toFixed(2);
        }
    } catch (err) {
        console.error('Error loading expenses:', err);
    }
}

document.addEventListener('DOMContentLoaded', function() {
    loadExpenses();
});
