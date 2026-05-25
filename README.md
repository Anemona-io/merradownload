# merradownload

A Python package for downloading, cleaning, and aggregating meteorological data from NASA's [MERRA-2](https://gmao.gsfc.nasa.gov/reanalysis/MERRA-2/) database.

Originally developed by [Jan Urbansky](https://github.com/emilylaiken/merradownload), adapted from the [Open Power System Data](https://github.com/Open-Power-System-Data/weather_data/blob/master/download_merra2.ipynb) notebook. Edited and maintained by [Anemona](https://anemona.io).

## Installation

```bash
pip install merradownload
```

## Prerequisites: NASA Earthdata account

1. Register at https://urs.earthdata.nasa.gov/
2. Go to **Applications → Authorized Apps → Approve More Applications**
3. Approve **NASA GESDISC DATA ARCHIVE**

## Quick start

### Python API

```python
from opendap_download.multi_processing_download import DownloadManager

dm = DownloadManager(
    username='your_earthdata_username',
    password='your_earthdata_password',
    links=['https://...'],       # list of OPeNDAP query URLs
    download_path='data/output', # where to save .nc4 files
)
dm.start_download(nr_of_threads=5)
```

### CLI

```bash
merradownload \
  --username YOUR_USER \
  --password YOUR_PASS \
  --urls-file urls.txt \
  --output-dir data/output \
  --threads 5
```

`urls.txt` should contain one OPeNDAP query URL per line. See `examples/merra_scraping.py` for how to generate these URLs for a given location, year range, and variable set.

## Example script

`examples/merra_scraping.py` shows a complete end-to-end workflow: coordinate translation → URL generation → download → xarray/pandas processing → CSV and plot outputs.

## Dependencies

| Package | Purpose |
|---|---|
| `requests` | HTTP downloads |
| `urllib3` | Retry logic |
| `tqdm` | Progress bar |
| `pyyaml` | Optional credential file support |

Processing dependencies (used in the example script only, not required by the core package):

```bash
pip install numpy pandas xarray netCDF4 matplotlib
```

## Features

- Parallel downloads via `ThreadPoolExecutor`
- Automatic retry on HTTP 5xx errors (3 retries, exponential backoff)
- Skips already-downloaded files — safe to resume interrupted runs
- Progress bar
- Credential file support (`yaml`)
