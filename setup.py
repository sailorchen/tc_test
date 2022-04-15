from setuptools import setup, find_namespace_packages

install_requires = [
    "requests",
    "pymysql",
    "pytest",
    "PyYAML",
    "allure-pytest",
    "numpy"
]

setup(
    name='ApiTest',
    version='0.1',
    python_requires='>=3.7, <4',
    packages=find_namespace_packages(include=['ApiTest.*']),
    install_requires=install_requires
)