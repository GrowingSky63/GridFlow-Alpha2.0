from domain.bdgd import *
from domain.bdgd.connection_branch import ConnectionBranch
from domain.bdgd.generator_unit import GeneratorUnitBT, GeneratorUnitMT

from domain.bdgd.substation import Substation

class ConsumerUnit(BDGDBase):
    """Classe base para unidades consumidoras"""
    __abstract__ = True
    electrical_link: Mapped[str_40]
    substation_cod_id: Mapped[str_40]
    supplied_voltage: Mapped[float] = mapped_column(VoltageType)
    is_active: Mapped[str] = mapped_column(Status)
    connection_date: Mapped[str_10]
    installed_load: Mapped[float]
    #energy_mean: Mapped[float]
    #load_curve: Mapped[LoadCurve]

class ConsumerUnitBT(ConsumerUnit):
    """Unidade Consumidora de Baixa Tensão (UCBT)"""
    __tablename__ = 'consumer_unit_bt'
    generator_unit_bt_cod_id: Mapped[str_40]
    connection_branch_cod_id: Mapped[str_40]
    
    def __repr__(self) -> str:
        return f'ConsumerUnitBT(cod_id={self.cod_id}, electrical_link={self.electrical_link}, supplied_voltage={self.supplied_voltage}, is_active={self.is_active}, connection_date={self.connection_date}, installed_load={self.installed_load}, generator_unit_cod_id={self.generator_unit_bt_cod_id}, connection_branch_cod_id={self.connection_branch_cod_id})'

class ConsumerUnitMT(ConsumerUnit):
    """Unidade Consumidora de Média Tensão (UCMT)"""
    __tablename__ = 'consumer_unit_mt'
    generator_unit_mt_cod_id: Mapped[str_40]


    def __repr__(self) -> str:
        return f'ConsumerUnitMT(cod_id={self.cod_id}, electrical_link={self.electrical_link}, supplied_voltage={self.supplied_voltage}, is_active={self.is_active}, connection_date={self.connection_date}, installed_load={self.installed_load}, generator_unit_mt_cod_id={self.generator_unit_mt_cod_id})'
