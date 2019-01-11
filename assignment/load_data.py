import csv

from sqlalchemy import create_engine, Integer, Column, String, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

engine = create_engine("sqlite:///btw.db")
Session = sessionmaker(bind=engine)
session = Session()

states = []
cities = []
federal_territory = None

parties = []


class VoteType(Enum):
    FIRST = 0
    SECOND = 1


class Vote(Base):
    __tablename__ = "vote"
    id = Column(Integer, primary_key=True, autoincrement=True)
    region_id = Column(Integer, ForeignKey("region.id"))
    party_id = Column(Integer, ForeignKey("party.id"))
    type = Column(Integer)
    temporary_result = Column(Integer)
    previous_period = Column(Integer)
    region = relationship("Region", back_populates="votes")
    party = relationship("Party", back_populates="votes")


class Region(Base):
    __tablename__ = "region"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    parent_id = Column(Integer, ForeignKey("region.id"))
    parent_region = relationship("Region", uselist=False)
    sub_regions: [] = relationship("Region", uselist=True)
    votes: [] = relationship("Vote", uselist=True)


class Party(Base):
    __tablename__ = "party"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    votes: [] = relationship("Vote", uselist=True)


Base.metadata.create_all(engine)

with open('btw17_kerg.csv', 'r') as csv_file:
    for i in range(2): next(csv_file)  # ignore first two lines

    reader = csv.reader(csv_file, delimiter=';')

    header_row = next(reader)
    for i in range(3, len(header_row) - 1):  # get party names
        if (i + 1) % 4 == 0:
            parties.append(Party(name=header_row[i]))

    for i in range(2): next(csv_file)  # ignore next two lines

    for row in reader:
        if str(row[0]).__contains__(','): # when separator line go for the next
            break

        if len(row) > 2:
            votes_row = row[3:-1]

            votes = []
            for i in range(0, len(votes_row), 2):
                vote = Vote(type=(i / 2) % 2 == 0, temporary_result=votes_row[i], previous_period=votes_row[i + 1])
                if vote.temporary_result != "" or vote.previous_period != "":
                    vote.party = parties[int(i / 4)]
                    votes.append(vote)

            region = Region(name=row[1], votes=votes)
            votes.clear()

            if len(row[0]) > 0 and len(row[2]) == 0:  # federal_territory
                federal_territory = region
                federal_territory.sub_regions = states
                states.clear()
            elif int(row[2]) == 99:  # state
                state = region
                state.sub_regions = cities
                cities.clear()
                states.append(state)
            else:  # city
                cities.append(region)

session.add(federal_territory)
session.commit()
