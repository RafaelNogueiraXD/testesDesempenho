from sqlalchemy import Column, Integer, String, Float
from .database import Base

class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    descricao = Column(String(300), nullable=True)
    preco = Column(Float, nullable=False)
    quantidade = Column(Integer, default=0)
