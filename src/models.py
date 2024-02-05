from datetime import datetime

from sqlalchemy import Table, Column, String, Integer, MetaData

metadata = MetaData()

parstext = Table(
    "parstext",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("datetime", String),
    Column("title", String, nullable=True),
    Column("count_x", Integer, default=0),
)
