from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)

@app.route("/contact/")
def MaPremiereAPI():
    return render_template("contact.html")

@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15  # Conversion Kelvin en °C
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)                                                                                                            
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def histogramme():
    return render_template("histogramme.html")

@app.route('/commits/')
def commits():
    # Remplacez 'VOTRE-USERNAME' et 'VOTRE-REPO' par vos vraies valeurs
    # Exemple : https://api.github.com/repos/ryan-dupont/5MCSI_Metriques/commits
    response = urlopen('https://api.github.com/repos/ryanvaugarni/5MCSI_Metriques/commits')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    
    # Dictionnaire pour compter les commits par minute (0-59)
    commits_per_minute = {}
    for i in range(60):
        commits_per_minute[i] = 0
    
    # Parcourir tous les commits
    for commit in json_content:
        date_string = commit['commit']['author']['date']
        # Extraire les minutes de la date
        date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
        minutes = date_object.minute
        commits_per_minute[minutes] += 1
    
    # Préparer les résultats
    results = []
    for minute, count in commits_per_minute.items():
        results.append({'minute': minute, 'count': count})
    
    return jsonify(results=results)

@app.route("/commits-graph/")
def commits_graph():
    return render_template("commits.html")

@app.route("/contact/")
def MaPremiereAPI():
    return "<h2>Ma page de contact</h2>"

if __name__ == "__main__":
  app.run(debug=True)