import os
import re
import datetime
from flask import Flask, render_template, request
from dotenv import load_dotenv
from peewee import MySQLDatabase, SqliteDatabase, Model, CharField, TextField, DateTimeField
from playhouse.shortcuts import model_to_dict

load_dotenv()
app = Flask(__name__)

if os.getenv("TESTING") == "true":
    print("Running in test mode")
    mydb = SqliteDatabase('file:memory?mode=memory&cache=shared', uri=True)
else:
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
        "company": "Meta · MLH Fellowship",
        "role": "Production Engineering Fellow",
        "start": "Jun 2026",
        "end": "Present",
        "description": "Selected for MLH's Production Engineering Fellowship hosted with Meta — building and operating reliable, production-grade software with an emphasis on deployment, testing, and system reliability.",
        "bullets": [
            "Built and shipped a full-stack Flask + MySQL application, deploying it to an Ubuntu Linux VPS and serving it as a systemd service so it restarts automatically on boot and survives crashes.",
            "Designed a timeline REST API backed by a peewee ORM data model, adding request validation and a test-mode SQLite configuration so the test suite runs without a live database.",
            "Wrote a Python unittest suite and a curl-based integration script covering create/read flows and malformed-input edge cases, catching regressions before each deploy.",
            "Automated deployment with a bash script that syncs the latest main branch, reinstalls dependencies, and restarts the service — collapsing a multi-step manual deploy into a single command.",
            "Practiced core production-engineering workflows: environment and secret management, service logs and monitoring, and Git-based code review with fellow engineers.",
        ],
    },
    {
        "company": "Amentum",
        "role": "Plant Engineering Intern",
        "start": "Jun 2025",
        "end": "Aug 2025",
        "description": "Supported IT and security operations for a regulated national-laboratory environment.",
        "bullets": [
            "Designed and deployed Splunk dashboards monitoring 250+ endpoints for real-time system-health visibility.",
            "Rolled out Cortex XDR endpoint protection across the network and automated agent installation with scripts, cutting manual setup time.",
            "Documented processes and collaborated with the plant IT team under strict compliance requirements.",
        ],
    },
    {
        "company": "Berkeley SETI Research Center",
        "role": "Research Intern",
        "start": "Jun 2024",
        "end": "Aug 2024",
        "description": "Searched for radio technosignatures — signs of extraterrestrial technology — in large radio-telescope datasets.",
        "bullets": [
            "Analyzed MeerKAT radio-telescope data to search for narrowband technosignatures across thousands of stars.",
            "Built a filtering and candidate-reduction workflow that narrowed 30,000+ raw detections down to 10 high-confidence candidates.",
            "Presented methods and findings to researchers at the University of Oxford.",
        ],
    },
    {
        "company": "Vassar College CS Department",
        "role": "Computer Science Coach",
        "start": "Jan 2024",
        "end": "Present",
        "description": "Teaching assistant and tutor for core computer-science courses.",
        "bullets": [
            "Support Data Structures & Algorithms and Theory of Computation as a teaching assistant.",
            "Tutor ~30 students weekly — explaining complex concepts, debugging student code, and running review sessions.",
        ],
    },
    {
        "company": "Vassar College Physics & Astronomy",
        "role": "Senior Thesis Researcher",
        "start": "Oct 2023",
        "end": "Present",
        "description": "Applying machine learning to astrophysical simulations to understand the physics of galaxy formation.",
        "bullets": [
            "Apply ML to 3D magnetohydrodynamic (MHD) simulations of the circumgalactic medium to model galaxy formation.",
            "Trained and compared Ridge regression, Random Forest, and PyTorch neural-network models to predict silicon mass in simulated gas.",
            "Managed 2TB datasets and ran training jobs on the Midway Supercomputer (HPC cluster).",
        ],
    },
    {
        "company": "Vassar College",
        "role": "Arctic Delta Research Assistant",
        "start": "Jan 2026",
        "end": "Present",
        "description": "Remote-sensing research on environmental change in Arctic river deltas.",
        "bullets": [
            "Process satellite imagery in Python to study nutrient flux and retention across Arctic river deltas.",
            "Build reusable remote-sensing pipelines to analyze large geospatial datasets.",
        ],
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
        "image": "/static/img/soccer.jpg",
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
    {
        "name": "My Dog",
        "description": "Spending time with my favorite research assistant and hiking buddy.",
        "image": "/static/img/dog.jpg",
    },
]

skills = {
    "Languages": ["Python", "Java", "TypeScript", "Fortran", "SQL", "C", "OCaml", "PHP", "Assembly"],
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
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    content = request.form.get('content', '').strip()

    if not name:
        return "Invalid name", 400
    if not content:
        return "Invalid content", 400
    if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
        return "Invalid email", 400

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


@app.route("/timeline")
def timeline():
    return render_template("timeline.html", title="Timeline", pages=pages)
