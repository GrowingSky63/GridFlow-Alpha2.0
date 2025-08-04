from domain.bdgd import *
from datetime import datetime

from domain.bdgd.substation import Substation

class GeneratorUnit(BDGDBase):
    """Classe base para unidades geradoras"""
    __abstract__ = True
    substation_cod_id: Mapped[str_40]
    supplied_voltage: Mapped[float] = mapped_column(VoltageType)
    is_active: Mapped[str] = mapped_column(Status)
    connection_date: Mapped[str_10]
    installed_load: Mapped[float]
    #energy_mean: Mapped[float]

class GeneratorUnitBT(GeneratorUnit):
    """Unidade Geradora de Baixa Tensão (UGBT)"""
    __tablename__ = 'generator_unit_bt'
    
    def __repr__(self) -> str:
        return f'GeneratorUnitBT(cod_id={self.cod_id}, supplied_voltage={self.supplied_voltage}, is_active={self.is_active}, connection_date={self.connection_date}, installed_load={self.installed_load})'

class GeneratorUnitMT(GeneratorUnit):
    """Unidade Geradora de Média Tensão (UGMT)"""
    __tablename__ = 'generator_unit_mt'
    #demand_mean: Mapped[float]

    def __repr__(self) -> str:
        return f'GeneratorUnitMT(cod_id={self.cod_id}, supplied_voltage={self.supplied_voltage}, is_active={self.is_active}, connection_date={self.connection_date}, installed_load={self.installed_load})'
