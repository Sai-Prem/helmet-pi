from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR
from sqlalchemy.orm import declarative_base, sessionmaker

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

engine = create_engine("sqlite:///mydb.db", echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

p1 = Person(16, "meA", "smihas", "saiprem@gmail.com", "hello")
session.add(p1)
session.commit()

results = session.query(Person).all()
print(results)