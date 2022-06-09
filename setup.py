from setuptools import setup

setup(
    name="edc",
    version="0.0.1",
    py_modules=["edc"],
    install_requires=[
        "ipython",
        "requests",
        "python-dotenv",
    ],
)
