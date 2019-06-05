from setuptools import setup, find_namespace_packages

setup(
    name='postal-admin-client',
    version='0.1',
    url="https://github.com/ZettaIO/postal-admin-client",
    author="Einar Forselv",
    author_email="eforselv@gmail.com",
    packages=find_namespace_packages(include=['postal_admin_client']),
    install_requires=[
        'requests>=2.22',
        'beautifulsoup4>=4.7',
    ],
)
