# 
# !!!!!!!!!!!!устарело удалить после тестирования
# tables = ['CREATE TABLE IF NOT EXISTS client(id SERIAL PRIMARY KEY, login char(32))',
#         'CREATE TABLE IF NOT EXISTS user(id SERIAL PRIMARY KEY, login char(32), password char(32))',
#         'CREATE TABLE IF NOT EXISTS client_history (client_id INT NOT NULL, request char(32), date CHAR(20), FOREIGN KEY (client_id) REFERENCES client(id) ON UPDATE CASCADE ON DELETE CASCADE)',
#         'CREATE TABLE IF NOT EXISTS user_history (user_id INT NOT NULL, request char(32), date CHAR(20), FOREIGN KEY (user_id) REFERENCES user(id) ON UPDATE CASCADE ON DELETE CASCADE)',
#         'CREATE TABLE IF NOT EXISTS user_client (user_id INT not null, client_id INT not null, FOREIGN KEY (client_id) REFERENCES client(id) ON UPDATE CASCADE ON DELETE CASCADE, FOREIGN KEY (user_id) REFERENCES user(id) ON UPDATE CASCADE ON DELETE CASCADE)',
#         'CREATE TABLE IF NOT EXISTS friends(im INT not null, friend INT not null, FOREIGN KEY (im) REFERENCES user(id) ON UPDATE CASCADE ON DELETE CASCADE, FOREIGN KEY (friend) REFERENCES user(id) ON UPDATE CASCADE ON DELETE CASCADE)',
#         'CREATE TABLE IF NOT EXISTS frendship_request(im INT not null, friend INT not null, FOREIGN KEY (im) REFERENCES user(id) ON UPDATE CASCADE ON DELETE CASCADE, FOREIGN KEY (friend) REFERENCES user(id) ON UPDATE CASCADE ON DELETE CASCADE)',]

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from server_prop import DB_SERVER

Base = declarative_base()

class Client(Base):
    def __init__(self, ip, user_id):
        self.ip = ip
        self.user_id = user_id

    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True)
    ip = Column(String(10))
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship('Users', back_populates='client')



class Users(Base):
    def __init__(self, login, password):
        self.login = login
        self.password = password

    __tablename__='users'

    id = Column(Integer, primary_key=True)
    login = Column(String(32))
    password = Column(String(32))

    client = relationship("Client",  back_populates="user")
    histor = relationship("History", back_populates="user")
  
    def __repr__(self):
        return f"{self.id} {self.login} {self.password}"





class History(Base):
    def __init__(self, request, user_id):
        self.request = request
        self.user_id = user_id

    __tablename__ = 'user_history'

    id = Column(Integer, primary_key=True)
    request = Column(String(15))
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship('Users', back_populates='histor')




class Frends(Base):
    def __init__(self, im, my_friend):
        self.im = im
        self.my_friend = my_friend

    __tablename__ = 'frends'
    id = Column(Integer, primary_key=True)
    im = Column(Integer)
    my_friend = Column(Integer)
    im_id = relationship('Users', ForeignKey("users.id"), back_populates='friends')
    my_friend_id = relationship('Users', ForeignKey("users.id"), back_populates='friends')
    


class Frend_request(Base):
    def __init__(self, im, my_friend):
        self.im = im
        self.my_friend = my_friend

    __tablename__ = 'frend_req'
    id = Column(Integer, primary_key=True)
    im = Column(Integer)
    my_friend = Column(Integer)
    im_id = relationship('Users', ForeignKey("users.id"), back_populates='frend_req')
    my_friend_id = relationship('Users', ForeignKey("users.id"), back_populates='frend_req')
    


if __name__ == '__main__':
    engine = create_engine(f"sqlite:///{DB_SERVER}", echo=True, future=True)
    Base.metadata.create_all(engine)