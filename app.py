from flask import Flask, render_template, request, redirect, url_for, flash
import pymongo

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MongoDB Verbindung
client = pymongo.MongoClient("mongodb://root:root@localhost:27017/")
database = client["QuizGame"]
statistics_collection = database["statistics"]
questions_collection = database["questions"]
answers_collection = database["answers"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_quiz', methods=['POST'])
def start_quiz():
    selected_category = request.form['category']

    if selected_category.isdigit():
        selected_category = int(selected_category)

        if 1 <= selected_category <= 4:
            category_name = get_category_name(selected_category)
            flash(f'Du hast die Kategorie {category_name} ausgewählt.', 'info')
            # Weitere Logik für das Quiz kann hier hinzugefügt werden
        else:
            flash('Ungültige Auswahl. Bitte wähle eine Zahl von 1 bis 4.', 'error')
    else:
        flash('Ungültige Eingabe. Bitte gib eine Zahl ein.', 'error')

    return redirect(url_for('index'))

def get_category_name(category_number):
    categories = {
        1: "Geschwindigkeit",
        2: "Baujahr",
        3: "Preis",
        4: "Anzahl PS"
    }
    return categories.get(category_number, "Unbekannte Kategorie")

if __name__ == '__main__':
    app.run(debug=True)
