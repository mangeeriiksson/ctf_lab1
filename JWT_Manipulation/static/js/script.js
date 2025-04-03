// Funktion för att animera flaggans avslöjande
function animateFlagReveal() {
    const flag = document.querySelector(".flag");
    if (flag) {
        flag.style.opacity = 0; // Döljer flaggan från början
        flag.style.transition = "opacity 2s ease-in-out"; // Sätter övergångseffekten
        setTimeout(() => {
            flag.style.opacity = 1; // Gör flaggan synlig efter fördröjningen
            flag.classList.add("glow-pulse"); // Lägger till pulseringseffekten
        }, 300); // Fördröjning innan flaggan visas
    }
}

// Funktion för att hämta och visa JWT-token från cookies
window.addEventListener("DOMContentLoaded", () => {
    const match = document.cookie.match(/auth_token=([^;]+)/);
    if (match) {
        console.log("JWT Token:", match[1]); // Skriv ut token i konsolen

        try {
            const payload = JSON.parse(atob(match[1].split('.')[1])); // Dekoda JWT payload
            console.log("Decoded JWT Payload:", payload); // Skriv ut dekodad payload
        } catch (e) {
            console.error("Could not decode token:", e); // Om det går fel vid dekodning
        }
    } else {
        console.log("No token found in cookies.");
    }
});

// Kalla på animateFlagReveal när sidan har laddats
document.addEventListener("DOMContentLoaded", function () {
    animateFlagReveal();
});
