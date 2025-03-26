# 🧙‍♂️ Walkthrough – The Oracle of Thebes (SSRF)

## 🧩 Challenge Summary

> "Consult the Oracle. Ask the right question. Uncover the forbidden scroll."

You are presented with a mysterious web interface where you may enter a URL and receive a response.  
The server fetches the content and returns it — a strong hint toward a **Server-Side Request Forgery (SSRF)** vulnerability.

---

## 🎯 Goal

Find the hidden flag located on an internal backend service (`internal-api`), which is **only accessible** from the oracle server (via SSRF).

---

## 🧪 Step-by-step Solution

### 1. Try a normal external URL:
