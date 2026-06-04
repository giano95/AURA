document.addEventListener("DOMContentLoaded", (event) => {
    // const toggle = document.querySelector("button").getElementsByClassName("theme-toggle")[0];
    const toggle = document.getElementById("theme-toggle");

    function setTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.theme = theme
    }

    // Load saved theme
    if (localStorage.theme === "dark" || localStorage.theme === "light") {
        setTheme(localStorage.theme)
    } else {
        if (window.matchMedia("(prefers-color-scheme: dark)").matches) {
            setTheme("dark")
        } else if (window.matchMedia("(prefers-color-scheme: light)").matches) {
            setTheme("light")
        } else {
            setTheme("dark") // Default to dark
        }
    }

    // Toggle themes on click
    toggle.addEventListener("click", (event) => {
        localStorage.theme === "dark" ? setTheme("light") : setTheme("dark")
    });
});