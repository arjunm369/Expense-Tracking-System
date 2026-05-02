let currentUserId = null;
let currentUsername = null;

async function login() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    if (!username || !password) return showMessage('Please enter username and password', true);

    try {
        const response = await fetch('http://localhost:8080/api/auth/login', {
            method: 'POST',
            headers: {'Content-Type': 'application/x-www-form-urlencoded'},
            body: `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`
        });
        if (!response.ok) throw new Error('Login failed');
        const user = await response.json();
        currentUserId = user.id;
        currentUsername = user.username;
        showApp();
    } catch (err) {
        showMessage(err.message, true);
    }
}

async function register() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const email = document.getElementById('email').value;
    const dob = document.getElementById('dob').value;
    const job = document.getElementById('job').value;
    if (!username || !password) return showMessage('Username and password required', true);

    try {
        const response = await fetch('http://localhost:8080/api/auth/register', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({username, password, email, dob, job})
        });
        if (!response.ok) throw new Error('Registration failed');
        showMessage('Registered successfully! Please login.');
    } catch (err) {
        showMessage(err.message, true);
    }
}

function logout() {
    currentUserId = null;
    currentUsername = null;
    document.getElementById('app-section').style.display = 'none';
    document.getElementById('auth-section').style.display = 'block';
}

function showApp() {
    document.getElementById('auth-section').style.display = 'none';
    document.getElementById('app-section').style.display = 'block';
    document.getElementById('current-user').textContent = currentUsername;
    loadExpenses();
}

async function addExpense() {
    const date = document.getElementById('expense-date').value;
    const category = document.getElementById('expense-category').value;
    const description = document.getElementById('expense-description').value;
    const amount = document.getElementById('expense-amount').value;
    if (!date || !amount) return alert('Date and amount required');

    await fetch('http://localhost:8080/api/expenses', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({user: {id: currentUserId}, date, category, description, amount})
    });
    loadExpenses();
}

async function loadExpenses() {
    const start = document.getElementById('filter-start').value;
    const end = document.getElementById('filter-end').value;
    const category = document.getElementById('filter-category').value;
    let url = `http://localhost:8080/api/expenses?userId=${currentUserId}`;
    if (category) url = `http://localhost:8080/api/expenses/filter/category?userId=${currentUserId}&category=${category}`;
    if (start && end) url = `http://localhost:8080/api/expenses/filter/date?userId=${currentUserId}&start=${start}&end=${end}`;

    const response = await fetch(url);
    const expenses = await response.json();
    const tbody = document.getElementById('expenses-body');
    tbody.innerHTML = '';
    expenses.forEach(e => {
        const row = `<tr><td>${e.date}</td><td>${e.category}</td><td>${e.description}</td><td>$${e.amount}</td></tr>`;
        tbody.innerHTML += row;
    });

    if (start && end) {
        const totalResp = await fetch(`http://localhost:8080/api/expenses/total?userId=${currentUserId}&start=${start}&end=${end}`);
        const total = await totalResp.json();
        document.getElementById('total-expense').textContent = `Total: $${total}`;
    }
}

function showMessage(msg, isError = false) {
    const el = document.getElementById('auth-message');
    el.textContent = msg;
    el.className = isError ? 'error' : '';
}