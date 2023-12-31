from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'comment': 'Table storing user information'}
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True)
    name = Column(String)
    surname = Column(String)
    password = Column(String)
    token = Column(String, unique=True)
    userlists = relationship("Userlist", back_populates="user")

class Userlist(Base):
    __tablename__ = 'userlists'
    __table_args__ = {'comment': 'Table storing user lists information'}
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, ForeignKey('events.title'))
    username = Column(String, ForeignKey('users.username'))
    user = relationship("User", back_populates="userlists")
    events = relationship("Event", back_populates="userlist")

class Event(Base):
    __tablename__ = 'events'
    __table_args__ = {'comment': 'Table storing event information'}
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, unique=True)
    description = Column(String)
    created_by = Column(String)
    event_date = Column(TIMESTAMP)
    userlist = relationship("Userlist", back_populates="events")


engine = create_engine('postgresql+psycopg2://postgres:fgrr44xs00!M@localhost/eventsdb')
Session = sessionmaker(bind=engine)

# Create all tables
Base.metadata.create_all(engine)

# Create a Session
session = Session()
