from server_prop import DB_SERVER




from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    def __init__(self, name, fullname, password, addresses):
        self.name = name
        self.fullname = fullname
        self.password = password
        self.addresses = addresses

    __tablename__ = "user_account"

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    fullname = Column(String(20))
    password = Column(String(20))

    addresses = relationship(
        "Address", back_populates="user", cascade="all, delete-orphan"
    )

    

    def __repr__(self):
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"

class Address(Base):
    def __init__(self, email_address):
        self.email_address = email_address


    __tablename__ = "address"

    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("user_account.id"), nullable=False)

    user = relationship("User", back_populates="addresses")

    def __repr__(self):
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"


from sqlalchemy import create_engine
engine = create_engine(f"sqlite:///{DB_SERVER}",  future=True)  # echo=True,
    # echo=True вывод отладочной информации
    # future=True гарантирует работу в SQLAlchemy 2.0-style


# Base.metadata.create_all(engine)


from sqlalchemy.orm import sessionmaker


# Session = sessionmaker(bind=engine)
# session = Session()

from sqlalchemy.orm import Session

# with Session(engine) as session:

#     spb = User('Spb_bob', 'Spangebob', 'pswd', [Address('dfg@ua.com')])
#     sand = User(name="Sandy", fullname='Sandy_mandy', password='pswd', addresses=[Address('dfg@ua.com'), Address('dgfd@dfg.uf')])
#     # spongebob = User(name="spongebob", fullname="Spongebob Squarepants", addresses=[Address(email_address="spongebob@sqlalchemy.org")],)
#     # sandy = User(
#     #     name="sandy",
#     #     fullname="Sandy Cheeks",
#     #     addresses=[
#     #         Address(email_address="sandy@sqlalchemy.org"),
#     #         Address(email_address="sandy@squirrelpower.org"),
#     #     ],
#     # )
#     # patrick = User(name="patrick", fullname="Patrick Star")
# # 
#     session.add_all([spb, sand])

#     session.commit()


# vasya = User('Vasya', 'Vasiliy Perdunov2', 'pswd2', )
# session.add(vasya)

# session.add_all([User("kolia", "Cool Kolian[S.A.]","kolia$$$"), User("zina", "Zina Korzina", "zk18")])


# session.commit()

# needUser = session.query(User).filter_by(name='Vasya').first()
# print(needUser.password) 


# needUser2 = session.query(User).filter_by(name='kolia').first()
# print(needUser2.name) 


# print(session.IdentitySet)

# for instance in session.query(User).order_by(User.id): 
#     print(instance.name, instance.fullname)

# for name, fullname in session.query(User.name, User.fullname): 
#     print(name, fullname)

# for row in session.query(User, User.name).all(): 
#    print(row.User, row.name)

# for u in session.query(User).order_by(User.id)[1:2]: 
#    print(u)

from sqlalchemy import select

session = Session(engine)

# # stmt = select(User).where(User.name.in_(["Spb_bob", "no_name"]))
# # print(stmt)



# # for user in session.scalars(stmt):
# #     print(user)


# stmt = (select(Address).join(Address.user).where(User.name=='Sandy').where(Address.email_address=='dgfd@dfg.uf'))
# sandy_adress = session.scalars(stmt).one()
# print(sandy_adress)
# sandy_adress.email_address = 'xz_adress@mail.ru'  # заменить email

# session.commit()

# stmt = select(User).where(User.name == "Spb_bob")
# spb_bob = session.scalars(stmt).one()
# # print(spb_bob)
# # spb_bob.addresses.append(Address('spbaderess@mail.ru'))
# # session.commit()
# spb_bob.email_address = 'xz_adress@mail.ru'
# session.commit()

sandi = session.get(User, 2)  # поиск по id
print(sandi)
# sandy.addresses.remove(sandy_address)
# session.flush()