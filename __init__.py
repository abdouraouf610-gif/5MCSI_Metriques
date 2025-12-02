from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen, Request
import sqlite3
                                                                                                                                       
app = Flask(__name__)                                                                                                                  
                                                                                                                                       
@app.route("/contact/")
def contact():
    return render_template("contact.html")
  
@app.route("/contact/")
def MaPremiereAPI():
    return "<h2>Ma page de contact</h2>"

@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def histogramme():
    return render_template("histogramme.html")
@app.route('/commits_data/')
def commits_data():
    # API GitHub donnée dans l’énoncé
    api_url = "https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits"

    # GitHub demande d’avoir un User-Agent dans l’en-tête HTTP
    req = Request(api_url, headers={"User-Agent": "MetriquesApp"})
    response = urlopen(req)
    raw_content = response.read()
    commits = json.loads(raw_content.decode('utf-8'))

    # Dictionnaire minute -> nombre de commits
    commits_per_minute = {}

    for commit in commits:
        # Récupération de la date du commit
        date_str = commit.get('commit', {}).get('author', {}).get('date')
        if not date_str:
            continue

        # Exemple de format : "2024-02-11T11:57:27Z"
        date_object = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
        minute = date_object.minute  # extrait la minute (0–59)

        # Incrémentation du compteur pour cette minute
        commits_per_minute[minute] = commits_per_minute.get(minute, 0) + 1

    # On transforme le dictionnaire en liste triée (plus pratique pour le front)
    results = [
        {"minute": minute, "count": commits_per_minute[minute]}
        for minute in sorted(commits_per_minute.keys())
    ]

    return jsonify(results=results)
@app.route('/commits/')
def commits():
    return render_template('commits.html')  
if __name__ == "__main__":
  app.run(debug=True)
