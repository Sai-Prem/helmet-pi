from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import text

Base = declarative_base()

class Person(Base):
    __tablename__ = "persons"

    ssn = Column("ssn", Integer, primary_key=True)
    firstname = Column("firstname", String)
    lastname = Column("lastname", String)
    email = Column("email", String)
    password = Column("password", String)

    def __init__(self, ssn, firstname, lastname, email, password):
        self.ssn = ssn
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password
    
    def __repr__(self):
        return f"({self.ssn} {self.firstname} {self.lastname} {self.email}, {self.password})"

class Comment(Base):
    __tablename__ = "comments"

    account = Column("account", String)
    comment = Column("comment", String)
    ssn = Column("ssn", Integer, primary_key=True)

    def __init__(self, account, comment, ssn):
        self.account = account
        self.comment = comment
        self.ssn = ssn 
    
    def __repr__(self):
        return f"({self.account} {self.comment} {self.ssn})"

engine = create_engine("sqlite:///mydb.db", echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

results = session.query(Comment).all()
print(results)

# p1 = Person(16, "meA", "smihas", "saiprem@gmail.com", "hello")
# session.add(p1)
# session.commit()

# statement = text("""SELECT * FROM comments""")

# index = 0
# with engine.connect() as con:
#     rs = con.execute(statement)
#     for n in rs:
#         index += 1
#     print(index)


p1 = Comment("me", "hey pressure", 18)
session.add(p1)
session.commit()

results2 = session.query(Comment).all()
print(results2)

for n in results2:
    print(n.account)

# with engine.connect() as con:
#     rs = con.execute(statement)
#     for n in rs:
#         print(n)