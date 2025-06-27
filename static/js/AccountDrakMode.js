const checkbtn = document.getElementById('checkMe');

window.onload = () => {
    const isDark = localStorage.getItem("darkMode") === "true";
    checkbtn.checked = isDark;
    AccountDarkModeBtn(isDark);
};

checkbtn.addEventListener("change", () => {
    const isChecked = checkbtn.checked;
    localStorage.setItem("darkMode", isChecked);
    AccountDarkModeBtn(isChecked);
});

function AccountDarkModeBtn(dark) {
    const main = document.getElementById('main');
    const profile_container = document.querySelector('.profile-container');
    const profile_title = document.querySelector('.profile-title');
    const profile_picture_wrapper = document.querySelector('.profile-picture-wrapper');
    const form_group_labels = document.querySelectorAll('.form-group label');
    const input_wrapper_input = document.querySelectorAll('.input-wrapper input');

    if (dark) {
        main.style.background = 'var(--black)';
        profile_container.style.background = 'var(--black)';
        profile_title.style.color = 'var(--white)';
        profile_picture_wrapper.style.background = 'var(--white)';
        form_group_labels.forEach(form_group_label => {
            form_group_label.style.color = 'var(--white)';
        })
        input_wrapper_input.forEach(change => {
            change.style.background = 'var(--gray-dark)';
            change.style.color = 'white';
        })
    }
    else {
        main.removeAttribute('style');
        profile_container.removeAttribute('style');
        profile_title.removeAttribute('style');
        profile_picture_wrapper.removeAttribute('style');
        form_group_labels.forEach(form_group_label => {
            form_group_label.removeAttribute('style');
        });
        input_wrapper_input.forEach(change => {
            change.removeAttribute('style');
        });
    }

}

