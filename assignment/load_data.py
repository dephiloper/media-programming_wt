import csv
from sqlalchemy.orm import sessionmaker
from entities import Party, Vote, Region, get_engine

Session = sessionmaker(bind=get_engine())
session = Session()

federal_territory = None


with open('btw17_kerg.csv', 'r') as csv_file:
    for i in range(2): next(csv_file)  # ignore first two lines
    parties = []

    reader = csv.reader(csv_file, delimiter=';')

    header_row = next(reader)
    for i in range(3, len(header_row) - 1):  # get party names
        if (i + 1) % 4 == 0:
            parties.append(Party(name=header_row[i]))

    for i in range(2): next(csv_file)  # ignore next two lines

    states = []
    constituencies = []

    for row in reader:
        if str(row[0]).__contains__(','):  # when separator line go for the next
            break

        if len(row) > 2:
            votes_row = row[3:-1]

            votes = []
            for i in range(0, len(votes_row), 4):
                vote = Vote(temporary_result=int(votes_row[i] or 0), previous_period=int(votes_row[i + 1] or 0),
                            second_temporary_result=int(votes_row[i+2] or 0), second_previous_period=int(votes_row[i + 3] or 0))
                # when both empty do not store vote
                if vote.temporary_result != 0 or vote.previous_period != 0 or \
                        vote.second_temporary_result != 0 or vote.second_previous_period != 0:
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
                state.sub_regions = constituencies
                constituencies.clear()
                states.append(state)
            else:  # constituencies
                constituencies.append(region)

session.add(federal_territory)
session.commit()
