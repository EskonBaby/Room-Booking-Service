## Setup-Anleitung
**Backend (FastAPI):**
1. Ins Verzeichnis `/backend` wechseln (im Terminal "cd backend" eingeben).
2. `pip install fastapi uvicorn pydantic` ausführen (falls Sie fastapi nicht installiert haben).
3. Den Server starten mit: `py -m uvicorn main:app --host 127.0.0.1 --port 9999 --reload` (läuft auf Port 9999. Das ist leider so Hardcoded. Ich habe den Port 8000 versucht aber das hat leider nicht geklappt.).

**Frontend (Vue 3):**
1. Ins Verzeichnis `/frontend` wechseln (in einem neuen Terminal "cd frontend" eingeben. Insgesamt sollen zwei Terminals gleichzeitig laufen.)
2. `npm install` ausführen (Node.js muss schon installiert werden).
3. App starten mit: `npm run dev` (läuft auf Port 5173).
4. http://localhost:5173/ im Browser öffnen.

**Hinweis:** Nachdem Löschen einer Buchung gehen Sie zurück zu "Find Room" und aktualisieren Sie die Seite. Danach soll der Raum in dem "Available" Teil erscheinen.

## Lösungsansatz & Entscheidungen
Das primäre Ziel dieser Lösung war es, den fehleranfälligen Chat-Prozess durch eine strukturierte, nachvollziehbare Buchungslogik abzulösen. 
- **Fokus auf Kernanforderungen:** Die App ermöglicht die Anzeige, Reservierung und eine Klare übersichtliche Darstellung der Räumen und Buchungen.
- **Schwerpunkte:** 
1) **Statusanzeige:** Jeder Raum verfügt über einen Status entweder "Available" oder "Unavailable" für eine gegebene Start-und-End Time.
2) **Zeitdisplay:** Ich bin davon ausgegangen, dass die Firma von 8:00 bis 19:00 offen hat und die Start und End Zeit der Reservierung können um 15 minuten inkrementiert werden. D.h die Form "Start Time" zeigt die Uhrzeiten von 8:00 bis 18:45 und die Form "End Time" zeigt 8:15 bis 19:00. Ebenfalls wird bei der Start Time die Zeit ab der nächstmögliche Uhrzeit. Also keine Buchungen in der Vergangenheit.
3) **Konfliktverhütung:** Mit Konflikte wird umgegangen, indem die derzeit ausgewählte Start und End Zeit mit dem Zeitraum jeder Buchung verglichen wird und dann anhand davon wir entschieden, ob der Raum in "Available" oder "Unavailable" gezeigt wird.


- **Herausforderung:** Aufgrund der zeitlichen Begrenzung und die Nebenläufige Praktika an der Uni und da Fastapi und Vue komplett neu für mich sind, musste ich sehr viel, zumindest die Grundlagen, in kurze Zeit lernen um etwas Vernünftiges liefern zu können.
- **KI Nutzung:** Um Transparent zu sein, KI wurde zwar benutzt aber gezielt. Da die Werkzeuge (also Vue und fastapi) komplett neu für mich sind, müsste ich bei manche probleme die Ki nach hilfe fragen, z.b wie ein paar Funktionalitäten entwickelt werden können oder auch bei fehler behebung. Damit habe ich neue Ansätze gelernt und viele Funktionen entwickelt, die ich alleine mit begrenzter Zeit und Kenntnisse wahrscheinlich nicht erledigen könnte. Darüber hinaus habe ich zuerst einen kleinen Prototyp der Website mit Figma erstellt damit ich einen überblick verschaffe, wie die website aussehen könnte und das hat die Konzeption erheblich beschleunigt. 

## Was ich mit mehr Zeit erweitern würde
- **Persistente Datenbank:** Integration von DatenBanken (z.B. SQLite oder Postgres), damit Buchungen dauerhaft gespeichert werden.
- **Benutzerverwaltung (Authentifizierung):** Statt den Namen und Id per Textfeld einzugeben, sollten Nutzer sich einloggen können (z.B. mit JWT-Token).
