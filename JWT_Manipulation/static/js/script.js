document.addEventListener("DOMContentLoaded", function() {
    const loginButton = document.querySelector("button");
    const message = document.getElementById("message");

    if (loginButton) {
        loginButton.addEventListener("click", function() {
            let username = document.getElementById("username").value.trim();

            if (!username) {
                message.innerHTML = "⚠️ Please enter your name!";
                return;
            }

            fetch("/login", {
                method: "POST",
                headers: { "Content-Type": "application/x-www-form-urlencoded" },
                body: `username=${encodeURIComponent(username)}`
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Server responded with ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                if (data.token) {
                    // Set the cookie properly
                    document.cookie = `auth_token=${data.token}; path=/; Secure; SameSite=None`;

                    // Decode JWT-token payload safely
                    try {
                        const base64Payload = data.token.split('.')[1];
                        const decodedPayload = JSON.parse(atob(base64Payload));

                        console.log("JWT Payload:", decodedPayload);

                        if (decodedPayload.role && decodedPayload.role.toLowerCase() === "admin") {
                            message.innerHTML = "✅ Welcome, mighty Pharaoh! Proceed to <a href='/admin'>Admin Chamber</a>";
                        } else {
                            message.innerHTML = "✅ Login successful! But are you truly worthy? 👀";
                        }
                    } catch (e) {
                        console.error("Failed to decode JWT payload:", e);
                        message.innerHTML = "❌ Something went wrong decoding the token!";
                    }
                } else {
                    message.innerHTML = "❌ Login failed! No token received.";
                }
            })
            .catch(error => {
                console.error("Fetch Error:", error);
                message.innerHTML = "❌ Error connecting to server!";
            });
        });
    }
});

