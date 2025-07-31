from domain import *
from geoalchemy2 import Geometry
from sqlalchemy.types import TypeDecorator, String
from sqlalchemy import Float

str_2 = Annotated[str, 2]
str_10 = Annotated[str, 10]
str_40 = Annotated[str, 40]
str_50 = Annotated[str, 50]
SubstationFk = Annotated[str_40, mapped_column(ForeignKey("substation.cod_id"))]
BusFk = Annotated[str_40, mapped_column(ForeignKey("bus.cod_id"))]
TransformerUnitMTFk = Annotated[str_40, mapped_column(ForeignKey("transformer_unit_mt.cod_id"))]
TransformerUnitATFk = Annotated[str_40, mapped_column(ForeignKey("transformer_unit_at.cod_id"))]
CircuitFk = Annotated[str_40, mapped_column(ForeignKey("circuit.cod_id"))]
ConductorFk = Annotated[str_40, mapped_column(ForeignKey("conductor.cod_id"))]
SegmentMTFk = Annotated[str_40, mapped_column(ForeignKey("segment_mt.cod_id"))]
ConnectionBranchFk = Annotated[str_40, mapped_column(ForeignKey("connection_branch.cod_id"))]
GeneratorUnitBTFk = Annotated[str_40, mapped_column(ForeignKey("generator_unit_bt.cod_id"))]
GeneratorUnitMTFk = Annotated[str_40, mapped_column(ForeignKey("generator_unit_mt.cod_id"))]
ConsumerUnitBTFk = Annotated[str_40, mapped_column(ForeignKey("consumer_unit_bt.cod_id"))]
ConsumerUnitMTFk = Annotated[str_40, mapped_column(ForeignKey("consumer_unit_mt.cod_id"))]
MultiPolygon = Geometry('MULTIPOLYGON', srid=4326)
MultiLinestring = Geometry('MULTILINESTRING', srid=4326)
Point = Geometry('POINT', srid=4326)

VOLTAGE_TYPE_MAP = {
    '0': 0.0, '1': 110.0, '2': 115.0, '3': 120.0, '4': 121.0, '5': 125.0, '6': 127.0,
    '7': 208.0, '8': 216.0, '9': 216.5, '10': 220.0, '11': 230.0, '12': 231.0,
    '13': 240.0, '14': 254.0, '15': 380.0, '16': 400.0, '17': 440.0, '18': 480.0,
    '19': 500.0, '20': 600.0, '21': 750.0, '22': 1000.0, '23': 2200.0, '24': 3200.0,
    '25': 3600.0, '26': 3785.0, '27': 3800.0, '28': 3848.0, '29': 3985.0, '30': 4160.0,
    '31': 4200.0, '32': 4207.0, '33': 4368.0, '34': 4560.0, '35': 5000.0, '36': 6000.0,
    '37': 6600.0, '38': 6930.0, '39': 7960.0, '40': 8670.0, '41': 11400.0,
    '42': 11900.0, '43': 12000.0, '44': 12600.0, '45': 12700.0, '46': 13200.0,
    '47': 13337.0, '48': 13530.0, '49': 13800.0, '50': 13860.0, '51': 14140.0,
    '52': 14190.0, '53': 14400.0, '54': 14835.0, '55': 15000.0, '56': 15200.0,
    '57': 19053.0, '58': 19919.0, '59': 21000.0, '60': 21500.0, '61': 22000.0,
    '62': 23000.0, '63': 23100.0, '64': 23827.0, '65': 24000.0, '66': 24200.0,
    '67': 25000.0, '68': 25800.0, '69': 27000.0, '70': 30000.0, '71': 33000.0,
    '72': 34500.0, '73': 36000.0, '74': 38000.0, '75': 40000.0, '76': 44000.0,
    '77': 45000.0, '78': 45400.0, '79': 48000.0, '80': 60000.0, '81': 66000.0,
    '82': 69000.0, '83': 72500.0, '84': 88000.0, '85': 88200.0, '86': 92000.0,
    '87': 100000.0, '88': 120000.0, '89': 121000.0, '90': 123000.0, '91': 131600.0,
    '92': 131630.0, '93': 131635.0, '94': 138000.0, '95': 145000.0, '96': 230000.0,
    '101': 245000.0, '97': 345000.0, '98': 500000.0, '102': 550000.0, '99': 750000.0,
    '100': 1000000.0
}
REVERSE_VOLTAGE_TYPE_MAP = {v: k for k, v in VOLTAGE_TYPE_MAP.items()}
class VoltageType(TypeDecorator):
    """Converts between float and string representation for VoltageType."""
    impl = String
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is not None:
            return REVERSE_VOLTAGE_TYPE_MAP.get(float(value))
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            return VOLTAGE_TYPE_MAP.get(value)
        return value

    @property
    def python_type(self):
        return float

# TransformerType mapping
TRANSFORMER_TYPE_MAP = {
    '0': 'Não informado',
    'M': 'Monofásico',
    'B': 'Bifásico',
    'T': 'Trifásico',
    'MT': 'Monofásico a três fios',
    'DA': 'Delta aberto',
    'DF': 'Delta fechado'
}
REVERSE_TRANSFORMER_TYPE_MAP = {v: k for k, v in TRANSFORMER_TYPE_MAP.items()}

class TransformerType(TypeDecorator):
    """Converts between string code and description for TransformerType."""
    impl = String
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is not None:
            return REVERSE_TRANSFORMER_TYPE_MAP.get(value, value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            return TRANSFORMER_TYPE_MAP.get(value, value)
        return value

    @property
    def python_type(self):
        return str

# UnitType mapping
UNIT_TYPE_MAP = {
    '0': 'Não informado',
    '1': 'Comparador fiscal ou concentrador',
    '2': 'Medidor eletromecânico',
    '3': 'Medidor eletrônico',
    '52': 'Módulos de Display e/ou Corte-Religa separados do medidor',
    '9': 'Banco de capacitor serial e paralelo',
    '10': 'Banco de capacitores paralelo',
    '11': 'Banco de capacitores serial',
    '12': 'Compensador de reativos estático',
    '51': 'Compensador de reativos rotativo',
    '13': 'Auto booster',
    '14': 'Regulador automático de tensão',
    '15': 'Abertura de jumper',
    '16': 'Chave a gás',
    '17': 'Chave a óleo',
    '18': 'Chave de transferência automática',
    '19': 'Chave faca',
    '20': 'Chave faca tripolar abertura com carga',
    '21': 'Chave faca unipolar abertura com carga',
    '22': 'Chave fusível',
    '23': 'Chave fusível abertura com carga com aterramento',
    '24': 'Chave fusível abertura sem carga',
    '25': 'Chave fusível abertura sem carga com aterramento',
    '26': 'Chave fusível lâmina',
    '27': 'Chave fusível religadora (três operações)',
    '28': 'Chave motorizada',
    '49': 'Chave Tipo Tandem',
    '29': 'Disjuntor',
    '30': 'Disjuntor de interligação de barra',
    '53': 'Disjuntor em módulo de manobra SF6',
    '31': 'Lâmina desligadora',
    '32': 'Religador',
    '33': 'Seccionadora tripolar de subestação',
    '34': 'Seccionadora unipolar de subestação',
    '47': 'Seccionadora com lâmina de terra',
    '48': 'Seccionadora em módulo de manobra',
    '50': 'Seccionadora com bob red corr cc',
    '35': 'Seccionalizador',
    '36': 'Seccionalizador monofásico',
    '45': 'Protetor de Rede de Transformador Subterrâneo',
    '46': 'Fusível',
    '38': 'Transformador de distribuição de média tensão (MT/BT)',
    '41': 'Transformador de força de alta tensão (AT/AT - AT/MT)',
    '54': 'Transformador de força de média tensão (MT/MT)',
    '42': 'Transformador de corrente',
    '43': 'Transformador de potencial',
    '44': 'Conjunto de Medição',
    '55': 'Transformador de defasamento'
}
REVERSE_UNIT_TYPE_MAP = {v: k for k, v in UNIT_TYPE_MAP.items()}

class UnitType(TypeDecorator):
    """Converts between string code and description for UnitType."""
    impl = String
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is not None:
            return REVERSE_UNIT_TYPE_MAP.get(value, value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            return UNIT_TYPE_MAP.get(value, value)
        return value

    @property
    def python_type(self):
        return str

# CircuitConfigurationType mapping
CIRCUIT_CONFIGURATION_TYPE_MAP = {
    '0': 'Não informado',
    'AN': 'Anel',
    'RA': 'Radial',
    'RT': 'Reticulado'
}
REVERSE_CIRCUIT_CONFIGURATION_TYPE_MAP = {v: k for k, v in CIRCUIT_CONFIGURATION_TYPE_MAP.items()}

class CircuitConfigurationType(TypeDecorator):
    """Converts between string code and description for CircuitConfigurationType."""
    impl = String
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is not None:
            return REVERSE_CIRCUIT_CONFIGURATION_TYPE_MAP.get(value, value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            return CIRCUIT_CONFIGURATION_TYPE_MAP.get(value, value)
        return value

    @property
    def python_type(self):
        return str

# Status mapping
STATUS_MAP = {
    '0': 'Não aplicável',
    'AT': 'Ativada',
    'DS': 'Desativada'
}
REVERSE_STATUS_MAP = {v: k for k, v in STATUS_MAP.items()}

class Status(TypeDecorator):
    """Converts between string code and description for Status."""
    impl = String
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is not None:
            return REVERSE_STATUS_MAP.get(value, value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            return STATUS_MAP.get(value, value)
        return value

    @property
    def python_type(self):
        return str

class BDGDBase(DeclarativeBase):
    cod_id: Mapped[Annotated[str_40, mapped_column(primary_key=True)]]
