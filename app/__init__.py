import os
import datetime
from flask import Flask, render_template, request
from dotenv import load_dotenv
from peewee import MySQLDatabase, Model, CharField, TextField, DateTimeField
from playhouse.shortcuts import model_to_dict

load_dotenv()
app = Flask(__name__)

mydb = MySQLDatabase(
    os.getenv("MYSQL_DATABASE"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    host=os.getenv("MYSQL_HOST"),
    port=3306,
)

print(mydb)


class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb


mydb.connect()
mydb.create_tables([TimelinePost])

experiences = [
    {
        "company": "Major League Hacking",
        "role": "Software Engineering Fellow",
        "start": "Jun 2026",
        "end": "Present",
        "description": "Building open-source projects and collaborating with engineers worldwide through the MLH Fellowship program.",
    },
    {
        "company": "Amentum",
        "role": "Plant Engineering Intern",
        "start": "Jun 2025",
        "end": "Aug 2025",
        "description": "Designed Splunk dashboards monitoring 250 endpoints, deployed Cortex XDR across the network, and automated system installation scripts to streamline IT operations.",
    },
    {
        "company": "Berkeley SETI Research Center",
        "role": "Research Intern",
        "start": "Jun 2024",
        "end": "Aug 2024",
        "description": "Technosignature detection using radio astronomy — analyzed MeerKAT datasets, reduced 30,000+ candidate signals to 10 high-confidence detections, and presented findings at Oxford University.",
    },
    {
        "company": "Vassar College CS Department",
        "role": "Computer Science Coach",
        "start": "Jan 2024",
        "end": "Present",
        "description": "Teaching Assistant for Data Structures & Algorithms and Theory of Computation; tutored ~30 students weekly.",
    },
    {
        "company": "Vassar College Physics & Astronomy",
        "role": "Senior Thesis Researcher",
        "start": "Oct 2023",
        "end": "Present",
        "description": "Applying machine learning to 3D magnetohydrodynamic simulations of galaxy formation — trained Ridge regression, Random Forest, and PyTorch neural network models on 2TB datasets hosted on the Midway Supercomputer.",
    },
    {
        "company": "Vassar College",
        "role": "Arctic Delta Research Assistant",
        "start": "Jan 2026",
        "end": "Present",
        "description": "Remote sensing data analysis for nutrient flux and retention in Arctic river deltas using Python-based satellite imagery processing pipelines.",
    },
]

education = [
    {
        "school": "Vassar College",
        "degree": "B.S. Computer Science & Astronomy",
        "start": "Sept 2022",
        "end": "May 2026",
        "description": "GPA: 3.76/4.0 · Scholarships: Benjamin Gilman Scholar, Thompson Bartlett Fellowship, Tananbaum Fellowship · Coursework: Machine Learning, Astrophysics, Galaxies & Galactic Structure, Stellar Astrophysics.",
    },
    {
        "school": "University of Edinburgh",
        "degree": "Study Abroad",
        "start": "Sept 2024",
        "end": "Dec 2024",
        "description": "Coursework: Computer Systems, Modern Physics, Astrobiology.",
    },
    {
        "school": "Temple University Japan",
        "degree": "Study Abroad",
        "start": "Jan 2025",
        "end": "May 2025",
        "description": "Coursework: Web Development, Data Science, Cyberspace & Society.",
    },
]

hobbies = [
    {
        "name": "Soccer",
        "description": "Playing and watching the beautiful game — always down for a kickaround.",
        "image": "https://images.unsplash.com/photo-1579952363873-27f3bade9f55?w=700&q=80",
    },
    {
        "name": "Traveling",
        "description": "Exploring new countries and cultures — from studying abroad in Edinburgh and Tokyo to research trips across the US.",
        "image": "https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1?w=700&q=80",
    },
    {
        "name": "Baking",
        "description": "Experimenting in the kitchen with breads, pastries, and recipes inspired by everywhere I've been.",
        "image": "https://images.unsplash.com/photo-1486427944299-d1955d23e34d?w=700&q=80",
    },
]

skills = {
    "Languages": ["Python", "Java", "TypeScript", "SQL", "C", "OCaml", "PHP", "Assembly"],
    "ML / Data Science": ["PyTorch", "scikit-learn", "NumPy", "Pandas", "Matplotlib", "Jupyter"],
    "Web": ["Vue.js", "React", "Next.js", "Laravel", "HTML/CSS", "JavaScript"],
    "Tools": ["Linux", "HPC / Supercomputing", "Git", "MySQL", "Splunk", "Docker", "LaTeX"],
}

visited_locations = [
    {"name": "Queens, New York, USA", "lat": 40.7282, "lng": -73.7949},
    {"name": "Berkeley, CA, USA", "lat": 37.8716, "lng": -122.2727},
    {"name": "Richland, WA, USA", "lat": 46.2856, "lng": -119.2844},
    {"name": "Edinburgh, Scotland, UK", "lat": 55.9533, "lng": -3.1883},
    {"name": "Tokyo, Japan", "lat": 35.6762, "lng": 139.6503},
    {"name": "Oxford, UK", "lat": 51.7520, "lng": -1.2577},
    {"name": "Poughkeepsie, NY, USA", "lat": 41.7004, "lng": -73.9209},
]

pages = [
    {"name": "Home", "url": "/"},
    {"name": "Hobbies", "url": "/hobbies"},
]


@app.route("/")
def index():
    return render_template(
        "index.html",
        title="Maya Laidler",
        url=os.getenv("URL"),
        experiences=experiences,
        education=education,
        visited_locations=visited_locations,
        skills=skills,
        hobbies=hobbies,
        pages=pages,
    )


@app.route("/hobbies")
def hobbies_page():
    return render_template(
        "hobbies.html",
        title="Hobbies — Maya Laidler",
        url=os.getenv("URL"),
        hobbies=hobbies,
        pages=pages,
    )


@app.route("/api/timeline_post", methods=["POST"])
def post_time_line_post():
    name = request.form['name']
    email = request.form['email']
    content = request.form['content']
    timeline_post = TimelinePost.create(name=name, email=email, content=content)

    return model_to_dict(timeline_post)


@app.route("/api/timeline_post", methods=["GET"])
def get_time_line_post():
    return {
        'timeline_posts': [
            model_to_dict(p)
            for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }
