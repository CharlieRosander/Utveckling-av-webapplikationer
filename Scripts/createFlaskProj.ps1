Write-output 'SCRIPT WRITTEN BY KALIBER'
Write-output 'Running script....'

Write-output ' '
Write-output 'Creating flask enviroment, please wait...'
python -m venv venv

Write-output '-------------------------------------------------'
Write-output ' '
Write-output 'Creating app.py file, please wait...'
New-item app.py
Write-output ' '
Write-output '-------------------------------------------------'

timeout 2
Write-output ' '

Write-output '-------------------------------------------------'
Write-output ' '
Write-output 'Setting content of app.py, please wait...'
Set-content app.py 'from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"'
    
Write-output ' '
Write-output '-------------------------------------------------'
Write-output ' '
Write-output 'Activating venv script, please wait...'
venv\scripts\activate
Write-output ' '
Write-output '-------------------------------------------------'

timeout 2
Write-output ' '

Write-output '-------------------------------------------------'
Write-output ' '
Write-output 'Running pip install flask, please wait...'
pip install flask
Write-output ' '
Write-output '-------------------------------------------------'

Write-output 'CLEARING SCREEN'
timeout 3
Write-output ' '

Clear-Host

Write-output '-------------------------------------------------'
Write-output ' '
Write-output 'All done!'
