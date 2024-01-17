// Wenn es diese DB nicht gibt, wird eine erstellt
db = db.getSiblingDB('QuizGame');

db.createCollection('cars');

db.cars.insertMany([
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
    },
]);

db.createCollection('questions');

db.questions.insertMany([
    {"FrageZuGeschwindigkeit":"Welches Auto ist das 2 schnellste?"},
    {"FrageZuPreis":"Welches Auto hat den höchsten Kaufpreis?"},
    {"FrageZuAnzahlPS":"Welches Auto hat am wenigsten Kraft in PS?"},
    {"FrageZuHerstellungsjahr":"Welches Auto ist am ältesten?"}
]);

db.createCollection('statistic');

