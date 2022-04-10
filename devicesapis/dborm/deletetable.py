from sqlalchemy import Column, Integer, MetaData, String, Table, create_engine

engine = create_engine("sqlite:///./User.db", echo=True)
meta = MetaData()

Query = Table(
    "Device",
    meta,
    Column("id", Integer, primary_key=True),
    Column("devicename", String),
    Column("configip", String),
    Column("port", String),
)
meta.drop_all(engine)
