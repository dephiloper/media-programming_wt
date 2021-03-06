from typing import List

from sqlalchemy import Column, Integer, ForeignKey, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()
engine = create_engine("sqlite:///btw.db", connect_args={'check_same_thread': False})


class Vote(Base):
    __tablename__ = "vote"
    id = Column(Integer, primary_key=True, autoincrement=True)
    region_id = Column(Integer, ForeignKey("region.id"))
    party_id = Column(Integer, ForeignKey("party.id"))
    temporary_result = Column(Integer)
    second_temporary_result = Column(Integer)
    previous_period = Column(Integer)
    second_previous_period = Column(Integer)
    region = relationship("Region", back_populates="votes")
    party = relationship("Party", back_populates="votes")

    def to_json(self):
        return {
            "id": self.id,
            "temporary_result": self.temporary_result,
            "second_temporary_result": self.second_temporary_result,
            "previous_period": self.previous_period,
            "second_previous_period": self.second_previous_period,
            "region": self.region.name,
            "party": self.party.name
        }


class Region(Base):
    __tablename__ = "region"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    parent_id = Column(Integer, ForeignKey("region.id"))
    sub_regions: List = relationship("Region", backref=backref('parent_region', remote_side=[id]), uselist=True)
    votes: List[Vote] = relationship("Vote", uselist=True)

    def to_json(self):
        parent = ""
        if self.parent_region != None:
            parent = self.parent_region.to_json()

        return {
            "id": self.id,
            "name": self.name,
            "parent": parent,
            "votes": [vote.to_json() for vote in self.votes]
        }


class Party(Base):
    __tablename__ = "party"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    votes: List[Vote] = relationship("Vote", uselist=True)

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "votes": [vote.to_json() for vote in self.votes]
        }


Base.metadata.create_all(engine)


def get_engine():
    return engine
