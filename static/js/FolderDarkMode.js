const checkbtn = document.getElementById('checkMe');


window.onload = () => {
    const isDark = localStorage.getItem("darkMode") === "true";
    checkbtn.checked = isDark;
    FolderDarkModeBtn(isDark);
};

checkbtn.addEventListener("change", () => {
    const isChecked = checkbtn.checked;
    localStorage.setItem("darkMode", isChecked);
    FolderDarkModeBtn(isChecked);
});


function FolderDarkModeBtn(dark) {
    const body = document.querySelector('.dashboard-main');
    const profile_text_h2 = document.querySelector('.profile-text h2');
    const profile_text_paragh = document.querySelector('.profile-text p');
    const quick_actions = document.querySelectorAll('.quick-action');
    const folder_form_card = document.querySelector('.folder-form-card');
    const form_group_input = document.querySelector('.form-group input');
    const modal_containers = document.querySelectorAll('.modal-container');
    const folders_cards = document.querySelectorAll('.folder-card');
    const folders_info_p = document.querySelectorAll('.folder-info p');
    const folder_info_h3 = document.querySelectorAll('.folder-info h3');
    const icons = document.querySelectorAll('.changecolorinDarkMode');
    const section_header_h2 = document.querySelectorAll('.section-header h2');
    const count_badge = document.querySelector('.count-badge');
    const empty_icon_h3 = document.querySelector('.empty-state h3');
    const empty_icon_p = document.querySelector('.empty-state p');
    const modal_content = document.querySelector('.modal-content');
    const modal_content_h3 = document.querySelector('.modal-content h3');


    if (dark) {
        body.style.background = 'var(--black)';
        profile_text_h2.style.color = 'var(--white)';
        profile_text_paragh.style.color = 'var(--white)';
        quick_actions.forEach(quick_action => {
            quick_action.style.background = 'var(--black)';
        });
        folder_form_card.style.background = 'var(--gray-dark)';
        form_group_input.style.background = 'var(--text-muted)';
        form_group_input.style.border = 'var(--text-muted)';
        form_group_input.style.color = 'white';
        modal_containers.forEach(modal_container => {
            modal_container.style.background = 'var(--black)'
        });
        folders_cards.forEach(folder_card => {
            folder_card.style.background = 'var(--gray-dark)';
        });
        folders_info_p.forEach(folder_info_p => {
            folder_info_p.style.color = 'var(--white)';
        })
        folder_info_h3.forEach(folder_info => {
            folder_info.style.color = 'var(--white)';
        })
        icons.forEach(icon => {
            icon.style.color = 'var(--text-muted)';
        })
        section_header_h2.forEach(section => {
            section.style.color = 'var(--text-muted)';
        })
        count_badge.style.color = 'var(--text-muted)';
        modal_content.style.background = 'var(--gray-dark)';
        modal_content_h3.style.color = 'var(--white)';
        empty_icon_h3.style.color = 'var(--text-muted)';
        empty_icon_p.style.color = 'var(--text-muted)';
        
    }
    else {
        body.removeAttribute('style');
        profile_text_h2.removeAttribute('style');
        profile_text_paragh.removeAttribute('style');
        quick_actions.forEach(quick_action => {
            quick_action.removeAttribute('style');
        });
        folder_form_card.removeAttribute('style');
        form_group_input.removeAttribute('style');
        modal_containers.forEach(modal_container => {
            modal_container.removeAttribute('style');
        });
        folders_cards.forEach(folder_card => {
            folder_card.removeAttribute('style');
        });
        folders_info_p.forEach(folder_info_p => {
            folder_info_p.removeAttribute('style');
        })
        folder_info_h3.forEach(folder_info_p => {
            folder_info_p.removeAttribute('style');
        })
        icons.forEach(icon => {
            icon.removeAttribute('style');
        })
        section_header_h2.forEach(section => {
            section.removeAttribute('style');
        })
        count_badge.removeAttribute('style');
        modal_content.removeAttribute('style');
        modal_content_h3.removeAttribute('style');
        empty_icon_h3.removeAttribute('style');
        empty_icon_p.removeAttribute('style');

   }
}

