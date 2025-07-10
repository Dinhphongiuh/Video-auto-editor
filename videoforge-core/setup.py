from setuptools import setup, find_packages
from pathlib import Path

# Read README file with explicit UTF-8 encoding
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name="videoforge-core",
    version="0.1.0",
    description="VideoForge - Professional Video Processing Engine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="VideoForge Team",
    author_email="contact@videoforge.com",
    url="https://github.com/videoforge/videoforge-core",
    packages=find_packages(),
    install_requires=[
        "click>=8.1.7",
        "ffmpeg-python>=0.2.0",
        "opencv-python>=4.8.0",
        "tqdm>=4.66.1",
        "colorama>=0.4.6",
        "pydantic>=2.0.0",
        "fastapi>=0.104.0",
        "uvicorn>=0.24.0",
        "websockets>=12.0",
        "pillow>=10.0.0",
        "numpy>=1.24.0",
        "scipy>=1.11.0",
        "requests>=2.31.0",
        "aiofiles>=23.2.0",
        "python-multipart>=0.0.6",
        "jinja2>=3.1.2",
    ],
    extras_require={
        "ai": [
            "openai-whisper>=20231117",
            "googletrans==4.0.0-rc1",
            "scikit-learn>=1.3.0",
            "torch>=2.0.0",
            "torchvision>=0.15.0",
            "transformers>=4.35.0",
            "librosa>=0.10.0",
            "soundfile>=0.12.0",
        ],
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.6.0",
        ],
        "gpu": [
            "torch[cuda]>=2.0.0",
            "torchvision[cuda]>=0.15.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "videoforge=videoforge.cli.main:main",
            "vf=videoforge.cli.main:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Multimedia :: Video",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.9",
    include_package_data=True,
    zip_safe=False,
)
