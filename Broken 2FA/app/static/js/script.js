document.addEventListener("DOMContentLoaded", function () {
    const passwordField = document.getElementById("password");
    const twoFAField = document.getElementById("2fa");
    const authResult = document.getElementById("auth-result");

    // 🔥 Funktion för att skicka lösenord och 2FA
    async function submitFlag() {
        let password = passwordField.value.trim();
        let twoFA = twoFAField.value.trim();

        try {
            let response = await fetch("/get_flag", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ password: password, twofa: twoFA })
            });

            let data = await response.json();

            if (data.flag) {
                authResult.innerHTML = `
                    🎉 The vault doors creak open...  
                    Flag: <strong>${data.flag}</strong><br><br>
                    📜 As you step inside, you uncover an ancient truth:<br>
                    <em>${data.message}</em>
                `;
                authResult.style.color = "lime";
                disableInputs();
            } else {
                triggerCurse(data.error);
            }
        } catch (error) {
            triggerCurse("❌ The Pharaoh’s magic prevents access!");
        }
    }

    // 🔥 Funktion för att trigga förbannelsen om något går fel
    function triggerCurse(errorMessage) {
        authResult.innerHTML = `⚠️ ${errorMessage}`;
        authResult.style.color = "red";
        authResult.classList.add("curse"); // Lägg till skakeffekt
        setTimeout(() => authResult.classList.remove("curse"), 1000);
    }

    // 🔥 Funktion för att inaktivera inputfälten när flaggan hittas
    function disableInputs() {
        passwordField.disabled = true;
        twoFAField.disabled = true;
    }

    // Gör funktionen globalt tillgänglig
    window.submitFlag = submitFlag;
});
