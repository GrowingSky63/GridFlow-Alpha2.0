from domain.bdgd import *
from domain.bdgd.substation import Substation

class TransformerUnit(BDGDBase):
    """Classe base para unidades transformadoras"""
    __abstract__ = True
    electrical_link_1: Mapped[str_40]
    electrical_link_2: Mapped[str_40]
    electrical_link_3: Mapped[str_40 | None]
    substation_cod_id: Mapped[SubstationFk]
    dist: Mapped[int]
    nominal_power: Mapped[float]
    transformer_type: Mapped[str] = mapped_column(TransformerType)
    unit_type: Mapped[str] = mapped_column(UnitType)
    geometry = mapped_column(Point, nullable=False)
    @declared_attr
    def substation(cls) -> Mapped[Substation]:
        return relationship(Substation)

class TransformerUnitMT(TransformerUnit):
    """Unidade Transformadora de Média Tensão (UNTRMT)"""

    __tablename__ =  'transformer_unit_mt'

    secondary_voltage: Mapped[float] = mapped_column(VoltageType)
    tap: Mapped[float]
    circuit_configuration_type: Mapped[str] = mapped_column(CircuitConfigurationType)
    
    def __repr__(self) -> str:
        return f'TransformerUnitMT(cod_id={self.cod_id}, electrical_link={self.electrical_link_1}, electrical_link_2={self.electrical_link_2}, electrical_link_3={self.electrical_link_3}, substation_cod_id={self.substation_cod_id}), dist={self.dist}, nominal_power={self.nominal_power}, transformer_type={self.transformer_type}, unit_type={self.unit_type}, secondary_voltage={self.secondary_voltage}, tap={self.tap}, circuit_configuration_type={self.circuit_configuration_type})'

class TransformerUnitAT(TransformerUnit):
    """Unidade Transformadora de Alta Tensão (UNTRAT)"""
    
    __tablename__ =  'transformer_unit_at'

    def __repr__(self) -> str:
        return f'TransformerUnitAT(cod_id={self.cod_id}, electrical_link={self.electrical_link_1}, electrical_link_2={self.electrical_link_2}, electrical_link_3={self.electrical_link_3}, substation_cod_id={self.substation_cod_id}), dist={self.dist}, nominal_power={self.nominal_power}, transformer_type={self.transformer_type}, unit_type={self.unit_type})'
