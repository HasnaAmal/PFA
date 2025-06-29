document.addEventListener('DOMContentLoaded', function () {
  const logoutBtn = document.getElementById('logoutBtn');
  const logoutModal = document.getElementById('logoutModal');
  const confirmBtn = document.getElementById('confirmLogoutBtn');
  const cancelBtn = document.getElementById('cancelLogoutBtn');

  if (logoutBtn && logoutModal && confirmBtn && cancelBtn) {
    logoutBtn.addEventListener('click', function (e) {
      e.preventDefault();
      logoutModal.style.display = 'flex';
    });

    confirmBtn.addEventListener('click', function () {
      window.location.href = logoutBtn.dataset.logoutUrl;
    });

    cancelBtn.addEventListener('click', function () {
      logoutModal.style.display = 'none';
    });
  }
});
