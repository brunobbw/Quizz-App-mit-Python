import pymongo

# Verbindung zu MongoDB herstellen (stellen Sie sicher, dass Ihr Docker-Container läuft)
client = pymongo.MongoClient("mongodb://root:root@localhost:27017/")

# Datenbank und Sammlung auswählen
db = client['QuizGame']
user_collection = db['statistic']
question_collection = db['questions']
car_collection = db['cars']


# Benutzernamen vom Terminal einlesen
user_name = input("Wie heißt du? ")

userPipeline = [
  {
    "$match": {
      "Name": user_name,
    }
  }
]

# Benutzer suchen
userStatus = user_collection.aggregate(userPipeline)

existing_user = next(userStatus, None)

if existing_user:
    print(f"Willkommen zurück, {user_name}!")
else:
    print(f"Willkommen als neuer Benutzer, {user_name}!")
    # Neuen Benutzer zur Datenbank hinzufügen
    new_user_data = {"Name": user_name, "score": 0}
    user_collection.insert_one(new_user_data)



# Kategorie auswählen
print("Wähle eine Kategorie aus:")
print("1. Geschwindigkeit")
print("2. Herstellungsjahr")
print("3. Preis")
print("4. Anzahl PS")

selected_category = input("Kategorie:")



# Überprüfen, ob die Eingabe eine gültige Zahl ist
if selected_category.isdigit():
    selected_category = int(selected_category)

    # Ausgabe je nach Benutzerauswahl
    if selected_category == 1:
        print("Du hast die Kategorie Geschwindigkeit ausgewählt.")
        print("")


        # ---------- Abschnitt Frage anzeigen ----------

        # Pipeline erstellen, um nur die Frage "FrageZuGeschwindigkeit" anzuzeigen
        speed_pipeline = [
    {
        "$match": {
            "FrageZuGeschwindigkeit": "Welches Auto ist das 2 schnellste?"
        }
    },
    {
        "$project": {
            "_id": 0,  # Exclude _id field
            "FrageZuGeschwindigkeit": 1  # Include only FrageZuGeschwindigkeit field
        }
    }
]

        # Frage suchen
        questions = question_collection.aggregate(speed_pipeline)

        for question in questions:
            print(question["FrageZuGeschwindigkeit"])

        # ---------- Abschnitt Autos anzeigen ----------

        # Hier drei zufällige Autos auswählen und anzeigen
        random_cars_pipeline = [
            {"$sample": {"size": 3}},
            {"$project": {"_id": 0}}
        ]

        # Zufällige Autos suchen
        random_cars = list(car_collection.aggregate(random_cars_pipeline))

        # Zuordnung von Zahlen zu Autos erstellen
        car_mapping = {str(i + 1): car["Name"] for i, car in enumerate(random_cars)}

        while True:
            for number, car_name in car_mapping.items():
                print(f"{number}. {car_name}")

            # Das zweitschnellste Auto finden
            second_fastest_car = car_collection.find_one({"Geschwindigkeit": {"$eq": sorted(car["Geschwindigkeit"] for car in random_cars)[1]}}, {"_id": 0})

            # User Option vom Terminal einlesen
            user_choice_number = input("Wähle das Auto: ")

            # Überprüfen, ob die Eingabe eine gültige Zahl ist
            if user_choice_number in car_mapping:
                user_choice = car_mapping[user_choice_number]

                if user_choice == second_fastest_car["Name"]:
                    print(f"Richtig!! Das zweitschnellste Auto ist {second_fastest_car['Name']}")

                    # Punktestand des aktuellen Spielers erhöhen
                    user_collection.update_one({"Name": user_name}, {"$inc": {"score": 1}})

                elif user_choice != second_fastest_car["Name"]:
                    print("Leider falsch... Die richtige Antwort ist:", second_fastest_car["Name"])

            else:
                print("Ungültige Auswahl. Bitte wähle eine Zahl von 1 bis 3. Versuche es erneut.")
                print("")






    elif selected_category == 2:
        print("Du hast die Kategorie Herstellungsjahr ausgewählt.")



    elif selected_category == 3:
        print("Du hast die Kategorie Preis ausgewählt.")



    elif selected_category == 4:
        print("Du hast die Kategorie Anzahl PS ausgewählt.")



    else:
        print("Ungültige Auswahl. Bitte wähle eine Zahl von 1 bis 4.")
        category_questions = None



# Verbindung trennen (optional, wird normalerweise nicht benötigt)
client.close()
