from domain.bdgd import *

class Conductor(BDGDBase):
    """Segmento Condutor (SEGCON)"""
    __tablename__ = 'conductor'
    nominal_resistence: Mapped[float]
    nominal_reactance: Mapped[float]
    nominal_current: Mapped[float]
    max_current: Mapped[float]

    def __repr__(self) -> str:
        return f'GeneratorUnitMT(cod_id={self.cod_id}, nominal_resistence={self.nominal_resistence}, nominal_reactance={self.nominal_reactance}, nominal_current={self.nominal_current}, max_current={self.max_current})'
