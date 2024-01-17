from datetime import datetime


from sqlalchemy import Table, Column, String, Integer, TIMESTAMP, MetaData, insert

metadata = MetaData()

parstext = Table(
    "parstext",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("datetime", String),
    Column("title", String, nullable=True),
    Column("count_x", Integer, default=0),
)

# with open('O_Genri_Testovaya_20_vmeste (1).txt', encoding="utf-8") as book:
#     for line in book:
#         x = line.count('х')
#         incertion_query = insert(parstext).values({"datetime": datetime.utcnow(), "title": "BOOK", "count_x": x})
#         connection.execute(incertion_query)
#         connection.commit()



# incertion_query = insert(parstext).values([
#     {"datetime": datetime.utcnow(), "title": "Niega", "count_x": 0},
#     {"datetime": datetime.utcnow(), "title": "Byniiga", "count_x": 1},
# ])
#
# connection.execute(incertion_query)
# connection.commit()
# select_all_query = select(parstext)
# select_all_result = connection.execute(select_all_query)
#
# print(select_all_result.all())