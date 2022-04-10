from sqlalchemy import Column, Integer, MetaData, String, Table, create_engine

engine = create_engine("sqlite:///./User.db", echo=True)
meta = MetaData()

Query = Table(
    "device",
    meta,
    Column("id", Integer, primary_key=True),
    Column("devicename", String),
    Column("configip", String),
    Column("port", String),
)

conn = engine.connect()
stmt = Query.update().where(
                            Query.c.devicename == "pm100d0").values(
                                port="7500")
conn.execute(stmt)
s = Query.select()
conn.execute(s).fetchall()
