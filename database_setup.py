from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Institution(Base):
    __tablename__ = 'institution'

    id = Column(Integer, primary_key=True)
    name = Column(String(500), nullable=False)
    address = Column(String(500))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address
        }


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    name = Column(String(250))
    gender = Column(String(10))
    picture = Column(String(250))
    institution_id = Column(Integer, ForeignKey('institution.id'))
    institution = relationship(Institution)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'email':self.email,
            'name': self.name,
            'gender': self.gender,
            'picture': self.picture,
            'institution': self.institution_id
        }

class OrganicUser(Base):
    __tablename__ = 'organicuser'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    name = Column(String(250))
    picture = Column(String(250))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'email':self.email,
            'name': self.name,
            'picture': self.picture
        }

engine = create_engine('sqlite:///users.db')
Base.metadata.create_all(engine)