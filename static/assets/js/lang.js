document.addEventListener("DOMContentLoaded", function () {
    const langSelector = document.getElementById("language-selector");

    let selectedLang = localStorage.getItem("selectedLanguage") || "ru";

    loadLanguage(selectedLang);
    
    langSelector.value = selectedLang;

    langSelector.addEventListener("change", function () {
        const newLang = langSelector.value;
        localStorage.setItem("selectedLanguage", newLang);
        loadLanguage(newLang);
    });
});

function loadLanguage(lang) {
    fetch("/static/assets/js/lang.json")
        .then(response => response.json())
        .then(data => {
            document.querySelectorAll("[data-translate]").forEach(element => {
                let key = element.getAttribute("data-translate");

                let keys = key.split(".");
                let translation = data[lang];

                keys.forEach(k => {
                    translation = translation?.[k];
                });

                if (element.tagName === "INPUT" || element.tagName === "TEXTAREA") {
                    element.placeholder = translation || key;
                } 
                else if (element.tagName === "OPTION") {
                    element.textContent = translation || key;
                } 
                else {
                    element.innerHTML = translation || key;
                }
            });
        })
        .catch(error => console.error("LANG ERROR ----------->(UI)", error));
}
