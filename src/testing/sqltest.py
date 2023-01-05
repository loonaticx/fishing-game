from fishbase.FishContext import FishContext
from fishbase.EnumBase import *
import sqlalchemy as db
from sqlalchemy_utils import database_exists, create_database


# import sqlite3
# con = sqlite3.connect("tutorial.db")
# cur = con.cursor()
# db = SQLAlchemy(app)
#
# db.create_all()


from sqlalchemy import create_engine, update

memory = True
# if memory:
#     engine = create_engine("sqlite:///:memory:", echo=True)

engine = create_engine("sqlite:///fish.db", echo=True)



#
# if not memory:
#     engine = create_engine("postgresql://localhost/fishdb")
#     if not database_exists(engine.url):
#         create_database(engine.url)
#
#     conn = engine.connect()
#     conn.execute("commit")

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()

from sqlalchemy.orm import declarative_base

Base = declarative_base()
# Base.prepare(autoload_with=engine)


from sqlalchemy import Column, Integer, String


class User(Base):
    __tablename__ = "users"

    # discord id
    id = Column(Integer, primary_key=True)
    disid = Column(Integer)
    context = Column(db.PickleType(), nullable = True)
    fullname = Column(String)
    nickname = Column(String)


    def __init__(self, disid):
        # self.name = name
        self.disid = disid

    def __repr__(self):
        return "<User(disid='%s', fullname='%s', nickname='%s')>" % (
            self.disid,
            self.fullname,
            self.nickname,
        )

    # create funciton to add python object
    def add_python_object(self, object_to_store):
        persistent_python_object = db.Column() # <-- would like to add python object here
        self.context = object_to_store
        return object_to_store


Base.metadata.create_all(engine)

# Create user
adder = User(4855435)
adder.add_python_object(FishContext())
session.add(adder)




# ed_user = User(name="ed", fullname="Ed Jones", nickname="edsnickname")


# print('e')

# Add to database
# db.session.add(adder)
# db.session.commit()

# print(session.query(User))

# Retrieve python object
user = (session.query(User).filter_by(disid=4855435).first())
result = user.context

result.GAME_MODE = GameMode.FREE_PLAY
print(result.GAME_MODE)


stmt = (
    update(User).
    where(User.disid == 4855435).
    values(context=result)
)
session.commit()
# session.query(user).filter(4855435).update({'context': result}, synchronize_session = True)

new = (session.query(User).filter_by(disid=4855435).first())
print(new.context.GAME_MODE)





#
#
# import sqlalchemy as db
# engine = db.create_engine("sqlite:///european_database.sqlite")
#
# metadata = db.MetaData() #extracting the metadata
# division= db.Table('divisions', metadata, autoload=True,autoload_with=engine) #Table object
#
# conn = engine.connect()
# from fishbase import FishContext
# disuser = 389428093
#
# cur.execute("CREATE TABLE fishdb(discorduser, context)")
#
# # if new user
# cur.execute("INSERT INTO fishdb VALUES(?, ?)", (disuser, FishContext))
# con.commit()
#
# # https://stackoverflow.com/questions/23139470/inserting-json-data-into-sql-server-with-python
# # cursor.execute("Insert Into Ticket_Info values (?)", (json.dumps(record),))
#
