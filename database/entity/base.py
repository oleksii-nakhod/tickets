import datetime
from typing import List
from sqlalchemy import create_engine, text, MetaData, Table, Column, Integer, String, ForeignKey, select, update, insert, and_
from sqlalchemy.orm import Session, DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass