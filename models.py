import os
import enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import (
    create_engine,
    Table,
    Column,
    Integer,
    String,
    Date,
    Text,
    ForeignKey,
    Enum
)

# engine = create_engine('postgresql://localhost:5432/matts_minis', echo=True)
engine = create_engine('sqlite:///minis.db?check_same_thread=False')
Base = declarative_base()

mini_colors_table = Table('mini_colors', Base.metadata,
    Column('mini_id', Integer, ForeignKey('minis.id')),
    Column('color_id', Integer, ForeignKey('colors.id'))
)

class MagicModel:
    def update(self, **kwargs):
        for key in kwargs:
            value = kwargs[key]
            setattr(self, key, value)
    @classmethod
    def objects(cls):
        return session.query(cls)

class ColorTypes(enum.Enum):
    primer = "primer"
    air = "air"
    base = "base"
    wash = "wash"
    layer = "layer"
    shade = "shade"
    technical = "technical"
    contrast = "contrast"
    misc = "misc"

class Mini(Base, MagicModel):
    __tablename__ = 'minis'
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    figure_type = Column(String)
    nickname = Column(String)
    description = Column(Text)
    retro = Column(Text)
    images = relationship("Image", back_populates="mini")
    colors = relationship("Color", secondary=mini_colors_table, back_populates="minis")
    def __init__(self, date=None, figure_type=None, nickname=None, description=None, retro=None):
        super().__init__()
        self.date = date
        self.figure_type = figure_type
        self.nickname = nickname
        self.description = description
        self.retro = retro
    @property
    def display_name(self):
        return self.nickname or self.figure_type
    @property
    def formatted_date(self):
        if not self.date:
            return ""
        return self.date.strftime("%B %d, %Y")
    @property
    def color_ids(self):
        return [color.id for color in self.colors]


class Color(Base, MagicModel):
    __tablename__ = 'colors'
    id = Column(Integer, primary_key=True)
    type = Column(Enum(ColorTypes))
    name = Column(String)
    hex = Column(String)
    brand = Column(String)
    minis = relationship("Mini", secondary=mini_colors_table, back_populates="colors")
    def __init__(self, type=None, name=None, hex=None, brand=None):
        super().__init__()
        self.type = type
        self.name = name
        self.hex = hex
        self.brand = brand
    @property
    def display_name(self):
        return ' '.join([self.brand, self.name])

class Image(Base, MagicModel):
    __tablename__ = 'images'
    id = Column(Integer, primary_key=True)
    mini_id = Column(Integer, ForeignKey('minis.id'))
    key = Column(String)
    mini = relationship("Mini", back_populates="images")
    def __init__(self, mini_id=None, key=None):
        super().__init__()
        self.mini_id = mini_id
        self.key = key
    @property
    def url(self):
        if os.environ['FLASK_ENV'] == 'development':
            return "/static/minis/"+str(self.mini.id)+"/images/"+self.key+".jpg"
        else:
            pass # TODO: Use S3 for storage for-realsies


Base.metadata.create_all(engine)
_Session = sessionmaker(bind=engine)
session = _Session()
