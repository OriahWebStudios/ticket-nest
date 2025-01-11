// Animate elements

anime({ targets: '.logo', translateY: [-50, 0], opacity: [0, 1], duration: 1000, easing: 'easeOutQuad' });
anime({ targets: 'form', translateX: [100, 0], opacity: [0, 1], duration: 1500, easing: 'easeOutQuad' });
anime({ targets: '.footer, .right-footer', opacity: [0, 1], duration: 2000, easing: 'easeOutQuad', delay: 1000 }); 
anime({ targets: '.description', opacity: [0, 1], duration: 2000, easing: 'easeOutQuad', delay: 1500 });

// Real Time Validation
document.getElementById('email').addEventListener('input', validateEmail);
document.getElementById('username').addEventListener('input', validateUsername);
document.getElementById('password').addEventListener('input', validatePassword);
document.getElementById('confirm-password').addEventListener('input', validateConfirmPassword);

function validateUsername() {
    const username = document.getElementById('username').value;
    const usernameError = document.getElementById('username-error');
    usernameError.textContent = '';
    if (username.length < 3) {
        usernameError.textContent = 'Full Name must be at least 3 characters';
    }

    if (usernameError.textContent !== '') {
        document.getElementById('registration-submit').disabled = true;
    } else {
        document.getElementById('registration-submit').disabled = false;
    }
}

function validateEmail() {
    const email = document.getElementById('email').value;
    const emailError = document.getElementById('email-error');
    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    emailError.textContent = '';
    if (!email.match(emailRegex)) {
        emailError.textContent = 'Please enter a valid email address';
    }

    if (emailError.textContent !== '') {
        document.getElementById('registration-submit').disabled = true;
    } else {
        document.getElementById('registration-submit').disabled = false;
    }
}

function validatePassword() {
    const password = document.getElementById('password').value;
    const passwordError = document.getElementById('password-error');
    const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
    passwordError.textContent = '';
    if (password.length < 8 || !password.match(passwordRegex)) {
        passwordError.textContent = 'Password must be at least 8 characters long. Must contain at least one uppercase letter, one lowercase letter, one number, and one special character';
    }

   if (passwordError.textContent !== '') {
        document.getElementById('registration-submit').disabled = true;
    } else {
        document.getElementById('registration-submit').disabled = false;
    }
}

function validateConfirmPassword() {
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm-password').value;
    const confirmPasswordError = document.getElementById('confirm-password-error');
    confirmPasswordError.textContent = '';
    if (password !== confirmPassword) {
        confirmPasswordError.textContent = 'Passwords do not match';
    }

    if (confirmPasswordError.textContent !== '') {
        document.getElementById('registration-submit').disabled = true;
    } else {
        document.getElementById('registration-submit').disabled = false;
    }

}

// Show Add To Cart Form
document.getElementById('add_to_cart').addEventListener('click', function() {
    document.getElementById('add-to-cart-form').style.display = 'block';
});


