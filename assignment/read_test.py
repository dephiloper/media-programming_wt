from sqlalchemy.orm import sessionmaker
from entities import get_engine, Region

Session = sessionmaker(bind=get_engine())
session = Session()

regions = session.query(Region).first()
print(regions)
