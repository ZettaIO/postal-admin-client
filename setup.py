from setuptools import setup

setup(
    name='postal-admin-client',
    version='0.1.1',
    url="https://github.com/ZettaIO/postal-admin-client",
    description="Python admin client for the open source mail delivery platform Postal",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Einar Forselv",
    author_email="eforselv@gmail.com",
    packages=['postal_admin_client'],
    install_requires=[
        'requests>=2.22',
        'beautifulsoup4>=4.7',
    ],
    keywords = ['posta', 'admin', 'client'],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
