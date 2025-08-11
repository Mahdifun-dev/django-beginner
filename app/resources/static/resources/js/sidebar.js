document.addEventListener("DOMContentLoaded", () => {
const sidebar = document.getElementById("sidebar");
const labels = sidebar.querySelectorAll(".sidebar-label");
const icons = sidebar.querySelectorAll(".sidebar-icon");
labels.forEach(label => {
    label.classList.add("hidden");
});
sidebar.classList.add("w-[110px]");

icons.forEach(label => {
    label.classList.add("animate-float");
});
});
function toggleSidebar() {
const sidebar = document.getElementById("sidebar");
const labels = sidebar.querySelectorAll(".sidebar-label");
const icons = sidebar.querySelectorAll(".sidebar-icon");
sidebar.classList.toggle("w-64");
sidebar.classList.toggle("w-[110px]");

labels.forEach(label => {
    label.classList.toggle("hidden");
});
icons.forEach(label => {
    label.classList.toggle("animate-float");
});
}