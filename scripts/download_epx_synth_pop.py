"""
tools to download and install FRED synthetic populations
"""

import os
import sys
import requests
import argparse
import tarfile
import json

_fname = os.path.join(os.path.dirname(__file__), "synth_pops.json")
with open(_fname) as f:
    synth_pops = json.load(f)


def download_file(url, save_as, chunk_size=8192) -> str:
    """
    Download a file at a given `url`.

    Parameters
    ----------
    url : path-like
        a valid url

    save_as : path-like
        filename used to save download

    Returns
    -------
    local_filename : path-like
        the name of the saved file
    """

    # determine size of file
    response = requests.get(url, stream=True)
    total_length = int(response.headers.get("content-length"))
    response.close()

    # download file
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        local_filename = save_as
        with open(local_filename, "wb") as f:
            dl = 0
            for chunk in r.iter_content(chunk_size=chunk_size):
                f.write(chunk)
                # progress bar
                dl += len(chunk)
                done = int(50 * dl / total_length)
                bar = "".join(("=" * done, " " * (50 - done)))
                per = (dl / total_length) * 100
                sys.stdout.write(f"\r\tprogress: [{bar}] {per:.2f}% done.")
                sys.stdout.flush()
    sys.stdout.write("\r")
    sys.stdout.flush()

    return local_filename


def download_synth_pop(name, version) -> None:
    """ """

    FRED_DATA = os.getenv("FRED_DATA")
    if FRED_DATA is None:
        msg = "FRED_DATA directory not found"
        raise FileNotFoundError(msg)

    print(f"downloading synthetic population: {name} version {version}")
    download_path = os.path.join(FRED_DATA, "fred-data.tar.gz")
    result = download_file(synth_pops[name]["versions"][version]["url"], download_path)
    print(f"successfully downloaded to: {result}")

    print(f"installing synthetic population...")
    data_tar = tarfile.open(download_path)
    data_tar.extractall(FRED_DATA)
    data_tar.close()
    print(f"successfully installed to: {FRED_DATA}")

    print("cleaning up...")
    os.remove(download_path)
    print(f"deleted: {download_path}")

    print("done.")


def _get_cli_parser() -> argparse.ArgumentParser:
    """ """
    parser = argparse.ArgumentParser(
        description=(
            "Download and install a FRED synthetic population "
            "to your local FRED_DATA diretory."
        )
    )
    parser.add_argument(
        "name", type=str, help="a FRED synthetic population name, e.g. RTI_2010"
    )
    parser.add_argument(
        "--version",
        type=str,
        nargs="?",
        help="optionally, specify the synthetic population version.",
        default="default",
    )
    return parser


if __name__ == "__main__":
    # parse cli arguments
    parser = _get_cli_parser()
    args = parser.parse_args()
    name = args.name
    version = args.version
    if version == "default":
        version = synth_pops[name]["default_version"]
    else:
        version = args.version
    download_synth_pop(name=name, version=version)
