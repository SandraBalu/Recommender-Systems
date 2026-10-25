# Lab 02 — Sistem de recomandare cu Recombee: înregistrare proprietăți

## Dataset ales: Movies (1980–2020)

**Fișier:** `movies.csv`  
**Număr de înregistrări:** 7.668 filme  
**Sursă:** [Movie-Data-Analysis](https://github.com/1tannu5/Movie-Data-Analysis)  
**Domeniu:** Cinematografie / Filme

## Descriere

Dataset-ul conține informații despre filme lansate între 1980 și 2020, incluzând titlul, genul, scorul IMDb, regizorul, clasificarea de vârstă și durata. Datele sunt folosite pentru a construi un sistem de recomandare de filme.

## Proprietăți înregistrate în Recombee

| Proprietate | Tip de date | Descriere | Exemplu |
|---|---|---|---|
| `genre` | string | Genul filmului | "Drama", "Action" |
| `year` | int | Anul lansării | 1980 |
| `score` | double | Scorul IMDb (0–10) | 8.4 |
| `director` | string | Numele regizorului | "Stanley Kubrick" |
| `rating` | string | Clasificare de vârstă | "R", "PG", "PG-13" |
| `runtime` | int | Durata în minute | 146 |

## Rulare script

```bash
# Instalare dependențe
pip install recombee-api-client pandas python-dotenv

# Copiere fișier credențiale
cp .env.example .env
# Completați .env cu datele din contul Recombee

# Rulare script
python recombee_properties.py
```

## Structura fișierelor

```
lab02/
├── recombee_properties.py   # Script principal
├── movies.csv               # Dataset filme
├── .env                     # Credențiale Recombee (nu se urcă pe GitHub)
├── .env.example             # Template credențiale
└── README.md                # Documentație
```
