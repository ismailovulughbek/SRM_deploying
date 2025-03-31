import config from './config.js';

document.getElementById("introServiceForm").addEventListener("submit", async function(event) {
    event.preventDefault();

    const form = document.getElementById("introServiceForm");
    const responseMessage = document.getElementById("responseMessage");
    const selectedLang = localStorage.getItem("selectedLanguage") || "ru";

    const formData = {
        full_name: form.full_name.value.trim(),
        email: form.email.value.trim(),
        phone: form.phone.value.trim(),
        service: form.service.value.trim()
    };

    if (Object.values(formData).some(value => value === "")) {
        showMessage("error", {
            en: "Please fill out all fields!",
            ru: "Пожалуйста, заполните все поля!",
            kz: "Барлық өрістерді толтырыңыз!"
        });
        return;
    }

    try {
        const response = await fetch(`${config.BACKEND_URL}/service`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(formData)
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.message?.[selectedLang] || "Something went wrong!");
        }

        showMessage("success", data.message);
        form.reset();
    } catch (error) {
        console.error("Error--> UI", error);
        showMessage("error", {
            en: "An error occurred!",
            ru: "Произошла ошибка!",
            kz: "Қате орын алды!"
        });
    }
});

// ✅ Xabar chiqaruvchi funksiya
function showMessage(type, messages) {
    const responseMessage = document.getElementById("responseMessage");
    const selectedLang = localStorage.getItem("selectedLanguage") || "ru";
    
    responseMessage.textContent = messages[selectedLang] || messages["ru"];
    responseMessage.style.display = "block";
    responseMessage.style.fontSize = "18px";
    responseMessage.style.fontWeight = "700";
    responseMessage.style.color = type === "success" ? "green" : "red";

    setTimeout(() => {
        responseMessage.style.display = "none";
    }, 3000);
}
