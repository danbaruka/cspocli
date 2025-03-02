from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="cardano-spo-cli",
    version="1.0.0",
    author="Cardano SPO CLI",
    author_email="support@cardano-spo-cli.org",
    description="Professional CLI tool for Cardano Stake Pool Operator wallet setup",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cardano-spo-cli",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
        "click>=8.0.0",
        "cryptography>=3.4.0",
        "mnemonic>=0.20.0",
        "bech32>=1.2.0",
    ],
    entry_points={
        "console_scripts": [
            "cspocli=cardano_spo_cli.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "cardano_spo_cli": ["*.txt", "*.md"],
    },
)
