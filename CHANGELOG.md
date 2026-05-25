# Changelog

All notable changes will be documented here.

## [1.0.0] - 2026-05-25

### Added
- `src/` layout and `pyproject.toml` — package is now pip-installable (`pip install merradownload`)
- `merradownload` CLI entry point for driving downloads from the command line
- Progress bar via `tqdm` during parallel downloads
- Retry on HTTP 5xx errors (3 retries, exponential backoff) via `urllib3.Retry`
- Skip-if-already-downloaded logic to resume interrupted downloads
- Per-file error logging instead of silent failures

### Changed
- Replaced `multiprocessing.dummy.Pool` with `concurrent.futures.ThreadPoolExecutor`
- `yaml.load()` replaced with `yaml.safe_load()` (security fix)
- Updated User-Agent string from Chrome 40 (2015) to Chrome 124
- Fixed `generate_url_params` chained-map iterator bug in example script
- `merra_scraping.py` moved to `examples/` and `%time` magic replaced with `time.perf_counter()`

### Fixed
- Typo in private method name (`__create_authenticated_sesseion`)
- Typo in `__main__` block (`downlaod123`)
- Bare `except:` in example script replaced with `except Exception as e`

## [0.1.0] - (original release)
Initial version by Jan Urbansky.
