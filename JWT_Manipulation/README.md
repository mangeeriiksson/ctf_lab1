# 🧾 JWT Manipulation – Psychic Signatures Edition (CVE-2022-21449 Inspired)

## 🎯 Mål
Få åtkomst till `/admin` och avslöja den gömda flaggan genom att manipulera JWT-signaturen.

---

## 🔐 Bakgrund

Den här utmaningen simulerar en verklig JWT-sårbarhet som påverkade vissa versioner av Java (JDK 15–18).  
I dessa versioner kunde en angripare skicka en JWT med en **ogiltig signatur** – där `r=0` och `s=0` i ECDSA – och servern **accepterade den ändå**.

Vi återskapar denna sårbarhet i Flask/Python för att du ska förstå riskerna med felaktig signaturverifiering.

---

## 🧪 Steg-för-steg: Utnyttja sårbarheten

### 1️⃣ Skapa JWT-token med `alg: ES256`

Gå till 👉 [https://token.dev](https://token.dev)

1. Välj algoritm: **ES256**
2. Fyll i Payload:

```json
{
  "username": "admin",
  "role": "admin",
  "exp": 9999999999
}
