from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///:Groupie.db', echo=True)
db_session = scoped_session(sessionmaker(autocommit=False,autoflush=False,bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    #ititializes the database
    Base.metadata.create_all(bind=engine)
    db_session.commit()

#creates object called Groupie
class Groupie(Base):
    __tablename__ = 'groupie'
    __table_args__ = {'extend_existing': True}

    #sets up columns for groupie datatable 
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False )
    topic = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=False)
    date = Column(String, nullable=False)
    location = Column(String, nullable=False)
    start_time = Column(String, nullable=False)
    end_time = Column(String, nullable=False)
    attendees = Column(Integer, nullable=False)

    #onstructor for Groupie datatable
    def __init__(self, name=None, email=None, topic=None, description=None, date=None, location=None, start_time=None, end_time=None, attendees=None):
        self.name = name
        self.email = email
        self.topic = topic
        self.description = description
        self.date = date
        self.location = location
        self.start_time = start_time
        self.end_time = end_time
        self.attendees = attendees

    #deals with what will print if developer every types "print(groupie)" where groupie is a Groupie object
    def __repr__(self):
        return '<Groupie ' + self.topic + '>'