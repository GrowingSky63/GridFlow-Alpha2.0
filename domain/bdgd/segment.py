from domain.bdgd import *
from domain.bdgd.conductor import Conductor
from domain.bdgd.substation import Substation

class SegmentMT(BDGDBase):
    """Segmento do Sistema de Distribuição (SSDMT)"""
    __tablename__ = 'segment_mt'
    electric_link_1: Mapped[str_40]
    electric_link_2: Mapped[str_40]
    substation_cod_id: Mapped[str_40]
    circuit: Mapped[str_40]
    conductor_cod_id: Mapped[str_40]
    length: Mapped[float]
    geometry = mapped_column(MultiLinestring, nullable=False)