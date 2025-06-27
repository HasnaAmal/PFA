const checkbtn = document.getElementById('checkMe');


window.onload = () => {
    const isDark = localStorage.getItem("darkMode") === "true";
    checkbtn.checked = isDark;
    IndexDarkModeBtn(isDark)
};

checkbtn.addEventListener("change", () => {
    const isChecked = checkbtn.checked;
    localStorage.setItem("darkMode", isChecked);
    IndexDarkModeBtn(isChecked)
});



//index.html dark mode
function IndexDarkModeBtn(dark) {
    const header = document.querySelector('header');
    const Navlabels = document.querySelectorAll('nav a');
    const login = document.querySelector('.login-container');
    const register = document.querySelector('.register-container');
    const login_inputs = document.querySelectorAll('.form-group input');
    const auth_links = document.querySelectorAll('.auth-links p');
    const service_cards = document.querySelectorAll('.service-card');
    const service_cards_paragh = document.querySelectorAll('.service-card p');
    const service_features_options = document.querySelectorAll('.service-features li');
    const why_choose_us = document.querySelector('.why-choose-us');
    const text = document.querySelectorAll('.text p');

    const dashboard_body = document.querySelector('.dashboard_body');
    const stat_card = document.querySelector('.stat-card');

    if (dark) {

        header.style.background = 'var(--dark)';
        Navlabels.forEach(Navlabel => {
            Navlabel.style.color = 'var(--light)';
        })
        login.style.background = 'var(--dark)';
        register.style.background = 'var(--dark)';
        login.style.border = 'var(--dark)';
        register.style.border = 'var(--dark)';
        login_inputs.forEach(login_input => {
            login_input.style.background = 'var(--dark-gray)';
            login_input.style.border = 'var(--dark-gray)';
            login_input.style.color = 'white';
        })
        auth_links.forEach(auth_link => {
            auth_link.style.color = 'var(--light)';
        })
        service_cards.forEach(service_card => {
            service_card.style.background = 'var(--dark)';
            service_card.style.border = 'var(--dark)';
        })
        service_cards_paragh.forEach(service_card_paragh => {
            service_card_paragh.style.color = 'var(--light)';
        })
        service_features_options.forEach(service_features_option => {
            service_features_option.style.color = 'var(--light)';
        })
        why_choose_us.style.background = 'var(--dark)';
        text.forEach(paragh => {
            paragh.style.color = 'var(--light)'
        })
        dashboard_body.style.background = 'red';
        stat_card.style.background = 'red';
    }



    else {

        header.removeAttribute('style');
        Navlabels.forEach(Navlabel => {
            Navlabel.style.color = 'var(--text-primary)';
        })
        login.style.background = 'var(--bg-card)';
        login.style.border = 'var(--border)';
        register.style.background = 'var(--bg-card)';
        register.style.border = 'var(--border)';
        login_inputs.forEach(login_input => {
            login_input.removeAttribute('style');
        })
        auth_links.forEach(auth_link => {
            auth_link.style.color = 'var(--dark)';
        })
        service_cards.forEach(service_card => {
            service_card.style.background = 'var(--light)';
            service_card.style.border = 'var(--light)';
        })
        service_cards_paragh.forEach(service_card_paragh => {
            service_card_paragh.style.color = 'var(--dark)';
        })
        service_features_options.forEach(service_features_option => {
            service_features_option.style.color = 'var(--dark)';
        })
        why_choose_us.removeAttribute('style');
        text.forEach(paragh => {
            paragh.removeAttribute('style');
        })

    }

}



