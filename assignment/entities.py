import enum
from typing import List

from sqlalchemy import Column, Integer, ForeignKey, String, create_engine, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()
engine = create_engine("sqlite:///btw.db")


class VoteType(enum.Enum):
    FIRST = 0
    SECOND = 1

    def to_json(self):
        if self == VoteType.FIRST:
            return "Erststimmen"
        elif self == VoteType.SECOND:
            return "Zweitstimmen"


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

    def to_json(self):
        return {
            "id": self.id,
            "type": self.type.to_json(),
            "temporary_result": self.temporary_result,
            "previous_period": self.previous_period,
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
