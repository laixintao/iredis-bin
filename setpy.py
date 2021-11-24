import os
import tarfile
import urllib.request

import shutil

from setuptools import setup
from distutils.command.install_scripts import install_scripts
from tempfile import TemporaryDirectory
from distutils import log
from stat import ST_MODE


VERSION = "1.9.4"


def download_binary(path):
    url = f"https://github.com/laixintao/iredis/releases/download/v{VERSION}/iredis.tar.gz"
    log.info("Downloading binary from %s", url)
    urllib.request.urlretrieve(url, os.path.join(path, "iredis.tar.gz"))
    tarball = os.path.join(path, "iredis.tar.gz")
    with tarfile.open(tarball, "r:gz") as tar:
        tar.extractall(path)
    return path


class InstallTokei(install_scripts):
    def run(self):
        with TemporaryDirectory() as tmpdir:
            binary_path = download_binary(tmpdir)
            target_path = os.path.join(self.install_dir, "iredis")
            os.makedirs(self.install_dir)
            log.info("Copying %s to %s", binary_path, target_path)
            if os.path.exists(target_path):
                os.remove(target_path)
            shutil.copytree(binary_path, target_path)
        if os.name == "posix":
            mode = ((os.stat(target_path)[ST_MODE]) | 0o555) & 0o7777
            os.chmod(target_path, mode)


setup(
    name="iredis-bin",
    version=VERSION,
    cmdclass={"install_scripts": InstallTokei},
    has_ext_modules=lambda: True,
)
