from setuptools import setup, find_packages

setup(
    name="dubsar",
    version="1.0.0",
    description="DUB.SAR 1.0 — Executable Mesopotamian Mathematical Tablet Language",
    author="DUB.SAR Contributors",
    packages=find_packages(),
    python_requires=">=3.9",
    entry_points={
        "console_scripts": [
            "dubsar = dubsar.cli:main",
        ],
    },
)
