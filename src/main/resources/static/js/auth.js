const API_URL = 'http://localhost:8080/api/auth';

function showMessage(msg, isError) {
    var el = document.getElementById('auth-message');
    if (el) {
        el.textContent = msg;
        el.className = isError ? 'error' : 'success';
    }
}

async function login() {
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;
    
    if (!username || !password) {
        showMessage('Please enter username and password', true);
        return;
    }

    try {
        var response = await fetch(API_URL + '/login', {
            method: 'POST',
            headers: {'Content-Type': 'application/x-www-form-urlencoded'},
            body: 'username=' + encodeURIComponent(username) + '&password=' + encodeURIComponent(password)
        });
        
        var text = await response.text();
        
        if (!response.ok) {
            throw new Error(text || 'Invalid credentials');
        }

        var user = JSON.parse(text);
        
        if (!user.id) {
            throw new Error('Invalid response from server');
        }

        sessionStorage.setItem('userId', user.id);
        sessionStorage.setItem('username', user.username);
        window.location.href = 'dashboard.html';
    } catch (err) {
        showMessage(err.message, true);
    }
}

async function register() {
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;
    var email = document.getElementById('email').value;
    var dob = document.getElementById('dob').value;
    var job = document.getElementById('job').value;
    
    if (!username || !password || !email) {
        showMessage('Username, password and email are required', true);
        return;
    }

    try {
        var userData = {
            username: username,
            password: password,
            email: email,
            dob: dob,
            job: job
        };
        var response = await fetch(API_URL + '/register', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(userData)
        });
        
        var text = await response.text();
        
        if (!response.ok) {
            throw new Error(text || 'Registration failed');
        }

        showMessage('Registered successfully! Redirecting to login...');
        setTimeout(function() { window.location.href = 'index.html'; }, 1500);
    } catch (err) {
        showMessage(err.message, true);
    }
}
