import csv
from sqlalchemy.orm import sessionmaker
from entities import Party, Vote, Region, get_engine, VoteType

Session = sessionmaker(bind=get_engine())
session = Session()

states = []
cities = []
federal_territory = None

parties = []

with open('btw17_kerg.csv', 'r') as csv_file:
    for i in range(2): next(csv_file)  # ignore first two lines

    reader = csv.reader(csv_file, delimiter=';')

    header_row = next(reader)
    for i in range(3, len(header_row) - 1):  # get party names
        if (i + 1) % 4 == 0:
            parties.append(Party(name=header_row[i]))

    for i in range(2): next(csv_file)  # ignore next two lines

    for row in reader:
        if str(row[0]).__contains__(','):  # when separator line go for the next
            break

        if len(row) > 2:
            votes_row = row[3:-1]

            votes = []
            for i in range(0, len(votes_row), 2):
                t = VoteType((i / 2) % 2) # first or second vote
                vote = Vote(type=t, temporary_result=votes_row[i], previous_period=votes_row[i + 1])
                if vote.temporary_result != "" or vote.previous_period != "": # when both empty do not store vote
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
