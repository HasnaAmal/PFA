function googleTranslateElementInit() {
    new google.translate.TranslateElement({
      pageLanguage: 'fr',
      includedLanguages: 'en,fr,ar',
      autoDisplay: false
    }, 'google_translate_element');
  }

  function changeLanguage(select) {
  const lang = select.value;

  // Si la langue est arabe, modifier manuellement le titre
  const title = document.getElementById('login-title');
  if (title) {
    title.textContent = (lang === 'ar') ? 'تسجيل الدخول' : 'Connexion';
  }

  // Traduction avec Google Translate
  const interval = setInterval(() => {
    const googleSelect = document.querySelector(".goog-te-combo");
    if (googleSelect) {
      googleSelect.value = lang;
      googleSelect.dispatchEvent(new Event("change"));
      clearInterval(interval);
    }
  }, 500);
}


  function getCurrentLangFromCookie() {
    const match = document.cookie.match(/(?:^|;\s*)googtrans=\/\w+\/(\w+)/);
    return match ? match[1] : 'fr';
  }

  document.addEventListener("DOMContentLoaded", () => {
    const currentLang = getCurrentLangFromCookie();
    const select = document.getElementById("selectLang");
    if (select) select.value = currentLang;
  });
