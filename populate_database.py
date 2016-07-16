from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Institution, User, OrganicUser
from hostdetails import host, path_to_repo

engine = create_engine('sqlite:///'+path_to_repo+'users.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Institution1 = Institution(name="Ramjas School", address="Anand Parbat")
# session.add(Institution1)
# session.commit()

# User1 = User(email="rashi.t.malik@gmail.com")
# session.add(User1)
# session.commit()

# file = open('subscribersList.txt','r')
# subscribers = file.read().splitlines()
# for subscriber in subscribers:
#     temp = subscriber
#     User1 = User(email=subscriber)
#     session.add(User1)
#     session.commit()

# user = session.query(User).filter_by(email="vgoel38@gmail.com")
# for u in user:
#     print u.email
#     session.delete(u)
#     session.commit()

# user = session.query(User)
# for u in user:
#     session.delete(u)
#     session.commit()

user = session.query(User).all()
for u in user:
    print u.email

# user = session.query(User).filter_by(email="vgoel38@gmail.com")
# for u in user:
#     print u.email

