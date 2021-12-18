import os
#imports for flask
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, Flask
)
#imports to make sure database works
from env.database import init_db, db_session
from flask_sqlalchemy import SQLAlchemy
from .database import Groupie

#impmorts to allow email access
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



db = SQLAlchemy()

def create_app(test_config=None):
    #creates and configures app
    app = Flask(__name__, template_folder='templates', instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'Groupie.db'),
    )

    db = SQLAlchemy(app)
    db.app = app

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    #route for index
    @app.route('/')
    def hello():
        groupielist = Groupie.query.all()
        groupielength = len(groupielist)
        return render_template("index.html", groupielist=groupielist, groupielength=groupielength)
    
    #another route for index
    @app.route('/index.html')
    def index():
        groupielist = Groupie.query.all()
        groupielength = len(groupielist)
        return render_template("index.html", groupielist=groupielist, groupielength=groupielength)

    #route if user wants to create Groupie
    @app.route("/create", methods=["GET", "POST"])
    def create():
        if request.method == "POST":
            #stores the values of each input section in the form
            name = request.form.get("name")
            email = request.form.get("email")
            topic = request.form.get("topic")
            description = request.form.get("description")
            date = request.form.get("date")
            location = request.form.get("location")
            start_time = request.form.get("start_time")
            end_time = request.form.get("end_time")

            #creates a new Groupie object that will be pushed to the database
            newGroupie = Groupie(name=name, email=email, topic=topic, description=description, date=date, 
            location=location, start_time=start_time, end_time=end_time, attendees=0)
            #stages the new Groupie object to be added to the database
            db_session.add(newGroupie)
            #pushes the new Groupie object to the database
            db_session.commit()
            #redirects back to homepage
            return redirect("/")
        else:  
            return render_template("create.html")

    #route for if user wants to sign-up Groupie
    @app.route('/signup', methods=["GET", "POST"])
    def makesignup():
        if request.method == "POST":

            #stores name of groupie and email of user that sign ups
            topic = request.form.get("topic")
            email = request.form.get("email")
            #searches for Groupie event by topic
            groupie = Groupie.query.filter_by(topic=topic).first()
            #configures mail application
            sender = "fidnyourgroupie@gmail.com"
            password = "groupie123"
            #SET up the MIME
            message = MIMEMultipart()
            message['From'] = sender
            message['To'] = email
            message['Subject'] = "Thank you for Registering for your Groupie!"
            #sets up body for email
            body = f'''Hello,
            Thank you so much for registering for your groupie.
            Make sure to save this email so that you know the details of your groupie.
            The topic is: {groupie.topic}
            The description is: {groupie.description} 
            The date is: {groupie.date}
            The location is: {groupie.location}
            The start time is: {groupie.start_time}
            The end time is: {groupie.end_time}
            If you need to get into contact with the creator, {groupie.name}, email them here: {groupie.email}.'''
            message.attach(MIMEText(body, 'plain'))
            #Create SMTP session for sending mail
            try:
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.ehlo()
                server.starttls()
                server.login(sender, password)
                text = message.as_string()
                server.sendmail(sender, email, text)
                server.quit()
                #increases the number of attendees by one
                groupie.attendees += 1
                db_session.commit()
            except:
                print ("Something went wrong...")
            return redirect("/")
        else:
            return render_template("signup.html")

    #route for if user wants to sign-up for Groupie
    @app.route('/signup.html')
    def signup():
        return render_template("signup.html")

    #route for if users use the search bar at the top of the nav
    @app.route('/searchgroupie', methods=["GET", "POST"])
    def search():
        if request.method == "POST":
            #stores the text in the search bar to a variable
            topic = request.form.get("search")
            #formats the text so that it is easy to search for similar topics
            search = "%{}%".format(topic)
            #searches through groupie datatable for topics that are similar to the topic provided in the search bar
            groupielist = Groupie.query.filter(Groupie.topic.like(search)).all()
            groupielength = len(groupielist)
            #if there are no events with topics similar to the one provided in the search bar
            if groupielength == 0:
                return render_template("index.html")
            #else, renders search.html which showcases each similar Groupie event
            else:
                return render_template("search.html", groupielist=groupielist, groupielength=groupielength)
        else:
            return render_template("index.html")   

    db.init_app(app)

    init_db()

    return app


