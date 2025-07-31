from domain.bdgd import *
from domain.bdgd.conductor import Conductor

class ConnectionBranch(BDGDBase):
    """Ramal de Ligação (RAMLIG)"""
    __tablename__ = 'connection_branch'
    electrical_link_1: Mapped[str_40]
    electrical_link_2: Mapped[str_40]
    conductor_cod_id: Mapped[ConductorFk]
    length: Mapped[float]

    conductor: Mapped[Conductor] = relationship()

    def __repr__(self) -> str:
        return f'ConnectionBranch(cod_id={self.cod_id}, electrical_link_1={self.electrical_link_1}, electrical_link_2={self.electrical_link_2}, conductor_cod_id={self.conductor_cod_id}, length={self.length})'
