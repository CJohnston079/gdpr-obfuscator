from setuptools import find_packages
from setuptools import setup

setup(
    name="obfuscator",
    version="0.1.0",
    author="Christopher Johnston",
    author_email="chris79gp@outlook.com",
    license="MIT",
    description="An obfuscation tool for data files in AWS S3.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/CJohnston079/gdpr-obfuscator",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    py_modules=["obfuscator", "exceptions"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=["botocore==1.34.120", "pandas==2.2.2", "Faker==25.8.0"],
)
