const checkbtn = document.getElementById('checkMe');


window.onload = () => {
    const isDark = localStorage.getItem("darkMode") === "true";
    checkbtn.checked = isDark;
    RemidersDarkMode(isDark);
};

checkbtn.addEventListener("change", () => {
    const isChecked = checkbtn.checked;
    localStorage.setItem("darkMode", isChecked);
    RemidersDarkMode(isChecked);
});

function RemidersDarkMode(black) {
    const dashboard_main = document.querySelector('.dashboard-main');
    const count_badge = document.querySelector('.count-badge');
    const profile_text = document.querySelector('.profile-text h2');
    const profile_text_p = document.querySelector('.profile-text p');
    const empty_state = document.querySelector('.empty-state');
    const empty_state_p = document.querySelector('.empty-state p');
    const quick_actions = document.querySelectorAll('.quick-actions a');
    const modal_content = document.querySelector('.modal-content');
    const addReminderLabel = document.getElementById('addReminderLabel');
    const changecolordark = document.getElementById('changecolordark');
    const filterscontainer = document.querySelector('.filters-container');
    const search_box = document.querySelector('.search-box i');
    const search_box_input_input = document.querySelector('.search-box input');
    const search_box_background = document.querySelector('.search-box');
    const sort_select = document.querySelector('.sort-select');
    const reminder_card = document.querySelector('.reminder-card');
    const reminder_content_p = document.querySelector('.reminder-content p');
    const detail_item = document.querySelectorAll('.detail-item span');

    if (black) {
        dashboard_main.style.background = 'black';
        count_badge.style.color = 'white';
        profile_text.style.color = 'white';
        profile_text_p.style.color = 'white';
        empty_state.style.background = '#2f3542';
        empty_state.style.border = '#2f3542';
        empty_state_p.style.color = 'white';
        quick_actions.forEach(quick_action => {
            quick_action.style.background = 'black';
        });
        modal_content.style.background = 'black';
        addReminderLabel.style.color = 'white';
        changecolordark.style.color = '#7b8a8b';
        filterscontainer.style.background = '#2f3542';
        search_box.style.color = 'white';
        search_box_input_input.style.color = 'white';
        search_box_background.style.background = '#7b8a8b';
        sort_select.style.background = '#7b8a8b';
        sort_select.style.color = 'white';
        reminder_card.style.background = '#2f3542';
        reminder_content_p.style.color = 'white';
        detail_item.forEach(element => {
            element.style.color = 'white';
        });

    }
    else {
        dashboard_main.removeAttribute('style');
        count_badge.removeAttribute('style');
        profile_text.removeAttribute('style');
        profile_text_p.removeAttribute('style');
        empty_state.removeAttribute('style');
        empty_state_p.removeAttribute('style');
        quick_actions.forEach(quick_action => {
            quick_action.removeAttribute('style');
        });
        modal_content.removeAttribute('style');
        addReminderLabel.removeAttribute('style');
        changecolordark.removeAttribute('style');
        filterscontainer.removeAttribute('style');
        search_box.removeAttribute('style');
        search_box_input_input.removeAttribute('style');
        search_box_background.removeAttribute('style');
        sort_select.removeAttribute('style');
        sort_select.removeAttribute('style');
        reminder_card.removeAttribute('style');
        reminder_content_p.removeAttribute('style');
        detail_item.forEach(element => {
            element.removeAttribute('style');
        });
    }
}

//sidebar_colors
function ColorsChange(color) {
    const change = document.querySelectorAll('.sidebar-nav a');
    if (color) {
        change.forEach(ch => {
            ch.classList.add("sidebarDrakModeclr");
        });
    }
    else {
        change.forEach(ch => {
            ch.classList.remove("sidebarDrakModeclr");
        });
    }
}