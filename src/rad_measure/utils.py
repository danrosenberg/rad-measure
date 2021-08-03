from tqdm import tqdm

import os
from pathlib import Path
import urllib.request
import zipfile


class DownloadProgressBar(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)


def download_url(url, output_path):
    """Download `url` to `output_path` and show a progress bar."""
    # Create parent directories of the file in `output_path`
    Path(os.path.dirname(output_path)).mkdir(parents=True, exist_ok=True)
    # Download
    with DownloadProgressBar(unit='B', unit_scale=True,
                             miniters=1, desc=url.split('/')[-1]) as pbar:
        urllib.request.urlretrieve(url, filename=output_path, reporthook=pbar.update_to)


def extract_zip(zip_path, ret_extracted_path=False):
    """Extract a zip and delete the .zip file."""
    dir_parents = os.path.dirname(zip_path)
    dir_name = Path(zip_path).stem
    extracted_path = os.path.join(dir_parents, dir_name, '')
    if ret_extracted_path:
        return extracted_path

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(dir_parents)
    os.remove(zip_path)
    print(f"Extracted '{Path(zip_path).name}' to '{extracted_path}'.")
