"""
Setup configuration for AI-SRE Agent
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="ai-sre-agent",
    version="0.1.0",
    author="Sebastian Maniak",
    author_email="sebastian@maniak.io",
    description="AI-powered Site Reliability Engineering agent using Kagent and Llama 3.2",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sebbycorp/AI-SRE-With-Kagent-OSS-Llama3.2",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Topic :: System :: Monitoring",
        "Topic :: System :: Systems Administration",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "ai-sre=src.main:main",
            "ai-sre-cli=src.cli:main",
        ],
    },
)
