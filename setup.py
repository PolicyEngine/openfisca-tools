from setuptools import setup, find_packages

setup(
    name="OpenFisca-Tools",
    version="0.10.1",
    author="PolicyEngine",
    license="http://www.fsf.org/licensing/licenses/agpl-3.0.html",
    url="https://github.com/policyengine/openfisca-tools",
    install_requires=[
        "OpenFisca-Core",
        "microdf_python",
        "numpy",
        "pandas",
        "wheel",
        "h5py",
        "tables",
        "google-cloud-storage",
    ],
    extras_require={
        "test": [
            "OpenFisca-US>=0.35.0",
            "OpenFisca-UK>=0.12.0",
        ]
    },
    packages=find_packages(),
)
