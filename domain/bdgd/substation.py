from domain.bdgd import *

class Substation(BDGDBase):
    """Subestação (SUB)"""
    __tablename__ = 'substation'
    dist: Mapped[int]
    pos: Mapped[str_2]
    name: Mapped[str_50]
    geometry = mapped_column(MultiPolygon, nullable=False)

    def __repr__(self) -> str:
        return f'Substation(cod_id={self.cod_id}, dist={self.dist}, pos={self.pos}, name={self.name})'
    