const checkbtn = document.getElementById('checkMe');


window.onload = () => {
    const isDark = localStorage.getItem("darkMode") === "true";
    checkbtn.checked = isDark;
    DashboardDarkModeBtn(isDark);
};

checkbtn.addEventListener("change", () => {
    const isChecked = checkbtn.checked;
    localStorage.setItem("darkMode", isChecked);
    DashboardDarkModeBtn(isChecked);
});


//dashboard dark mode 
function DashboardDarkModeBtn(black) {
    const body = document.querySelector('body');
    const dashboard_body = document.querySelector('.dashboard-main');
    const quick_actions = document.querySelectorAll('.quick-actions a');
    const stat_cards = document.querySelectorAll('.stat-card');
    const stat_content_h3 = document.querySelectorAll('.stat-content h3');
    const stat_content_p = document.querySelectorAll('.stat-content p');
    const empty_states = document.querySelectorAll('.empty-state');
    const empty_states_paragh = document.querySelectorAll('.empty-state p');
    const modal_content_h3 =document.querySelector('.modal-content h3');
    const modal_content =document.querySelector('.modal-content');
    const profile_text_h2 = document.querySelector('.profile-text h2');
    const profile_text_p = document.querySelector('.profile-text p');
    const icons = document.querySelectorAll('.changecolorinDarkMode');
    const empty_message = document.querySelectorAll('.empty-message');
    const empty_message_p = document.querySelectorAll('.empty-message p');
    const section_header_h2 = document.querySelectorAll('.section-header h2');




    if (black) {
        body.style.background = 'var(--black)';
        dashboard_body.style.background = 'var(--black)';
        quick_actions.forEach(quick_action => {
            quick_action.style.background = 'var(--black)';
        })
        stat_cards.forEach(stat_card => {
            stat_card.style.background = 'var(--gray-dark)';
        })
        empty_states.forEach(empty_state => {
            empty_state.style.background = 'var(--gray-dark)';
            empty_state.style.border = 'var(--gray-dark)';
        })
        empty_states_paragh.forEach(empty_state_paragh => {
            empty_state_paragh.style.color = 'var(--white)';
        })
        profile_text_h2.style.color = 'var(--white)';
        profile_text_p.style.color = 'var(--white)';
        modal_content.style.background = 'var(--gray-dark)';
        modal_content_h3.style.color = 'var(--white)';
        icons.forEach(icon => {
            icon.style.color = 'var(--text-muted)';
        });
        stat_content_h3.forEach(stat => {
            stat.style.color = 'var(--white)';
        });
        stat_content_p.forEach(stat => {
            stat.style.color = 'var(--white)';
        });
        empty_message.forEach(stat => {
            stat.style.background = 'var(--gray-dark)';
            stat.style.border = 'var(--gray-dark)';
        });
        empty_message_p.forEach(empty => {
            empty.style.color = 'var(--white)';
        });
        section_header_h2.forEach(sec => {
            sec.style.color = 'var(--text-muted)';
        });
    }
    else {
        body.removeAttribute('style');
        dashboard_body.removeAttribute('style');
        quick_actions.forEach(quick_action => {
            quick_action.removeAttribute('style');
        })
        stat_cards.forEach(stat_card => {
            stat_card.removeAttribute('style');
        })
        empty_states.forEach(empty_state => {
            empty_state.removeAttribute('style');
        })
        empty_states_paragh.forEach(empty_state_paragh => {
            empty_state_paragh.removeAttribute('style');
        })
        profile_text_h2.removeAttribute('style');
        profile_text_p.removeAttribute('style');
        modal_content.removeAttribute('style');
        modal_content_h3.removeAttribute('style');
        icons.forEach(icon => {
            icon.removeAttribute('style');
        });
        stat_content_h3.forEach(stat => {
            stat.removeAttribute('style');
        });
        stat_content_p.forEach(stat => {
            stat.removeAttribute('style');
        });
        empty_message.forEach(stat => {
            stat.removeAttribute('style');
        });
        empty_message_p.forEach(empty => {
            empty.removeAttribute('style');
        });
        section_header_h2.forEach(sec => {
            sec.removeAttribute('style');
        });
    }
}

