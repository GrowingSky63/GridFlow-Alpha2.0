import json
from time import time
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import DBAPIError
from sqlalchemy import URL, create_engine
from tqdm import tqdm
from domain.bdgd import BDGDBase
from domain.bdgd.conductor import Conductor
from domain.bdgd.connection_branch import ConnectionBranch
from domain.bdgd.consumer_unit import ConsumerUnitBT, ConsumerUnitMT
from domain.bdgd.generator_unit import GeneratorUnitBT, GeneratorUnitMT
from domain.bdgd.segment import SegmentMT
from domain.bdgd.substation import Substation
from domain.bdgd.transformer_unit import TransformerUnitMT, TransformerUnitAT
from infra.bdgd_downloader import BDGDDownloader
from tempfile import TemporaryDirectory
import geopandas as gpd
import dotenv, os

dotenv.load_dotenv(dotenv.find_dotenv())

drivername = 'postgresql'
username = 'gridflow'
password = os.getenv('DB_PASSWORD', 'postgres')
host = '172.25.0.233'
port = 5432
database = 'bdgd'
url = URL.create(
    drivername='postgresql',
    username='gridflow',
    password=os.getenv('DB_PASSWORD', 'postgres'),
    host='172.25.0.233',
    port=5432,
    database='bdgd'
)
engine = create_engine(url, echo=False)

BDGDBase.metadata.drop_all(engine)

BDGDBase.metadata.create_all(engine)

Session = sessionmaker(engine)

with open('gdbs.json') as bdgds_file:
    bdgds = json.loads(bdgds_file.read())

with TemporaryDirectory(prefix='gridflow') as temp_dir:
    for bdgd_name, bdgd_id in bdgds.items():
        layers_columns = {
            'SUB': {
                'COD_ID': 'cod_id',
                'DIST': 'dist',
                'POS': 'pos',
                'NOME': 'name',
                'geometry': 'geometry_obj'
            },
            'UNTRAT': {
                'COD_ID': 'cod_id',
                'PAC_1': 'electrical_link_1',
                'PAC_2': 'electrical_link_2',
                'PAC_3': 'electrical_link_3',
                'SUB': 'substation_cod_id',
                'DIST': 'dist',
                'POT_NOM': 'nominal_power',
                'TIP_TRAFO': 'transformer_type',
                'TIP_UNID': 'unit_type',
                'geometry': 'geometry_obj'
            },
            'SEGCON': {
                'COD_ID': 'cod_id',
                'R1': 'nominal_resistence',
                'X1': 'nominal_reactance',
                'CNOM': 'nominal_current',
                'CMAX': 'max_current'
            },
            'SSDMT': {
                'COD_ID': 'cod_id',
                'PAC_1': 'electric_link_1',
                'PAC_2': 'electric_link_2',
                'SUB': 'substation_cod_id',
                'CTMT': 'circuit',
                'TIP_CND': 'conductor_cod_id',
                'COMP': 'length',
                'geometry': 'geometry_obj'
            },
            'UNTRMT': {
                'COD_ID': 'cod_id',
                'PAC_1': 'electrical_link_1',
                'PAC_2': 'electrical_link_2',
                'PAC_3': 'electrical_link_3',
                'SUB': 'substation_cod_id',
                'DIST': 'dist',
                'POT_NOM': 'nominal_power',
                'TIP_TRAFO': 'transformer_type',
                'TIP_UNID': 'unit_type',
                'TEN_LIN_SE': 'secondary_voltage',
                'TAP': 'tap',
                'CONF': 'circuit_configuration_type',
                'geometry': 'geometry_obj'
            },
            'RAMLIG': {
                'COD_ID': 'cod_id',
                'PAC_1': 'electrical_link_1',
                'PAC_2': 'electrical_link_2',
                'TIP_CND': 'conductor_cod_id',
                'COMP': 'length'
            },
            'UCMT_tab': {
                'COD_ID': 'cod_id',
                'PAC': 'electrical_link',
                'SUB': 'substation_cod_id',
                'TEN_FORN': 'supplied_voltage',
                'SIT_ATIV': 'is_active',
                'DAT_CON': 'connection_date',
                'CAR_INST': 'installed_load',
                'CEG_GD': 'generator_unit_mt_cod_id'
            },
            'UCBT_tab': {
                'COD_ID': 'cod_id',
                'PAC': 'electrical_link',
                'SUB': 'substation_cod_id',
                'TEN_FORN': 'supplied_voltage',
                'SIT_ATIV': 'is_active',
                'DAT_CON': 'connection_date',
                'CAR_INST': 'installed_load',
                'CEG_GD': 'generator_unit_bt_cod_id',
                'RAMAL': 'connection_branch_cod_id'
            },
            'UGMT_tab': {
                'COD_ID': 'cod_id',
                'SUB': 'substation_cod_id',
                'TEN_CON': 'supplied_voltage',
                'SIT_ATIV': 'is_active',
                'DAT_CON': 'connection_date',
                'POT_INST': 'installed_load'

            },
            'UGBT_tab': {
                'COD_ID': 'cod_id',
                'SUB': 'substation_cod_id',
                'TEN_CON': 'supplied_voltage',
                'SIT_ATIV': 'is_active',
                'DAT_CON': 'connection_date',
                'POT_INST': 'installed_load'
            }
        }   
        table_names = {
            'SUB': 'substation',
            'UNTRAT': 'transformer_unit_at',
            'SEGCON': 'conductor',
            'SSDMT': 'segment_mt',
            'UNTRMT': 'transformer_unit_mt',
            'RAMLIG': 'connection_branch',
            'UCMT_tab': 'consumer_unit_mt',
            'UCBT_tab': 'consumer_unit_bt',
            'UGMT_tab': 'generator_unit_mt',
            'UGBT_tab': 'generator_unit_bt'
        }

        downloader = BDGDDownloader(
            bdgd_id=bdgd_id,
            bdgd_name=bdgd_name,
            output_folder=temp_dir,
            extract=True,
            verbose=True
        )
        with downloader as bdgd_path:
            for layer, columns in layers_columns.items():
                t_start = time()
                gdf = gpd.read_file(bdgd_path, layer=layer)
                have_geom = 'geometry' in gdf.columns
                gdf.rename(columns=columns, inplace=True)
                if have_geom:
                    gdf.set_geometry('geometry_obj', inplace=True)
                    gdf['geometry'] = gdf.geometry.apply(lambda geom: geom.wkb)
                    columns['geometry'] = 'geometry'
                gdf = gdf[columns.values()]
                with Session.begin() as session:
                    chunk_size = 10000
                    with tqdm(total=len(gdf), desc=f"Inserindo {layer}", unit="reg", unit_scale=True) as pbar:
                        for i in range(0, len(gdf), chunk_size):
                            chunk = gdf.iloc[i:i+chunk_size]
                            try:
                                chunk.to_sql(
                                    table_names[layer],
                                    con=session.get_bind(),
                                    if_exists='append',
                                    index=False
                                )
                            except DBAPIError as exc:
                                if hasattr(exc, 'orig') and hasattr(exc.orig, 'pgcode') and exc.orig.pgcode == '23505': # type: ignore
                                    ...
                                else:
                                    raise exc
                            finally:
                                pbar.update(len(chunk))
                                del chunk

                # print(f"\033[32m{bdgd_name} -> {layer} ({time() - t_start:.2f}s)\033[m")
                del gdf