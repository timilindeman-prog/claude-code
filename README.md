# Automatisk Omvärldsanalys

Ett AI-drivet system som automatiskt skapar djupgående omvärldsanalyser och skickar dem som snygga PDF-rapporter till din e-post varje månad.

## 📋 Översikt

Detta system:
- 🔍 Samlar in data om dina valda ämnesområden
- 🤖 Analyserar informationen med AI (Claude)
- 📊 Identifierar trender, mönster och insikter
- 📄 Genererar professionella PDF-rapporter
- 📧 Skickar rapporten till din e-post
- ⏰ Körs automatiskt en gång per månad

## 🚀 Snabbstart

### 1. Installation

```bash
# Klona eller ladda ner projektet
cd claude-code

# Installera beroenden
pip install -r requirements.txt
```

### 2. Konfiguration

**Skapa .env-fil:**

```bash
cp .env.example .env
```

Redigera `.env` och fyll i:
- `ANTHROPIC_API_KEY`: Din Anthropic API-nyckel (hämta från https://console.anthropic.com/)
- E-postinställningar (Gmail-exempel nedan)

**För Gmail:**
1. Gå till Google Account > Security
2. Aktivera 2-stegsinloggning
3. Skapa ett App Password (https://myaccount.google.com/apppasswords)
4. Använd app-lösenordet i `.env`

**Anpassa config.yaml:**

Redigera `config.yaml` för att välja:
- Ämnen du vill analysera
- Hur djup analysen ska vara
- PDF-inställningar
- Schema för körning

### 3. Kör systemet

**🌐 Webbgränssnitt (rekommenderas):**
```bash
cd web
python app.py
```
Öppna sedan http://localhost:5000 i din webbläsare.

**Kommandorad (CLI):**

Kör en gång (testa):
```bash
python main.py --once
```

Interaktivt läge:
```bash
python main.py
```

Schemalagd körning (daemon):
```bash
python main.py --daemon
```

## 📁 Projektstruktur

```
claude-code/
├── src/
│   ├── __init__.py
│   ├── data_collector.py    # Samlar in data från webben
│   ├── analyzer.py           # AI-driven analys med Claude
│   ├── pdf_generator.py      # Genererar snygga PDF-rapporter
│   ├── email_sender.py       # Skickar e-post med bilagor
│   └── scheduler.py          # Hanterar schemalagd körning
├── main.py                   # Huvudskript
├── config.yaml               # Konfiguration
├── .env                      # Miljövariabler (API-nycklar, etc.)
├── requirements.txt          # Python-beroenden
└── README.md                 # Denna fil
```

## ⚙️ Konfiguration

### config.yaml

```yaml
# Ämnen att analysera
topics:
  - "Artificiell intelligens och maskininlärning"
  - "Hållbarhet och klimatförändringar"
  - "Svensk ekonomi och näringsliv"
  # Lägg till dina egna ämnen här!

# Hur många källor per ämne
search:
  max_results_per_topic: 10
  language: "sv"  # sv eller en

# Analysdjup
analysis:
  depth: "deep"  # quick, standard eller deep
  include_recommendations: true
  include_trends: true

# PDF-inställningar
pdf:
  title: "Månatlig Omvärldsanalys"
  language: "sv"
  include_sources: true
```

### .env

```bash
# Anthropic API
ANTHROPIC_API_KEY=your_api_key_here

# E-post (Gmail-exempel)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_FROM=din.email@gmail.com
EMAIL_PASSWORD=ditt_app_lösenord

# Mottagare
EMAIL_TO=mottagare@example.com
```

## 📊 Vad innehåller rapporten?

PDF-rapporten innehåller:

1. **Sammanfattning** - Kort översikt av de viktigaste insikterna
2. **Ämnesanalyser** - Djupgående analys av varje valt ämne
3. **Övergripande insikter** - Kopplingar och samband mellan ämnen
4. **Identifierade trender** - De viktigaste trenderna som framträder
5. **Rekommendationer** - Konkreta handlingsförslag

## 🔄 Automatisk körning

### Schemalagd körning med systemd (Linux)

Skapa en systemd service:

```bash
sudo nano /etc/systemd/system/omvarldsanalys.service
```

Innehåll:
```ini
[Unit]
Description=Automatisk Omvärldsanalys
After=network.target

[Service]
Type=simple
User=DIN_ANVÄNDARE
WorkingDirectory=/sökväg/till/claude-code
ExecStart=/usr/bin/python3 main.py --daemon
Restart=always

[Install]
WantedBy=multi-user.target
```

Aktivera och starta:
```bash
sudo systemctl enable omvarldsanalys
sudo systemctl start omvarldsanalys
sudo systemctl status omvarldsanalys
```

### Cron-jobb (alternativ)

```bash
crontab -e
```

Lägg till (kör första dagen i månaden kl 09:00):
```
0 9 1 * * cd /sökväg/till/claude-code && /usr/bin/python3 main.py --once >> analysis.log 2>&1
```

## 🛠️ Avancerad användning

### Anpassa datainsamling

Redigera `src/data_collector.py` för att:
- Integrera med riktiga nyhetskällor (NewsAPI, Google News, etc.)
- Lägga till specifika RSS-feeds
- Scrapa specifika webbplatser

### Anpassa PDF-design

Redigera `src/pdf_generator.py` för att:
- Ändra färger och typsnitt
- Lägga till företagslogotyp
- Anpassa layout och struktur

### Anpassa AI-analysen

Redigera `src/analyzer.py` för att:
- Ändra analysdjup och fokus
- Lägga till specifika analysramar
- Anpassa till din bransch eller sektor

## 📝 Loggning

Systemet skapar automatiskt loggfiler:
- `analysis_scheduler.log` - Loggar schemalagda körningar
- Kör med `>> analysis.log 2>&1` för att logga output

## 🔒 Säkerhet

**Viktigt:**
- Dela ALDRIG din `.env`-fil
- `.env` är redan i `.gitignore`
- Använd app-specifika lösenord för e-post
- Rotera API-nycklar regelbundet

## 🐛 Felsökning

**"ANTHROPIC_API_KEY saknas"**
- Kontrollera att `.env` existerar och innehåller giltig API-nyckel

**"E-post kunde inte skickas"**
- Kontrollera SMTP-inställningar
- För Gmail: använd app-lösenord (inte vanligt lösenord)
- Kontrollera att 2-stegsinloggning är aktiverad

**"PDF genereras inte"**
- Kontrollera att weasyprint är installerat korrekt
- På Linux kan du behöva: `sudo apt-get install python3-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0`

## 📚 Teknisk stack

- **Python 3.8+**
- **Claude API** (Anthropic) - AI-analys
- **WeasyPrint** - PDF-generering
- **Schedule** - Schemaläggning
- **SMTP** - E-postutskick

## 🤝 Bidra

Vill du förbättra systemet? Pull requests välkomnas!

## 📄 Licens

MIT License - Använd fritt!

## 📧 Support

För frågor eller problem, öppna ett issue på GitHub.

---

**Skapad med AI-teknologi för att göra omvärldsbevakning enklare och mer insiktsfullt.**
