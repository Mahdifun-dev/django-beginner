
document.addEventListener("DOMContentLoaded", function () {
// User dropdown
const userMenuButton = document.getElementById("user-menu-button");
const userDropdown = document.getElementById("user-dropdown");

userMenuButton.addEventListener("click", function () {
    userDropdown.classList.toggle("show");
});

// Close dropdowns when clicking outside
window.addEventListener("click", function (event) {
    if (
    !event.target.matches("#user-menu-button") &&
    !userMenuButton.contains(event.target)
    ) {
    if (userDropdown.classList.contains("show")) {
        userDropdown.classList.remove("show");
    }
    }
});
});
