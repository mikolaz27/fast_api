import os

from databases import Database
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime, func

DATABASE_URL = os.getenv('DATABASE_URL', "sqlite:///posts.db")

engine = create_engine(DATABASE_URL)
metadata = MetaData()

posts = Table(
    "posts",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String(50)),
    Column("description", String(200)),
    Column("created_by", String(50)),
    Column("created_date", DateTime, default=func.now(), nullable=False),
)

database = Database(DATABASE_URL)
