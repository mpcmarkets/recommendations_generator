#!/usr/bin/env python3
"""
Setup script for ai_tools package
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "AI Tools - A comprehensive AI library for LLM providers, embeddings, vector stores, and tools"

# Read requirements
def read_requirements():
    requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(requirements_path):
        with open(requirements_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return []

setup(
    name="ai_tools",
    version="1.0.0",
    author="MPC Markets",
    author_email="dev@mpcmarkets.com",
    description="A comprehensive AI library for LLM providers, embeddings, vector stores, and tools",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/mpcmarkets/ai_tools",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
        "all": [
            "openai>=1.0.0",
            "anthropic>=0.3.0",
            "langchain>=0.1.0",
            "faiss-cpu>=1.7.0",
            "pgvector>=0.2.0",
            "transformers>=4.20.0",
            "torch>=1.12.0",
            "requests>=2.28.0",
            "beautifulsoup4>=4.11.0",
            "python-docx>=0.8.11",
            "PyPDF2>=3.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "ai-tools=ai_tools.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
