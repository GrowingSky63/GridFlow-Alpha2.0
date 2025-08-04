from infra.bdgd_downloader import BDGDDownloader
from sqlalchemy import URL, create_engine
from concurrent.futures import ProcessPoolExecutor, as_completed
from tempfile import TemporaryDirectory
from time import time
import geopandas as gpd
import dotenv, os, json

dotenv.load_dotenv(dotenv.find_dotenv())

REGISTRY_CHUNK_SIZE = 5000

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

with open('gdbs.json') as bdgds_file:
    bdgds = json.loads(bdgds_file.read())

def ensure_tables_exist(conn, layers_columns, table_names):
    import pandas as pd
    for layer, columns in layers_columns.items():
        df = pd.DataFrame(columns=columns.values())
        df.to_sql(
            table_names[layer],
            con=conn,
            if_exists='append',
            index=False
        )

def create_gdf(columns):
    gdf = gpd.GeoDataFrame(columns=columns.values())
    have_geom = 'geometry' in gdf.columns
    gdf.rename(columns=columns, inplace=True)
    if have_geom:
        gdf.set_geometry('geometry_obj', inplace=True)
        gdf['geometry'] = gdf.geometry.apply(lambda geom: geom.wkb)
        columns['geometry'] = 'geometry'
    return gdf[columns.values()]


def open_gdf(bdgd_path, layer, columns):
    t_start = time()
    gdf = gpd.read_file(bdgd_path, layer=layer)
    print(f"\033[32mgdf da camada {layer} instanciado na memória ({time() - t_start:.2f} s)\033[m")
    have_geom = 'geometry' in gdf.columns
    gdf.rename(columns=columns, inplace=True)
    if have_geom:
        gdf.set_geometry('geometry_obj', inplace=True)
        gdf['geometry'] = gdf.geometry.apply(lambda geom: geom.wkb)
        columns['geometry'] = 'geometry'
    return gdf[columns.values()]

def write_gdf_into_gdb(layer, columns, chunk_size=10000, bdgd_path: str | None = None):
    gdf = create_gdf(columns) if not bdgd_path else open_gdf(bdgd_path, layer, columns)
    t_start = time()
    with engine.connect() as conn:
        for i in range(0, len(gdf), chunk_size):
            chunk = gdf.iloc[i:i+chunk_size]
            chunk.to_sql(
                table_names[layer],
                con=conn,
                if_exists='append',
                index=False
            )
            del chunk
    del gdf
    print(f"\033[32mgdf da camada {layer} inserido no banco ({time() - t_start:.2f} s)\033[m")

with TemporaryDirectory(prefix='gridflow') as temp_dir:
    for bdgd_name, bdgd_id in bdgds.items():
        print(f"\033[32mIniciando processamento do gdb {bdgd_name}\033[m")
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
            extract=True
        )

        with downloader as bdgd_path:
            print("\033[32mDownload Iniciado\033[m")
            [write_gdf_into_gdb(layer, columns, REGISTRY_CHUNK_SIZE) for layer, columns in layers_columns.items()]
            with ProcessPoolExecutor(max_workers=2) as executor:
                futures = [executor.submit(write_gdf_into_gdb, layer, columns, REGISTRY_CHUNK_SIZE, bdgd_path) for layer, columns in layers_columns.items()]
            for future in as_completed(futures):
                print(future.result())