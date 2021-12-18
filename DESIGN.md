To explain my design decisions, I will begin by first explaining the design behind the structure of the databse in database.py, followed by an explanation of the html pages/css, and finally an explanation for __init__.py.

database.py
The contents of this file include imports from sqlalchemy at the top of the file, the setting up of the db engine, db_session, Base, and Base.query, as well as a function called "init_db()" that initializes the database. These inclusions are critical and non-negotiable for SQl alchemy to be used, so I will not be elaborating on my decsion to include this. After this, though, there I included code for a class called Groupie that creates an object of the same name. In SQLAlchemy, data is pushed to the database via objects that hold various attributes. The reasoning behind teh attributes I chose to include for the datatable is that all of the information requred is needed in order for other usres to have a clear picture on teh specifications concerning each Groupie event. For example, if the email of the creator wasn't incldued, then users that sign up for the event will not know how to contact the creator. Furthmore, if the location wasn't included, then users would obviously not know where the event will occur. The reason I chose to use SQLAlchemy instead of the otehr options for databases and sql that we learned in class is becasue I was exposed to SQLAlchemy in Tech 4 Social Good, and thought it would be immensely interesting to start my own project from scratch. Addiotnally, I found that SQLAlchemy is very beneficial to use with python as well as it essentially allows one to map sqlite3 database data on python objects. This makes it immensely easy in flask applications where the backend of the project is created utilziing python.

HTML Pages/CSS
Beginning with the index.html page, I made sure to include a navbar at the top of the webpage as I wanted users to easily be able to navigate through each function of the website. Whether they want to search for a Groupie, create one, or be brought back to the homepage, they can easily do so by clicking on any of the items in the navbar. I believed that this was an extremely practical and useful feature to include, so I made sure to implement this design choice on every other webpage on the website. Underneath the short welcome greeting that is present on the main page, I created a jinja function that outputs every single registered Groupie event in the database, along with each Groupie's attributes. To ensure that this looks celan and stylized on the website, I used my styles.css file to evenly space out each Groupie events with the css flex attributes. Additionally, I inlcuded a nicely styled footer that displays the contact information for Groupie. Similar to the navigation bar, this is included on every webpage. 
Now, let's turn focus to the navigation bar at the top. The navigation bar was created using bootstrap as it easily allows for dynamic navbars to be created that change based on the dimensions of the window the website occupies. On the left-most side of the navbar is the word "Groupie," which, when clicked, will bring users to the main page of the website. Right next to this is the search bar and search button. Looking at the right-hand side of the navigation bar, I believed that it was critical to provide an easy way for users to create and register their own Groupie events, so I made sure to include a button that allows users to do so. When a user creates their event, I made sure to include an attribute in the creation of the Groupie datatables that each entry into the table must have a topic that is unique. The reaosn being is that users sign up for events via the topic of the Groupie. Therefore, if two Groupies had the same topic, there would be confusion in the backend over which event the user wishes to sign up for.

__init__.py
This file contains all of the logic for the routes of the website. The first route provided, "create_app," is needed in order to run SQLAlchemy with flask, so I will not explain its inclusion in this section. The rest of the file contains all of the possible routes for this application. Beginning with the two routes for index, I needed to store a list of all the Groupie objects (rows) in the database as well as the total number of Groupie obects (rows) as this information needs to be passed to index.html in order to display each groupie event on the homepage via jinja.
For uerss that want to create their own Groupie, I created a route called "/create" that, if the method is "POST," stores the values inputted by the user in the form before creating a new Groupie object that will then be pushed to the database. This easy way to add new data to the database is the reason why I decided to create a form on "create.html" in the first place.
Furthermore, if a user wants to sign up for a club, I created a route called "/signup" that stores the topic and email the user enters, which allows the website to send an email to the user concerning their Groupie event and update the number of attendees for that specific Groupie event. Had I had more time, one desire would be change this to send an invitation for a google calendar event. However, the intention behind sending an email is similar to a GCAL invite in that I wanted the user to have a copy of the Groupie's information in case they ever wanted to easily reference it. 
Lastly, I included a route called "/searchgroupie" that is connected with the search bar in the navigation bar and allows users to easily search for Groupie events. The reasoning behind the code in this route is that I wanted to prioritize usbality of the website by easily allowing users to serach for events they are interested in. Since the job of Groupie is to facilitate student connections, a search feature seemed integral to achieving this goal. 