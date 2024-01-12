import random

import pymongo

# Verbindung zu MongoDB herstellen (stellen Sie sicher, dass Ihr Docker-Container läuft)
client = pymongo.MongoClient("mongodb://root:root@localhost:27017/")

# Datenbank erstellen ("QuizGame")
database = client["QuizGame"]

# Sammlungen erstellen ("statistics", "questions" und "answers")
statistics_collection = database["statistics"]
cars_collection = database["cars"]

all_cars = [
    {
        "Name": "Alfa Romeo",
        "Preis": 120000,
        "Geschwindigkeit": 380,
        "AnzahlPS": 410,
        "Herstellungsjahr": 2021
    },
    {
        "Name": "Tesla Model S",
        "Preis": 85000,
        "Geschwindigkeit": 200,
        "AnzahlPS": 670,
        "Herstellungsjahr": 2022
    },
    {
        "Name": "BMW M5",
        "Preis": 110000,
        "Geschwindigkeit": 305,
        "AnzahlPS": 600,
        "Herstellungsjahr": 2020
    },
    {
        "Name": "Mercedes-Benz S-Class",
        "Preis": 130000,
        "Geschwindigkeit": 250,
        "AnzahlPS": 550,
        "Herstellungsjahr": 2023
    },
    {
        "Name": "Audi R8",
        "Preis": 160000,
        "Geschwindigkeit": 330,
        "AnzahlPS": 620,
        "Herstellungsjahr": 2021
    },
    {
        "Name": "Porsche 911",
        "Preis": 135000,
        "Geschwindigkeit": 310,
        "AnzahlPS": 580,
        "Herstellungsjahr": 2022
    },
    {
        "Name": "Ferrari 488 GTB",
        "Preis": 250000,
        "Geschwindigkeit": 340,
        "AnzahlPS": 670,
        "Herstellungsjahr": 2021
    },]


# Antworten in die MongoDB-Sammlung "cars" einfügen (nur einmal)
if cars_collection.count_documents({}) == 0:
    cars_collection.insert_many(all_cars)


# Benutzernamen vom Terminal einlesen
user_name = input("Wie heißt du? ")

# Überprüfen, ob der Benutzer bereits in der Datenbank existiert
existing_user = statistics_collection.find_one({"player": user_name})

if existing_user:
    print(f"Willkommen zurück, {user_name}!")
else:
    # Benutzernamen in die Datenbank unter der Sammlung "statistics" speichern oder aktualisieren
    statistics_collection.update_one(
        {"player": user_name},
        {"$set": {"player": user_name, "score": 0}},
        upsert=True
    )
    print(f"Willkommen, {user_name}!")

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
        print("Welches Auto ist das 2 schnellste?")
        # Zufällige Auswahl von 3 Autos
        selected_cars = []
        for i in range(3):
            car = random.choice(all_cars)
            selected_cars.append(car)
            print(f"- {car['Name']} ")

            if i == 2:
                # Autos nach Geschwindigkeit sortieren
                sorted_cars = sorted(selected_cars, key=lambda x: x['Geschwindigkeit'], reverse=True)

                # Ausgabe des zweit schnellsten Auto
                print(f"Das zweit schnellste Auto ist: {sorted_cars[1]['Name']} (Geschwindigkeit: {sorted_cars[1]['Geschwindigkeit']} Km/h)")


    elif selected_category == 2:
        print("Du hast die Kategorie Herstellungsjahr ausgewählt.")
        print("Welches Auto ist am ältesten?")
        # Zufällige Auswahl von 3 Autos
        selected_cars = []
        for i in range(3):
            car = random.choice(all_cars)
            selected_cars.append(car)
            print(f"- {car['Name']} ")

            if i == 2:  # Prüfe, ob es der dritte Durchlauf ist
                # Auto mit dem ältesten Herstellungsjahr
                lowest_buildYear_car = min(selected_cars, key=lambda x: x['Herstellungsjahr'])

                # Ausgabe des Autos mit dem höchsten Preis
                print(f"Das Auto älteste Auto ist: {lowest_buildYear_car['Name']} (Herstellungsjahr: {lowest_buildYear_car['Herstellungsjahr']})")


    elif selected_category == 3:
        print("Du hast die Kategorie Preis ausgewählt.")
        print("Welches Auto hat den höchsten Kaufpreis?")
        # Zufällige Auswahl von 3 Autos
        selected_cars = []
        for i in range(3):
            car = random.choice(all_cars)
            selected_cars.append(car)
            print(f"- {car['Name']} ")

            if i == 2:  # Prüfe, ob es der dritte Durchlauf ist
                # Auto mit dem höchsten Preis finden
                highest_price_car = max(selected_cars, key=lambda x: x['Preis'])

                # Ausgabe des Autos mit dem höchsten Preis
                print(f"Das Auto mit dem höchsten Kaufpreis ist: {highest_price_car['Name']} (Preis: {highest_price_car['Preis']} CHF)")


    elif selected_category == 4:
        print("Du hast die Kategorie Anzahl PS ausgewählt.")
        print("Welches Auto hat am wenigsten Kraft in PS?")
        # Zufällige Auswahl von 3 Autos
        selected_cars = []
        for i in range(3):
            car = random.choice(all_cars)
            selected_cars.append(car)
            print(f"- {car['Name']} ")

            if i == 2:  # Prüfe, ob es der dritte Durchlauf ist
                # Auto mit dem höchsten Preis finden
                lowest_price_car = min(selected_cars, key=lambda x: x['Preis'])

                # Ausgabe des Autos mit dem höchsten Preis
                print(f"Das Auto mit am wenigsten Kraft (in PS) ist: {lowest_price_car['Name']} (Anzahl PS: {lowest_price_car['Preis']})")


    else:
        print("Ungültige Auswahl. Bitte wähle eine Zahl von 1 bis 4.")
        category_questions = None



# Verbindung trennen (optional, wird normalerweise nicht benötigt)
client.close()
