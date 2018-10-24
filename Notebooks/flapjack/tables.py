from sqlalchemy import Column, Float, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class experiment(Base):
    __tablename__ = 'experiment'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    machine = Column(String)

class dna(Base):
    __tablename__ = 'dna'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    sequence = Column(String)

class sample(Base):
    __tablename__ = 'sample'
    id = Column(Integer, primary_key=True)
    experiment_id = Column(Integer, ForeignKey(experiment.id))
    row = Column(Integer)
    col = Column(Integer)
    media = Column(String)
    strain = Column(String)


class supplement(Base):
    __tablename__ = 'supplement'
    id = Column(Integer, primary_key=True)
    sample_id = Column(Integer, ForeignKey(sample.id))
    name = Column(String)
    concentration = Column(Float)

class vector(Base):
    __tablename__ = 'vector'
    id = Column(Integer, primary_key=True)
    dna_id = Column(Integer, ForeignKey(dna.id))
    sample_id = Column(Integer, ForeignKey(sample.id))

class measurement(Base):
    __tablename__ = 'measurement'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    value = Column(Float)
    time = Column(Float)
    sample_id = Column(Integer, ForeignKey(sample.id))

