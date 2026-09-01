from sqlalchemy import Column, Integer, String, Date
from models.conexao import Base


class Equipamento(Base):

    __tablename__ = "equipamentos"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    patrimonio = Column(
        String(100),
        unique=True,
        nullable=False
    )

    tipo = Column(
        String(100),
        nullable=False
    )

    marca = Column(
        String(100),
        nullable=False
    )

    modelo = Column(
        String(100),
        nullable=False
    )

    numero_serie = Column(
        String(150),
        unique=True,
        nullable=False
    )

    data_aquisicao = Column(
        Date,
        nullable=False
    )

    localizacao = Column(
        String(200),
        nullable=False
    )

    status = Column(
        String(50),
        nullable=False
    )