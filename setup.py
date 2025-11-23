#!/usr/bin/env python3
"""
CareConnect Setup Script
"""

from setuptools import setup, find_packages

setup(
    name="careconnect",
    version="1.0.0",
    description="AI Guardian for the Elderly",
    author="CareConnect Team",
    author_email="support@careconnect.health",
    packages=find_packages(),
    install_requires=[
        "fastapi==0.104.1",
        "uvicorn==0.24.0",
        "opencv-python==4.8.1.78",
        "scikit-learn==1.3.2",
        "tensorflow==2.15.0",
        "numpy==1.24.3",
        "pydantic==2.5.0",
        "sqlalchemy==2.0.23",
        "psycopg2==2.9.9",
        "websockets==12.0",
        "twilio==8.11.0",
        "python-jose==3.3.0",
        "passlib==1.7.4",
        "python-multipart==0.0.6",
        "aiofiles==23.2.1",
        "librosa==0.10.1",
        "pyttsx3==2.90"
    ],
    extras_require={
        "dev": [
            "pytest==7.4.3",
            "pytest-cov==4.1.0",
            "fastapi[testclient]==0.104.1"
        ]
    },
    entry_points={
        "console_scripts": [
            "careconnect=run:main",
        ],
    },
    python_requires=">=3.8",
)