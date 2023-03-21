Instruktioner för att få igång flask-appen

LÄNK TILL REPO: https://github.com/CharlieRosander/kaliberTestPage

1. Skapa en tom mapp för projektet och extrahera rar filen i den, använder du GitHub så klonar du repon till valfri plats
2. Navigera till den mappen i powershell och skapa venv:en med python -m venv venv
3. Aktivera venv-skriptet
4. Projektet innehåller en txt-fil med modulerna som krävs, kör därför "pip install -r reqs.txt"
5. Starta med flask run --debug

OBS: Jag har för skojs skull integrerat 2st APIs i appen, en väder api från openweathermap, 
samt en äldre modell av ChatGPT från OpenAI. 

För att dessa ska fungera (Detta är frivilligt, går att skippa)
så behövs API-keys, dom får du om du vill, skaffa själv och skriva in i .env filen så kommer dom att läsas av med
python-dotenv paketet.

Appen har också en signup/login page (också bara för skojsskull), där informationen hanteras av en lokal sqlite databas
som skapas per defualt i instance-foldern i projektmappen.
