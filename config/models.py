#encoding=utf-8
from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.dialects.mysql import VARCHAR, DATETIME,DATE,FLOAT 
from sqlalchemy.engine.url import URL 
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker

import settings


def build_session(db_name='knownews',pool=True,transaction=True):
    if pool:
        return sessionmaker(bind=create_engine( URL(**settings.DATABASE[db_name]),connect_args={'charset':'utf8'}, pool_size=5, pool_recycle=290),autocommit=not transaction)()

    return sessionmaker(bind=create_engine( URL(**settings.DATABASE[db_name]),connect_args={'charset':'utf8'}, poolclass=NullPool), autocommit=not transaction)()


DeclarativeBase=declarative_base()
def create_knownews_table(engine):
    DeclarativeBase.metadata.create_all(engine)


class WebNews(DeclarativeBase):
    __tablename__='webnews'
    id = Column('id',Integer,primary_key=True)
    title = Column('title',VARCHAR(256))
    abstract = Column('abstract',VARCHAR(64000))
    content = Column('content',VARCHAR(64000))
    source_id = Column('source_id',Integer)
    created_at = Column('created_at',DATETIME)
    keywords = Column('keywords', VARCHAR(6400)) 

    def __init__(self,title,abstract,content,source_id,created_at,keywords):
        self.title=title
        self.abstract=abstract
        self.content=content
        self.source_id=source_id
        self.created_at=created_at
        self.keywords=keywords

class RawContents(DeclarativeBase):
    __tablename__='rawcontents'
    id = Column('id',Integer,primary_key=True)
    title = Column('title',VARCHAR(256))
    content = Column('content',VARCHAR(64000))
    source = Column('source',VARCHAR(64))
    created_at = Column('created_at',DATETIME)

    def __init__(self,title,content,source,created_at):
        self.title=title
        self.content=content
        self.source=source
        self.created_at=created_at

class NewsWebsites(DeclarativeBase):
    __tablename__ = 'newswebsites'
    id = Column('id', Integer, primary_key=True)
    name_en = Column('name_en', VARCHAR(64))
    name_cn = Column('name_cn', VARCHAR(100))
    url = Column('url', VARCHAR(200))

    def __init__(self, name_en, name_cn, url):
        self.name_en = name_en
        self.name_cn = name_cn
        self.url = url

class KeywordsExplain(DeclarativeBase):
    __tablename__ = 'keywordsexplain'
    id = Column('id', Integer, primary_key=True)
    keyword = Column('keyword', VARCHAR(10))
    explaination = Column('explaination', VARCHAR(640))

    def __init__(self, keyword, explaination):
        self.keyword = keyword
        self.explaination = explaination
