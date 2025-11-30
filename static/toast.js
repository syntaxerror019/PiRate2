function showToast(text, duration = 3000, color = "primary") {
  const notification = document.createElement("div");
  notification.className = "position-fixed top-0 end-0 p-3";
  notification.innerHTML = `
    <div class="toast align-items-center text-white bg-${color} border-0" role="alert" aria-live="assertive" aria-atomic="true">
      <div class="d-flex">
        <div class="toast-body">${text}</div>
        <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
      </div>
    </div>
  `;
  document.body.appendChild(notification);
  const toast = new bootstrap.Toast(notification.firstChild);
  toast.show();
  setTimeout(() => {
    toast.hide();
    document.body.removeChild(notification);
  }, duration);
}
