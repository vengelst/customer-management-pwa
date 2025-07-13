# Kundenverwaltungs-App (Customer Management System)

Eine fortschrittliche Flask-basierte Kundenverwaltungsanwendung für professionelles Kontakt- und Beziehungsmanagement mit Progressive Web App (PWA) Funktionalität.

## ✨ Hauptfunktionen

### 📱 Progressive Web App
- **Installierbar** auf iOS und Android als native App
- **Offline-Funktionalität** für Kerndaten
- **App-Icons** und Splash-Screen
- **Push-Benachrichtigungen** (zukünftig)

### 👥 Kundenverwaltung
- Vollständige Kundendatenbank mit Kategorien
- Mehrere Kontakte pro Kunde
- Terminplanung und -verwaltung
- Suchfunktion über alle Felder
- Druckfähige Kundenblätter

### 📄 Dokumentenmanagement
- **Drei Upload-Methoden:**
  - Traditioneller File-Upload
  - Drag & Drop Interface
  - **Mobile Kamera-Scanning** mit Tap-to-Capture
- Unterstützte Formate: PDF, Word, Excel, PowerPoint, Bilder
- Dokumentenvorschau und -download
- Tags und Beschreibungen

### 🎨 Benutzerfreundlichkeit
- **Responsive Design** für alle Geräte
- **Dark Theme** mit Bootstrap
- **Intuitive Popups** mit Kundendetails
- **Mobile-optimierte** Bedienung
- **Touch-freundliche** Interfaces

## 🚀 Technologie-Stack

### Backend
- **Flask** - Python Web Framework
- **SQLAlchemy** - ORM für PostgreSQL
- **PostgreSQL** - Datenbank
- **Gunicorn** - WSGI Server

### Frontend
- **Bootstrap 5** - CSS Framework (Dark Theme)
- **Font Awesome 6** - Icons
- **Vanilla JavaScript** - Interaktivität
- **Service Worker** - PWA Funktionalität

### Features
- **Responsive Design** für Desktop und Mobile
- **Kamera-Integration** für Dokument-Scanning
- **Offline-Unterstützung** durch Service Worker
- **Print-Optimierung** für Kundenblätter

## 📦 Installation

### Voraussetzungen
- Python 3.9+
- PostgreSQL
- Git

### Setup
1. Repository klonen:
```bash
git clone https://github.com/yourusername/customer-management-app.git
cd customer-management-app
```

2. Virtuelle Umgebung erstellen:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# oder
venv\Scripts\activate  # Windows
```

3. Abhängigkeiten installieren:
```bash
pip install -r requirements.txt
```

4. Umgebungsvariablen setzen:
```bash
export DATABASE_URL="postgresql://user:password@localhost/dbname"
export SESSION_SECRET="your-secret-key"
```

5. Datenbank initialisieren:
```bash
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

6. App starten:
```bash
python main.py
```

## 🎯 Verwendung

### Kunden verwalten
1. Neue Kunden über "Neuer Kunde" anlegen
2. Kategorien zuweisen: "neu", "Interesse", "Bedarf", "kein Bedarf"
3. Kontakte zu Kunden hinzufügen
4. Termine planen und verwalten

### Dokumente hochladen
1. Zu einem Kunden navigieren
2. "Dokumente" → "Dokument hochladen"
3. **Drei Optionen:**
   - **Datei Upload:** Klassische Dateiauswahl
   - **Drag & Drop:** Dateien in Browser ziehen
   - **Mobile Scan:** Kamera öffnen und antippen für Foto

### PWA Installation
#### iOS (iPhone/iPad):
1. App in Safari öffnen
2. "Teilen" → "Zum Home-Bildschirm"
3. App wie native App nutzen

#### Android:
1. "Installieren" Button klicken
2. App wird zum Home-Screen hinzugefügt

## 🗂️ Projektstruktur

```
customer-management-app/
├── app.py                 # Flask App Konfiguration
├── main.py               # Haupteinstiegspunkt
├── routes.py             # URL-Routen und Logik
├── models.py             # Datenbankmodelle
├── static/
│   ├── css/
│   │   └── custom.css    # Benutzerdefinierte Styles
│   ├── js/
│   │   ├── app.js        # Hauptlogik
│   │   └── popup.js      # Popup-Funktionalität
│   ├── icons/            # PWA Icons
│   ├── screenshots/      # PWA Screenshots
│   ├── manifest.json     # PWA Manifest
│   └── sw.js            # Service Worker
├── templates/            # HTML Templates
│   ├── base.html        # Basis-Template
│   ├── index.html       # Startseite
│   ├── customer_*.html  # Kunden-Templates
│   └── document_*.html  # Dokument-Templates
├── uploads/             # Hochgeladene Dateien
└── PWA_iOS_Anleitung.md # iOS Installation Guide
```

## 🎨 Design-Prinzipien

### Mobile-First
- Touch-optimierte Bedienung
- Responsive Layout
- Schnelle Ladezeiten
- Offline-Funktionalität

### Benutzerfreundlichkeit
- Intuitive Navigation
- Klare Kategorisierung
- Schnelle Suchfunktion
- Informative Popups

### Professionelles Design
- Konsistentes Dark Theme
- Moderne Icons
- Klare Typographie
- Barrierefreie Bedienung

## 🔧 Konfiguration

### Umgebungsvariablen
```bash
DATABASE_URL=postgresql://user:pass@host:port/dbname
SESSION_SECRET=your-secret-key-here
FLASK_ENV=development  # oder production
```

### PWA Einstellungen
- Anpassung in `static/manifest.json`
- Icons in `static/icons/`
- Service Worker in `static/sw.js`

## 📱 Mobile Features

### Kamera-Integration
- Direkte Kamera-Nutzung im Browser
- Tap-to-Capture Funktionalität
- Automatische Bildoptimierung
- Speicherung als JPG

### Touch-Optimierung
- Große Touch-Targets
- Swipe-Gesten (geplant)
- Haptic Feedback (geplant)
- Landscape/Portrait Support

## 🛡️ Sicherheit

### Datenschutz
- Sichere Passwort-Hashing
- Session-Management
- CSRF-Schutz
- SQL-Injection Schutz

### Dateien
- Validierung von Dateitypen
- Sichere Dateinamen
- Größenbeschränkungen
- Virenscanning (empfohlen)

## 🚀 Deployment

### Produktionsserver
```bash
gunicorn --bind 0.0.0.0:5000 --workers 4 main:app
```

### Docker (Optional)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]
```

## 📈 Zukünftige Features

### Geplante Erweiterungen
- [ ] Push-Benachrichtigungen
- [ ] Kalender-Integration
- [ ] Export-Funktionen (Excel, PDF)
- [ ] Erweiterte Suchfilter
- [ ] Backup-System
- [ ] Multi-User Support
- [ ] API-Schnittstelle
- [ ] Reporting Dashboard

### Mobile Verbesserungen
- [ ] Offline-Synchronisation
- [ ] Swipe-Gesten
- [ ] Voice-to-Text
- [ ] Barcode-Scanner
- [ ] GPS-Integration

## 🤝 Beitragen

1. Fork das Repository
2. Feature-Branch erstellen (`git checkout -b feature/AmazingFeature`)
3. Änderungen committen (`git commit -m 'Add some AmazingFeature'`)
4. Branch pushen (`git push origin feature/AmazingFeature`)
5. Pull Request erstellen

## 📄 Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert - siehe [LICENSE](LICENSE) für Details.

## 🙏 Danksagungen

- Flask Community für das großartige Framework
- Bootstrap Team für das UI Framework
- Font Awesome für die Icons
- Replit für die Entwicklungsumgebung

## 📞 Support

Bei Fragen oder Problemen:
1. GitHub Issues verwenden
2. Dokumentation prüfen
3. Community fragen

---

**Entwickelt mit ❤️ für effiziente Kundenverwaltung**