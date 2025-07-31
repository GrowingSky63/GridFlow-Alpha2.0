from domain.bdgd import *
from domain.bdgd.conductor import Conductor
from domain.bdgd.substation import Substation

class SegmentMT(BDGDBase):
    """Segmento do Sistema de Distribuição (SSDMT)"""
    __tablename__ = 'segment_mt'
    electric_link_1: Mapped[str_40]
    electric_link_2: Mapped[str_40]
    substation_cod_id: Mapped[SubstationFk]
    circuit: Mapped[str_40]
    conductor_cod_id: Mapped[ConductorFk]
    length: Mapped[float]
    geometry = mapped_column(MultiLinestring, nullable=False)

    substation: Mapped[Substation] = relationship()
    conductor: Mapped[Conductor] = relationship()