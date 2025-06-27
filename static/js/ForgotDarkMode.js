const checkbtn = document.getElementById('checkMe');


window.onload = () => {
    const isDark = localStorage.getItem("darkMode") === "true";
    checkbtn.checked = isDark;
    ForgotDarkMode(isDark)
};

checkbtn.addEventListener("change", () => {
    const isChecked = checkbtn.checked;
    localStorage.setItem("darkMode", isChecked);
    ForgotDarkMode(isChecked)
});

function ForgotDarkMode(black) {
    const header = document.querySelector('header');
    const Navlabels = document.querySelectorAll('nav a');
    const login = document.querySelector('.login-container');
    const login_inputs = document.querySelector('.form-group input');
    const auth_links = document.querySelectorAll('.auth-links p');

    if (black) {
        header.style.background = 'var(--dark)';
        Navlabels.forEach(Navlabel => {
            Navlabel.style.color = 'var(--light)';
        })
        login.style.background = 'var(--dark)';
        login.style.border = 'var(--dark)';
        login_inputs.style.background = 'var(--dark-gray)';
        login_inputs.style.border = 'var(--dark-gray)';
        login_inputs.style.color = 'white';
        auth_links.forEach(auth_link => {
            auth_link.style.color = 'var(--light)';
        })
    }
    else {
        header.removeAttribute('style');
        Navlabels.forEach(Navlabel => {
            Navlabel.style.color = 'var(--text-primary)';
        })
        login.style.background = 'var(--bg-card)';
        login.style.border = 'var(--border)';
        login_inputs.removeAttribute('style');
        auth_links.forEach(auth_link => {
            auth_link.style.color = 'var(--dark)';
        })
    }
}