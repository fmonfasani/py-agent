#!/usr/bin/env python3
"""
py-agent-client setup script
"""

from setuptools import setup, find_packages
import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# Version
VERSION = "0.1.0"

setup(
    name="py-agent-client",
    version=VERSION,
    description="Intelligent AI API routing with automatic cost optimization",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/py-agent/client",
    author="py-agent Team",
    author_email="hello@py-agent.com",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    packages=find_packages(exclude=["tests", "tests.*"]),
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=[
        "httpx>=0.25.0",
        "pydantic>=2.0.0", 
        "python-dotenv>=1.0.0",
        "tenacity>=8.0.0",
        "rich>=13.0.0",
        "tiktoken>=0.5.0",
        "openai>=1.0.0",
        "anthropic>=0.8.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.0.0", 
            "pytest-mock>=3.10.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "pre-commit>=3.0.0",
        ],
        "docs": [
            "mkdocs>=1.5.0",
            "mkdocs-material>=9.0.0",
            "mkdocstrings[python]>=0.22.0",
        ],
        "test": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.0.0",
            "pytest-mock>=3.10.0", 
            "responses>=0.23.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "py-agent=py_agent_client.cli:main",
        ],
    },
    project_urls={
        "Homepage": "https://py-agent.com",
        "Documentation": "https://docs.py-agent.com", 
        "Repository": "https://github.com/py-agent/client",
        "Issues": "https://github.com/py-agent/client/issues",
        "Changelog": "https://github.com/py-agent/client/blob/main/CHANGELOG.md",
    },
    keywords="ai api routing optimization openai anthropic cost",
)