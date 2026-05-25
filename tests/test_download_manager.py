import os
import pytest
import tempfile
import yaml
from opendap_download.multi_processing_download import DownloadManager

VALID_URL = (
    'https://goldsmr4.gesdisc.eosdis.nasa.gov/opendap/MERRA2/M2T1NXSLV.5.12.4/'
    '2017/01/MERRA2_400.tavg1_2d_slv_Nx.20170101.nc4'
    '?U2M[0:1:23][180:1:180][288:1:288]'
)
# get_filename regex matches the stem before .nc4, not including the extension
EXPECTED_FILENAME = 'MERRA2_400.tavg1_2d_slv_Nx.20170101'


class TestGetFilename:
    def test_extracts_correct_filename(self):
        assert DownloadManager.get_filename(VALID_URL) == EXPECTED_FILENAME

    def test_raises_for_malformed_url(self):
        # A URL with no path segments at all — the regex returns None and .group(0) raises AttributeError
        with pytest.raises(AttributeError):
            DownloadManager.get_filename('not-a-url-at-all')


class TestDownloadUrlsSetter:
    def test_accepts_valid_urls(self):
        dm = DownloadManager()
        dm.download_urls = [VALID_URL]
        assert dm.download_urls == [VALID_URL]

    def test_accepts_none(self):
        dm = DownloadManager()
        dm.download_urls = None
        assert dm.download_urls == []

    def test_raises_for_invalid_url(self):
        dm = DownloadManager()
        with pytest.raises(ValueError):
            dm.download_urls = ['https://example.com/not-a-merra-url']


class TestReadCredentialsFromYaml:
    def test_parses_valid_yaml(self):
        dm = DownloadManager()
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump({'username': 'testuser', 'password': 'testpass'}, f)
            tmp_path = f.name
        try:
            dm.read_credentials_from_yaml(tmp_path)
            # If credentials were set correctly, no exception is raised.
            # We verify by checking the internal state indirectly via set_username_and_password
            assert dm._DownloadManager__username == 'testuser'
            assert dm._DownloadManager__password == 'testpass'
        finally:
            os.unlink(tmp_path)


class TestSkipAlreadyDownloaded:
    def test_skips_existing_file(self, tmp_path):
        dm = DownloadManager(
            username='u',
            password='p',
            links=[VALID_URL],
            download_path=str(tmp_path),
        )
        # Pre-create the file that would be downloaded (stem without .nc4, matching get_filename output)
        existing = tmp_path / EXPECTED_FILENAME
        existing.write_bytes(b'existing content')

        # _mp_download_wrapper should return without calling __download_and_save_file
        # If it tried to download, it would fail because there's no real session.
        # The fact that no exception is raised confirms the skip path was taken.
        dm._mp_download_wrapper(VALID_URL)
        assert existing.read_bytes() == b'existing content'
