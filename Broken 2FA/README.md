🔐 Broken 2FA – Pharaoh's Vault

🔧 Steg 1: Registrera en användare

Gå till /register och skapa ett konto.

Du omdirigeras till /login.

🔑 Steg 2: Logga in och få din 2FA-kod

Logga in via /login.

Du hamnar på /verify_2fa och får en kod (men du behöver inte använda den).

💥 Steg 3: Exploatera buggen med Burp Suite

Öppna Burp Suite → Intercept ON.

Gå till /verify_2fa, fyll i formuläret och skicka.

Fånga requesten i Burp och ändra:

2fa=000000&verified=true

Skicka iväg requesten → du blir inloggad och skickas till /game.

🏺 Steg 4: Lås upp vaulten

Gå till /game.

Fyll i lösenordet: 𓂀𓏏𓆣𓊪

Klicka på "Unlock the Vault"

🏆 Flagga: O24{PHARAOHS_2FA_BROKEN}

❗ Varför fungerar det?

Servern accepterar verified=true som bevis på att 2FA är godkänd.

Flask-sessionen sparar detta och hoppar över verifiering.
