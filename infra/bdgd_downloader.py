from os import path, remove
from requests import get
from tqdm import tqdm
from zipfile import ZipFile

class BDGDDownloader:
    def __init__(self, bdgd_id: str, bdgd_name: str, output_folder: str, extract: bool = False, verbose: bool = True):
        self.bdgd_id = bdgd_id
        self.bdgd_name = bdgd_name
        self.output_folder = output_folder
        self.extract = extract
        self.verbose = verbose
        self.zip_path = None
        self.bdgd_path = None

    def __enter__(self) -> str:
        self.zip_path = self.download()
        if self.extract:
            self.bdgd_path = self.extract_zip()
            return self.bdgd_path
        return self.zip_path
        
    def __exit__(self, exc_type, exc_value, traceback):
        self._cleanup()

    def download(self) -> str:
        
        with get(f"https://www.arcgis.com/sharing/rest/content/items/{self.bdgd_id}/data", stream=True) as response:
            response.raise_for_status()
            zip_path = path.join(self.output_folder, f"{self.bdgd_name}.zip")
            
            with open(zip_path, "wb") as f:
                if not self.verbose:
                    f.write(response.content)
                    return zip_path

                total_size = int(response.headers.get('content-length', 0))
                with tqdm(total=total_size, unit='B', unit_scale=True, desc=f"Downloading {self.bdgd_name}") as pbar:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            pbar.update(len(chunk))
        return zip_path
    
        

    def extract_zip(self) -> str:
        """Extrai o arquivo ZIP e retorna o caminho do GDB extraído"""
        if not self.zip_path or not path.exists(self.zip_path):
            raise FileNotFoundError(f"ZIP file {self.zip_path} does not exist.")
        
        with ZipFile(self.zip_path, "r") as zip_ref:
            # Pega o primeiro diretório (assumindo que é o GDB)
            files = zip_ref.infolist()
            gdb_file = files[0].filename.split('/')[0]
            extract_path = path.join(self.output_folder, gdb_file)

            if not self.verbose:
                zip_ref.extractall(self.output_folder)
                return extract_path
            
            for file in tqdm(files, desc=f"Extracting {self.bdgd_name}", unit="file"):
                zip_ref.extract(file, self.output_folder)

        return extract_path

    def _cleanup(self):
        """Limpa arquivos temporários"""
        if self.zip_path and path.exists(self.zip_path):
            remove(self.zip_path)
        if self.bdgd_path and path.exists(self.bdgd_path):
            remove(self.bdgd_path)
