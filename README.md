# 🏢 Proiect Gestiune Asociație "Bloc X69"

Aplicație web dezvoltată în **Python (Flask)** cu backend în **PostgreSQL**, destinată managementului financiar și administrativ al unei asociații de proprietari.

---

## 🏗️ Arhitectură

Proiectul este structurat pe clase conform diagramelor UML (Use-Case, Class, Sequence, Activity, ER):

```
proiect7_asociatie/
├── app2.py                        # Rutele Flask (slim, fără logică de business)
├── app.py                         # Versiunea originală (backup)
├── database.py                    # Conexiunea la PostgreSQL
├── calculator_intretinere.py      # Script utilitar pentru calcul rapid în terminal
├── test_app2.py                   # 15 teste automate cu Pytest
├── models/
│   ├── user.py                    # Clasele User și Administrator
│   ├── apartment.py               # Clasele Apartment, Locatar, WaterConsumption
│   ├── financial_manager.py       # Clasa FinancialManager (formula REQ-41)
│   ├── supplier.py                # Clasele Supplier și Invoice
│   └── payment.py                 # Clasa Payment
├── templates/                     # Paginile HTML (Jinja2)
└── static/                        # CSS și resurse frontend
```

### Clase principale

| Clasă | Fișier | Responsabilitate |
|---|---|---|
| `User` | `models/user.py` | Autentificare, logout, reset parolă |
| `Administrator` | `models/user.py` | Rapoarte, facturi, contracte (extinde User) |
| `FinancialManager` | `models/financial_manager.py` | Calculul cotelor lunare (REQ-41) |
| `Apartment` | `models/apartment.py` | Gestiunea apartamentelor |
| `Locatar` | `models/apartment.py` | Plăți online, istoric, indici apă |
| `Supplier` + `Invoice` | `models/supplier.py` | Furnizori și facturi |
| `Payment` | `models/payment.py` | Înregistrarea plăților locatarilor |

---

## 📋 Pre-condiții

- **Python 3.12+** instalat
- **PostgreSQL 18** instalat și pornit
- **Git** instalat (pentru clonare)

---

## 🚀 Instalare și Configurare

### 1. Clonarea Repositoriului

```bash
git clone https://github.com/StanMarian1/Proiect---Asociatie-de-locatari.git
cd Proiect---Asociatie-de-locatari
```

### 2. Configurarea Bazei de Date

1. Deschide **pgAdmin 4** și creează o bază de date nouă numită `asociatie_db`
2. Deschide un **Query Tool** pe această bază de date
3. Rulează scriptul `baza_de_date.sql` pentru a crea structura tabelelor
4. Rulează scriptul de populare pentru a introduce datele inițiale

> **⚠️ Important:** Deschide `database.py` și asigură-te că parola pentru userul `postgres` coincide cu cea setată la instalarea PostgreSQL:
> ```python
> conn = psycopg2.connect(
>     dbname="asociatie_db",
>     user="postgres",
>     password="PAROLA_TA",  # <- modifică aici
>     host="localhost",
>     port="5432"
> )
> ```

### 3. Instalarea Dependențelor

```bash
pip install -r requirements.txt
```

### 4. Validarea Proiectului (Testare Automată)

Rulează cele **15 teste automate** pentru a verifica integritatea aplicației:

```bash
python -m pytest test_app2.py -v
```

Rezultat așteptat: **15 passed**

### 5. Pornirea Aplicației

```bash
python app2.py
```


---

## 🔐 Date de Acces

| Rol | Utilizator | Parolă |
|---|---|---|
| **Administrator** | `admin` | `1234` |
| **Administrator** | `admin_asociatie` | `parola_admin123` |
| **Locatar** | `m.ionescu` | `parola123` |
| **Locatar** | `familia.popa` | `parola123` |

---

## 📐 Formula de Calcul Întreținere (REQ-41)

```
Sumă Apartament = ((Total Facturi + Total Salarii) / Total Camere)
                  × Camere Apartament × (Nr. Locatari × 0.5)
```

Pentru a vedea calculele rapid în terminal, fără să pornești serverul:

```bash
python calculator_intretinere.py
```

---

## 🛠️ Tehnologii Folosite

| Componentă | Tehnologie |
|---|---|
| Backend | Python 3.12 / Flask |
| Bază de date | PostgreSQL 18 |
| ORM / DB Driver | psycopg2 |
| Testare | Pytest + unittest.mock |
| Frontend | HTML5, CSS3, Jinja2 |
| Versionare | GitHub |
