import os
import tarfile

try:
    from urllib.request import urlretrieve
except ImportError:
    from urllib import urlretrieve

import shutil

from setuptools import setup
from distutils.command.install_scripts import install_scripts
from backports.tempfile import TemporaryDirectory

from distutils import log
from stat import ST_MODE


VERSION = "1.9.4"


def download_binary(path):
    url = "https://github.com/laixintao/iredis/releases/download/v{}/iredis.tar.gz".format(
        VERSION
    )
    log.info("Downloading binary from %s", url)
    urlretrieve(url, os.path.join(path, "iredis.tar.gz"))
    tarball = os.path.join(path, "iredis.tar.gz")
    with tarfile.open(tarball, "r:gz") as tar:
        tar.extractall(path)
    return path


class InstallTokei(install_scripts):
    def run(self):
        with TemporaryDirectory() as tmpdir:
            binary_path = download_binary(tmpdir)
            target_path = os.path.join(self.install_dir, "iredis")
            lib_path = os.path.join(self.install_dir, "lib")
            os.makedirs(self.install_dir)
            log.info("Copying %s/lib to %s", binary_path, lib_path)
            shutil.copytree(os.path.join(binary_path, "lib"), lib_path)
            log.info("Copying %s/iredis to %s", binary_path, target_path)
            shutil.copy2(os.path.join(binary_path, "iredis"), target_path)
        if os.name == "posix":
            mode = ((os.stat(target_path)[ST_MODE]) | 0o555) & 0o7777
            os.chmod(target_path, mode)


setup(
    name="iredis-bin",
    version=VERSION,
    cmdclass={"install_scripts": InstallTokei},
    has_ext_modules=lambda: True,
)
