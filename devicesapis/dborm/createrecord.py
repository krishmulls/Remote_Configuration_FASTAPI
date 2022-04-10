from sqlalchemy import Column, Integer, MetaData, String, Table, create_engine

engine = create_engine("sqlite:///./User.db", echo=True)
meta = MetaData()

students = Table(
    "device",
    meta,
    Column("id", Integer, primary_key=True),
    Column("devicename", String),
    Column("configip", String),
    Column("port", String),
)

ins = students.insert()
ins = students.insert().values(
    devicename="pm100d1", configip="192.168.0.197", port="8000"
)
conn = engine.connect()
result = conn.execute(ins)
