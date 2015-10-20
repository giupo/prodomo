# -*- coding:utf-8 -*-
"""
Questo modulo controlla la gestione CRUD degli switch come configurati
dall'utente

E' il frontend al db (Model)
"""
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from pkg_resources import Requirement, resource_filename
dbfile = resource_filename(Requirement.parse("prodomo"), "db/prodomo.db")
engine = create_engine('sqlite:///' + dbfile, echo=True)
Session = sessionmaker(bind=engine)

Base = declarative_base()
class Switch(Base):
    __tablename__ = 'switch'

    id = Column(Integer, primary_key=True)
    pin = Column(Integer, unique=True)
    description = Column(String)

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return "<Switch(id='%s', pin='%s', description='%s')>" % (
                             self.id, self.pin, self.description)
