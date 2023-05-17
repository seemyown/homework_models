import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import *

with open('conn_data.txt', 'r') as cd:
    conn = cd.readline()

engine = create_engine(f'postgresql://{conn}')

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

with open('fixtures.json', 'r') as fx:
    records = json.load(fx)

for record in records:
    if record['model'] == 'publisher':
        publisher = Publisher(id=record['pk'], name=record['fields']['name'])
        session.add(publisher)
        session.commit()
    if record['model'] == 'book':
        book = Book(id=record['pk'], title=record['fields']['title'], id_publisher=record['fields']['id_publisher'])
        session.add(book)
        session.commit()
    if record['model'] == 'shop':
        shop = Shop(id=record['pk'], name=record['fields']['name'])
        session.add(shop)
        session.commit()
    if record['model'] == 'stock':
        stock = Stock(id=record['pk'], id_book=record['fields']['id_book'], id_shop=record['fields']['id_shop'], count=record['fields']['count'])
        session.add(stock)
        session.commit()
    if record['model'] == 'sale':
        sale = Sale(id=record['pk'], price=record['fields']['price'], date_sale=record['fields']['date_sale'],id_stock=record['fields']['id_stock'] ,count=record['fields']['count'])
        session.add(sale)
        session.commit()

find = input('Введите автора: ')

datas = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale)\
    .join(Stock, Book.id == Stock.id_book)\
    .join(Shop, Shop.id == Stock.id_shop)\
    .join(Publisher, Book.id_publisher == Publisher.id)\
    .join(Sale, Sale.id_stock == Stock.id)\
    .filter(func.lower(Publisher.name) == find).all()

for data in datas:
    print(data[0],'|',data[1],'|',data[2],'|', data[3].date())


session.close()


    