from Crypto.Cipher import AES
import base64
import os

# 🔑 Generera en svag 16-byte nyckel (t.ex. "pharaohpharaoh12")
KEY = b'pharaohpharaoh12'  # Detta är en statisk och osäker nyckel (medvetet svag för CTF)

# 🚀 Läs flaggan från `flag.txt`
FLAG_FILE = "flag.txt"
if not os.path.exists(FLAG_FILE):
    print("[ERROR] flag.txt saknas! Skapa en fil med flaggan.")
    exit(1)

with open(FLAG_FILE, "rb") as f:
    plaintext = f.read()

# 📦 AES-kryptering med ECB (dåligt och medvetet sårbart!)
cipher = AES.new(KEY, AES.MODE_ECB)
padded_plaintext = plaintext + b' ' * (16 - len(plaintext) % 16)  # Pad till multipel av 16
ciphertext = cipher.encrypt(padded_plaintext)

# 📂 Spara den krypterade filen
with open("static/secrets.enc", "wb") as f:
    f.write(ciphertext)

print("[✔] Kryptering klar! `static/secrets.enc` skapad.")
print("[!] OBS: Svag kryptering används (AES-ECB, statisk nyckel). Studenter kan brute-force'a eller analysera mönster.")
