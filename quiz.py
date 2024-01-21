import pymongo
import time

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
    print("--------------------------------")
    print("")
    print("Möchtest du die Rangliste sehen?")
    showStatistic = input("ja oder nein:")

    if showStatistic == "nein":
        print("In Ordnung! Das Spiel startet!")
        print("")

    else:
        print("Hier die Rangliste: ")
        # Pipeline erstellen, um die Top 3 Spieler nach dem Punktestand zu sortieren
        top_players_pipeline = [
            {"$sort": {"score": -1, "time": 1}},
            # Absteigend nach Punktestand sortieren, aufsteigen nach Zeit sortieren
            {"$limit": 3},  # Ergebnisse auf die Top 3 Spieler begrenzen
            {"$project": {"_id": 0, "Name": 1, "score": 1, "time": 1}}  # Nur Name und Punktestand anzeigen
        ]

        # Top 3 Spieler suchen und anzeigen
        top_players = list(user_collection.aggregate(top_players_pipeline))

        print("\nTop 3 Spieler:")
        for rank, player in enumerate(top_players, start=1):
            print(f"{rank}. {player['Name']} - Punktestand: {player['score']} - {player['time']}Sek.")
        print("")

else:
    print(f"Willkommen als neuer Benutzer, {user_name}!")
    # Neuen Benutzer zur Datenbank hinzufügen
    new_user_data = {"Name": user_name, "score": 0, "time": 0}
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

        # Äußere Schleife für dreimalige Durchführung
        for attempt in range(1, 4):
            start_time = time.time()    # Startzeit für den Timer
            # ---------- Abschnitt Frage anzeigen ----------

            # Pipeline erstellen, um nur eine Frage zu Geschwindigkeit anzuzeigen
            geschwindigkeit_pipeline = [
                {
                    "$match": {
                        "FrageZuGeschwindigkeit": {"$exists": True}
                    }
                },
                {
                    "$project": {
                        "_id": 0,
                        "FrageZuGeschwindigkeit": 1
                    }
                }
            ]

            # Frage suchen
            question = question_collection.aggregate(geschwindigkeit_pipeline).next()

            print(question["FrageZuGeschwindigkeit"])

            # ---------- Abschnitt Autos anzeigen ----------

            # Hier drei zufällige Autos mit Geschwindigkeit auswählen und anzeigen
            random_cars_pipeline = [
                {"$match": {"Geschwindigkeit": {"$exists": True}}},
                {"$sample": {"size": 3}},
                {"$project": {"_id": 0, "Name": 1, "Geschwindigkeit": 1}}
            ]

            # Zufällige Autos suchen
            random_cars = list(car_collection.aggregate(random_cars_pipeline))

            # Zuordnung von Zahlen zu Autos erstellen
            car_mapping = {str(i + 1): car["Name"] for i, car in enumerate(random_cars)}

            for number, car_name in car_mapping.items():
                print(f"{number}. {car_name}")

            # User Option vom Terminal einlesen
            user_choice_number = input("Wähle das Auto: ")

            # Überprüfen, ob die Eingabe eine gültige Zahl ist
            if user_choice_number in car_mapping:
                user_choice = car_mapping[user_choice_number]

                # Das zweitschnellste Auto finden
                second_fastest_car = car_collection.find_one(
                    {"Geschwindigkeit": {"$eq": sorted(car["Geschwindigkeit"] for car in random_cars)[1]}}, {"_id": 0}) # Bestätigung durch Herr Ninivaggi, dass es eine Pipeline ist, daher ist das richtig so!

                if user_choice == second_fastest_car["Name"]:
                    print(f"Richtig!! Das zweit schnellste Auto ist {second_fastest_car['Name']}")
                    print("")

                    # Punktestand des aktuellen Spielers erhöhen
                    user_collection.update_one({"Name": user_name}, {"$inc": {"score": 1}}) # Bestätigung durch Herr Ninivaggi, dass es eine Pipeline ist, daher ist das richtig so!

                elif user_choice != second_fastest_car["Name"]:
                    print("Leider falsch... Die richtige Antwort ist:", second_fastest_car["Name"])
                    print("")

            end_time = time.time()  # Endzeit für den Timer
            time_to_play = round(end_time - start_time, 1)  # Berechnung der vergangenen Zeit und Zahl wird auf eine Nachkommastelle gerundet

            # Timerwert in der Datenbank aktualisieren
            user_collection.update_one({"Name": user_name}, {"$set": {"time": time_to_play}})

        print("--------------- Das Spiel ist zu Ende! ---------------\n")

        # Pipeline erstellen, um die Top 3 Spieler nach dem Punktestand zu sortieren
        top_players_pipeline = [
            {"$sort": {"score": -1, "time": 1}},  # Absteigend nach Punktestand sortieren, aufsteigen nach Zeit sortieren
            {"$limit": 3},  # Ergebnisse auf die Top 3 Spieler begrenzen
            {"$project": {"_id": 0, "Name": 1, "score": 1, "time": 1}}  # Nur Name und Punktestand anzeigen
        ]

        # Top 3 Spieler suchen und anzeigen
        top_players = list(user_collection.aggregate(top_players_pipeline))

        print("\nTop 3 Spieler:")
        for rank, player in enumerate(top_players, start=1):
            print(f"{rank}. {player['Name']} - Punktestand: {player['score']} - {player['time']}Sek.")








    elif selected_category == 2:
        print("Du hast die Kategorie Herstellungsjahr ausgewählt.")
        print("")

        # Äußere Schleife für dreimalige Durchführung
        for attempt in range(1, 4):
            start_time = time.time()  # Startzeit für den Timer
            # ---------- Abschnitt Frage anzeigen ----------

            # Pipeline erstellen, um nur eine Frage zu Herstellungsjahr anzuzeigen
            herstellungsjahr_pipeline = [
                {
                    "$match": {
                        "FrageZuHerstellungsjahr": {"$exists": True}
                    }
                },
                {
                    "$project": {
                        "_id": 0,
                        "FrageZuHerstellungsjahr": 1
                    }
                }
            ]

            # Frage suchen
            question = question_collection.aggregate(herstellungsjahr_pipeline).next()

            print(question["FrageZuHerstellungsjahr"])

            # ---------- Abschnitt Autos anzeigen ----------

            # Hier drei zufällige Autos mit Herstellungsjahr auswählen und anzeigen
            random_cars_pipeline = [
                {"$match": {"Herstellungsjahr": {"$exists": True}}},
                {"$sample": {"size": 3}},
                {"$project": {"_id": 0, "Name": 1, "Herstellungsjahr": 1}}
            ]

            # Zufällige Autos suchen
            random_cars = list(car_collection.aggregate(random_cars_pipeline))

            # Pipeline erstellen, um das älteste Auto zu finden
            oldest_car_pipeline = [
                {"$match": {"Name": {"$in": [car["Name"] for car in random_cars]}}},
                {"$sort": {"Herstellungsjahr": 1}},
                {"$limit": 1},
                {"$project": {"_id": 0, "Name": 1, "Herstellungsjahr": 1}}
            ]

            # Das älteste Auto finden
            oldest_car = car_collection.aggregate(oldest_car_pipeline).next()

            # Zuordnung von Zahlen zu Autos erstellen
            car_mapping = {str(i + 1): car["Name"] for i, car in enumerate(random_cars)}

            for number, car_name in car_mapping.items():
                print(f"{number}. {car_name}")

            # User Option vom Terminal einlesen
            user_choice_number = input("Wähle das Auto: ")

            # Überprüfen, ob die Eingabe eine gültige Zahl ist
            if user_choice_number in car_mapping:
                user_choice = car_mapping[user_choice_number]

                if user_choice == oldest_car["Name"]:
                    print(f"Richtig!! Das älteste Auto ist {oldest_car['Name']}")
                    print("")

                    # Punktestand des aktuellen Spielers erhöhen
                    user_collection.update_one({"Name": user_name}, {"$inc": {"score": 1}})
                else:
                    print(f"Leider falsch... Die richtige Antwort ist: {oldest_car['Name']}")
                    print("")

            end_time = time.time()  # Endzeit für den Timer
            time_to_play = round(end_time - start_time, 1)  # Berechnung der vergangenen Zeit und Zahl wird auf eine Nachkommastelle gerundet

            # Timerwert in der Datenbank aktualisieren
            user_collection.update_one({"Name": user_name}, {"$set": {"time": time_to_play}})

        print("--------------- Das Spiel ist zu Ende! ---------------\n")

        # Pipeline erstellen, um die Top 3 Spieler nach dem Punktestand zu sortieren
        top_players_pipeline = [
            {"$sort": {"score": -1, "time": 1}},
            # Absteigend nach Punktestand sortieren, aufsteigen nach Zeit sortieren
            {"$limit": 3},  # Ergebnisse auf die Top 3 Spieler begrenzen
            {"$project": {"_id": 0, "Name": 1, "score": 1, "time": 1}}  # Nur Name und Punktestand anzeigen
        ]

        # Top 3 Spieler suchen und anzeigen
        top_players = list(user_collection.aggregate(top_players_pipeline))

        print("\nTop 3 Spieler:")
        for rank, player in enumerate(top_players, start=1):
            print(f"{rank}. {player['Name']} - Punktestand: {player['score']} - {player['time']}Sek.")



    elif selected_category == 3:
        print("Du hast die Kategorie Preis ausgewählt.")
        print("")

        # Äußere Schleife für dreimalige Durchführung
        for attempt in range(1, 4):
            start_time = time.time()  # Startzeit für den Timer
            # ---------- Abschnitt Frage anzeigen ----------

            # Pipeline erstellen, um nur eine Frage zu Preise anzuzeigen
            preis_pipeline = [
                {
                    "$match": {
                        "FrageZuPreis": {"$exists": True}
                    }
                },
                {
                    "$project": {
                        "_id": 0,
                        "FrageZuPreis": 1
                    }
                }
            ]

            # Frage suchen
            question = question_collection.aggregate(preis_pipeline).next()

            print(question["FrageZuPreis"])

            # ---------- Abschnitt Autos anzeigen ----------

            # Hier drei zufällige Autos mit Preis auswählen und anzeigen
            random_cars_pipeline = [
                {"$match": {"Preis": {"$exists": True}}},
                {"$sample": {"size": 3}},
                {"$project": {"_id": 0, "Name": 1, "Preis": 1}}
            ]

            # Zufällige Autos suchen
            random_cars = list(car_collection.aggregate(random_cars_pipeline))

            # Pipeline erstellen, um das teuerste Auto zu finden
            mostExpensive_car_pipeline = [
                {"$match": {"Name": {"$in": [car["Name"] for car in random_cars]}}},
                {"$sort": {"Preis": -1}},
                {"$limit": 1},
                {"$project": {"_id": 0, "Name": 1, "Preis": 1}}
            ]

            # Das teuerste Auto finden
            mostExpensive_car = car_collection.aggregate(mostExpensive_car_pipeline).next()

            # Zuordnung von Zahlen zu Autos erstellen
            car_mapping = {str(i + 1): car["Name"] for i, car in enumerate(random_cars)}

            for number, car_name in car_mapping.items():
                print(f"{number}. {car_name}")

            # User Option vom Terminal einlesen
            user_choice_number = input("Wähle das Auto: ")

            # Überprüfen, ob die Eingabe eine gültige Zahl ist
            if user_choice_number in car_mapping:
                user_choice = car_mapping[user_choice_number]

                if user_choice == mostExpensive_car["Name"]:
                    print(f"Richtig!! Das teuerste Auto ist {mostExpensive_car['Name']}")
                    print("")

                    # Punktestand des aktuellen Spielers erhöhen
                    user_collection.update_one({"Name": user_name}, {"$inc": {"score": 1}})
                else:
                    print(f"Leider falsch... Die richtige Antwort ist: {mostExpensive_car['Name']}")
                    print("")

            end_time = time.time()  # Endzeit für den Timer
            time_to_play = round(end_time - start_time,
                                 1)  # Berechnung der vergangenen Zeit und Zahl wird auf eine Nachkommastelle gerundet

            # Timerwert in der Datenbank aktualisieren
            user_collection.update_one({"Name": user_name}, {"$set": {"time": time_to_play}})

        print("--------------- Das Spiel ist zu Ende! ---------------\n")

        # Pipeline erstellen, um die Top 3 Spieler nach dem Punktestand zu sortieren
        top_players_pipeline = [
            {"$sort": {"score": -1, "time": 1}},
            # Absteigend nach Punktestand sortieren, aufsteigen nach Zeit sortieren
            {"$limit": 3},  # Ergebnisse auf die Top 3 Spieler begrenzen
            {"$project": {"_id": 0, "Name": 1, "score": 1, "time": 1}}  # Nur Name und Punktestand anzeigen
        ]

        # Top 3 Spieler suchen und anzeigen
        top_players = list(user_collection.aggregate(top_players_pipeline))

        print("\nTop 3 Spieler:")
        for rank, player in enumerate(top_players, start=1):
            print(f"{rank}. {player['Name']} - Punktestand: {player['score']} - {player['time']}Sek.")



    elif selected_category == 4:
        print("Du hast die Kategorie Anzahl PS ausgewählt.")
        print("")

        # Äußere Schleife für dreimalige Durchführung
        for attempt in range(1, 4):
            start_time = time.time()  # Startzeit für den Timer
            # ---------- Abschnitt Frage anzeigen ----------

            # Pipeline erstellen, um nur eine Frage zu Anzahl PS anzuzeigen
            anzahlPS_pipeline = [
                {
                    "$match": {
                        "FrageZuAnzahlPS": {"$exists": True}
                    }
                },
                {
                    "$project": {
                        "_id": 0,
                        "FrageZuAnzahlPS": 1
                    }
                }
            ]

            # Frage suchen
            question = question_collection.aggregate(anzahlPS_pipeline).next()

            print(question["FrageZuAnzahlPS"])

            # ---------- Abschnitt Autos anzeigen ----------

            # Hier drei zufällige Autos mit Anzahl PS auswählen und anzeigen
            random_cars_pipeline = [
                {"$match": {"AnzahlPS": {"$exists": True}}},
                {"$sample": {"size": 3}},
                {"$project": {"_id": 0, "Name": 1, "AnzahlPS": 1}}
            ]

            # Zufällige Autos suchen
            random_cars = list(car_collection.aggregate(random_cars_pipeline))

            # Pipeline erstellen, um das schwächste Auto zu finden
            mostPowerful_car_pipeline = [
                {"$match": {"Name": {"$in": [car["Name"] for car in random_cars]}}},
                {"$sort": {"AnzahlPS": 1}},
                {"$limit": 1},
                {"$project": {"_id": 0, "Name": 1, "AnzahlPS": 1}}
            ]

            # Das schwächste Auto finden
            mostPowerful_car = car_collection.aggregate(mostPowerful_car_pipeline).next()

            # Zuordnung von Zahlen zu Autos erstellen
            car_mapping = {str(i + 1): car["Name"] for i, car in enumerate(random_cars)}

            for number, car_name in car_mapping.items():
                print(f"{number}. {car_name}")

            # User Option vom Terminal einlesen
            user_choice_number = input("Wähle das Auto: ")

            # Überprüfen, ob die Eingabe eine gültige Zahl ist
            if user_choice_number in car_mapping:
                user_choice = car_mapping[user_choice_number]

                if user_choice == mostPowerful_car["Name"]:
                    print(f"Richtig!! Das schwächste Auto ist {mostPowerful_car['Name']}")
                    print("")

                    # Punktestand des aktuellen Spielers erhöhen
                    user_collection.update_one({"Name": user_name}, {"$inc": {"score": 1}})
                else:
                    print(f"Leider falsch... Die richtige Antwort ist: {mostPowerful_car['Name']}")
                    print("")

            end_time = time.time()  # Endzeit für den Timer
            time_to_play = round(end_time - start_time, 1)  # Berechnung der vergangenen Zeit und Zahl wird auf eine Nachkommastelle gerundet

            # Timerwert in der Datenbank aktualisieren
            user_collection.update_one({"Name": user_name}, {"$set": {"time": time_to_play}})

        print("--------------- Das Spiel ist zu Ende! ---------------\n")

        # Pipeline erstellen, um die Top 3 Spieler nach dem Punktestand zu sortieren
        top_players_pipeline = [
            {"$sort": {"score": -1, "time": 1}},
            # Absteigend nach Punktestand sortieren, aufsteigen nach Zeit sortieren
            {"$limit": 3},  # Ergebnisse auf die Top 3 Spieler begrenzen
            {"$project": {"_id": 0, "Name": 1, "score": 1, "time": 1}}  # Nur Name und Punktestand anzeigen
        ]

        # Top 3 Spieler suchen und anzeigen
        top_players = list(user_collection.aggregate(top_players_pipeline))

        print("\nTop 3 Spieler:")
        for rank, player in enumerate(top_players, start=1):
            print(f"{rank}. {player['Name']} - Punktestand: {player['score']} - {player['time']}Sek.")



    else:
        print("Ungültige Auswahl. Bitte wähle eine Zahl von 1 bis 4.")
        category_questions = None



# Verbindung trennen (optional, wird normalerweise nicht benötigt)
client.close()
