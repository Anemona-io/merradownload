import argparse
import logging
from opendap_download.multi_processing_download import DownloadManager


def main():
    parser = argparse.ArgumentParser(
        description='Download MERRA-2 data from NASA GES DISC',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument('--username', required=True, help='Earthdata username')
    parser.add_argument('--password', required=True, help='Earthdata password')
    parser.add_argument('--urls-file', required=True,
                        help='Path to a text file with one download URL per line')
    parser.add_argument('--output-dir', default='download', help='Download directory')
    parser.add_argument('--threads', type=int, default=4, help='Number of download threads')
    parser.add_argument('--verbose', action='store_true')
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.WARNING)

    with open(args.urls_file) as f:
        urls = [line.strip() for line in f if line.strip()]

    dm = DownloadManager(
        username=args.username,
        password=args.password,
        links=urls,
        download_path=args.output_dir,
    )
    dm.start_download(nr_of_threads=args.threads)


if __name__ == '__main__':
    main()
