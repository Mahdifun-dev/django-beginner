document.addEventListener("DOMContentLoaded", function () {
  const currentPath = window.location.pathname;
  const sidebarItems = document.querySelectorAll(".sidebar-item");

  sidebarItems.forEach((item) => {
    const itemHref = item.getAttribute("href");

    // بررسی دقیق‌تر: اگر آدرس دقیقاً برابر باشه
    if (itemHref === currentPath) {
      item.classList.add("active");
    } else {
      item.classList.remove("active");
    }
  });
});