
function googleTranslateElementInit() {
    new google.translate.TranslateElement({
        pageLanguage: 'fr',
        includedLanguages: 'en,fr,ar',
        autoDisplay: false
    }, 'google_translate_element');
}

function changeLanguage(selectElement) {
    const lang = selectElement.value;
    const interval = setInterval(() => {
        const googleSelect = document.querySelector(".goog-te-combo");
        if (googleSelect) {
            googleSelect.value = lang;
            googleSelect.dispatchEvent(new Event("change"));
            clearInterval(interval);
        }
    }, 500);
}

