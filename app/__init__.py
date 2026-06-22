import os
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

experiences = [
    {
        "company": "Major League Hacking",
        "role": "Software Engineering Fellow",
        "start": "Jun 2026",
        "end": "Present",
        "description": "Building open-source projects and collaborating with engineers worldwide through the MLH Fellowship program.",
    },
    {
        "company": "Tech Startup Co.",
        "role": "Software Engineering Intern",
        "start": "May 2025",
        "end": "Aug 2025",
        "description": "Developed full-stack features using React and Python, improving load times by 30%.",
    },
]

education = [
    {
        "school": "State University",
        "degree": "B.S. Computer Science",
        "start": "2022",
        "end": "2026",
        "description": "Relevant coursework: Data Structures, Algorithms, Web Development, Machine Learning.",
    },
]

hobbies = [
    {
        "name": "Photography",
        "description": "Capturing landscapes and street scenes wherever I travel.",
        "image": "hobby_photography.jpg",
    },
    {
        "name": "Hiking",
        "description": "Exploring trails and national parks across the country.",
        "image": "hobby_hiking.jpg",
    },
    {
        "name": "Cooking",
        "description": "Experimenting with recipes from cultures I have visited.",
        "image": "hobby_cooking.jpg",
    },
]

visited_locations = [
    {"name": "New York, USA", "lat": 40.7128, "lng": -74.0060},
    {"name": "London, UK", "lat": 51.5074, "lng": -0.1278},
    {"name": "Tokyo, Japan", "lat": 35.6762, "lng": 139.6503},
    {"name": "Paris, France", "lat": 48.8566, "lng": 2.3522},
    {"name": "Sydney, Australia", "lat": -33.8688, "lng": 151.2093},
    {"name": "Mexico City, Mexico", "lat": 19.4326, "lng": -99.1332},
]

pages = [
    {"name": "Home", "url": "/"},
    {"name": "Hobbies", "url": "/hobbies"},
]


@app.route("/")
def index():
    return render_template(
        "index.html",
        title="MLH Fellow",
        url=os.getenv("URL"),
        experiences=experiences,
        education=education,
        visited_locations=visited_locations,
        pages=pages,
    )


@app.route("/hobbies")
def hobbies_page():
    return render_template(
        "hobbies.html",
        title="Hobbies",
        url=os.getenv("URL"),
        hobbies=hobbies,
        pages=pages,
    )
