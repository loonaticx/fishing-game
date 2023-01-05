import sqlalchemy as db

from sqlalchemy import create_engine, update

# todo: make the create_engine options a config value
# memory = True
# if memory:
#     engine = create_engine("sqlite:///:memory:", echo=True)

engine = create_engine("sqlite:///fish.db", echo = True)

#
# if not memory:
#     engine = create_engine("postgresql://localhost/fishdb")
#     if not database_exists(engine.url):
#         create_database(engine.url)
#
#     conn = engine.connect()
#     conn.execute("commit")

from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind = engine)
session = Session()

from sqlalchemy.orm import declarative_base

Base = declarative_base()

from sqlalchemy import Column, Integer, String


class User(Base):
    __tablename__ = "users"

    # discord id
    id = Column(Integer, primary_key = True)  # user number
    disid = Column(Integer)  # discord id
    username = Column(String)  # friendly username
    context = Column(db.PickleType(), nullable = True)  # FishContext object, blob

    def __init__(self, disid: int, username: str):
        self.disid = disid
        self.username = username

    def __repr__(self):
        return "<User(disid='%s', context='%s', id='%s')>" % (
            self.disid,
            self.context,
            self.id,
        )

    def registerFishContext(self, cls):
        self.context = cls
        return cls


def updateContext(disid, context):
    update(User).where(User.disid == disid).values(context = context)
    session.commit()


Base.metadata.create_all(engine)
