import sys
from tqdm import tqdm


class TqdmUpTo(tqdm):
    r"""
    A wrapper class around the tqdm progress bar that can be used for showing download progress.
    Provides `update_to(n)` which uses `tqdm.update(delta_n)`.
    Taken from https://gist.github.com/leimao/37ff6e990b3226c2c9670a2cd1e4a6f5,
    Inspired by [twine#242](https://github.com/pypa/twine/pull/242),
    [mentioned here](https://github.com/pypa/twine/commit/42e55e06).
    """
    def update_to(self, b=1, bsize=1, tsize=None):
        r"""
        Updates the tqdm progress indicator.
        b (int): Number of blocks transferred so far [default: 1].
        bsize (int): Size of each block (in tqdm units) [default: 1].
        tsize (int): Total size (in tqdm units). If [default: None] remains unchanged.
        """
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)  # will also set self.n = b * bsize


def download_from_url(url: str, dst_path : str):
    r"""
    Downloads the contents of specified URL to the specified destination filepath.
    Uses :class:`TqdmUpTo` to show download progress.
    Args:
        url (str): The URL to download from.
        dst_path (str): The path to save the downloaded data to.
    """
    if sys.version_info[0] == 2:
        from urllib import urlretrieve
    else:
        from urllib.request import urlretrieve
    filename = url.split("/")[-1]
    print(f"Downloading from {url}...")
    with TqdmUpTo(unit='B', unit_scale=True, unit_divisor=1024, miniters=1, desc=filename) as t:
        urlretrieve(url, dst_path, reporthook=t.update_to)