from random import choice

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ddl import Users, History, Frends, Frend_request, Client
from server_prop import DB_SERVER

count_item = 5




def fill_db():
    rand_li = [i for i in range(count_item)]


    engine = create_engine(f"sqlite:///{DB_SERVER}") 
    Session = sessionmaker(bind=engine)

    with Session() as session:
        try:
            # User_li = []
            # History_li = []
            # Frends_li = []
            # Frend_request_li = []
            # Clinet_li = []
            # for i in range(count_item):
            #     User_li.append(Users(f'login_{i}', f'password_{i}'))
            #     History_li.append(History(f'request_{i}', {i}))
            #     Frends_li.append(Frends(choice(rand_li), choice(rand_li)))
            #     Frend_request_li.append(Frend_request(choice(rand_li), choice(rand_li)))
            #     Clinet_li.append(Client(f'ip_{i}', i))

            session.add(Users(login='login_', password='password'))
            session.commit()
        finally:
            session.close()

if __name__ == '__main__':
    fill_db()