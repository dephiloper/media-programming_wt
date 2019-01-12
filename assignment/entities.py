import enum

from sqlalchemy import Column, Integer, ForeignKey, String, create_engine, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()
engine = create_engine("sqlite:///btw.db")


class VoteType(enum.Enum):
    FIRST = 0
    SECOND = 1


class Vote(Base):
    __tablename__ = "vote"
    id = Column(Integer, primary_key=True, autoincrement=True)
    region_id = Column(Integer, ForeignKey("region.id"))
    party_id = Column(Integer, ForeignKey("party.id"))
    type = Column(Enum(VoteType))
    temporary_result = Column(Integer)
    previous_period = Column(Integer)
    region = relationship("Region", back_populates="votes")
    party = relationship("Party", back_populates="votes")


class Region(Base):
    __tablename__ = "region"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    parent_id = Column(Integer, ForeignKey("region.id"))
    sub_regions: [] = relationship("Region", backref=backref('parent_region', remote_side=[id]), uselist=True)
    votes: [] = relationship("Vote", uselist=True)


class Party(Base):
    __tablename__ = "party"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    votes: [] = relationship("Vote", uselist=True)


Base.metadata.create_all(engine)


def get_engine():
    return engine
