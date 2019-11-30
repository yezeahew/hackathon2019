from setuptools import setup

setup(
    name='insta485',
    version='0.1.0',
    packages=['insta485'],
    include_package_data=True,
    install_requires=[
        'arrow==0.15.1',
        'bs4==0.0.1',
        'Flask==1.1.1',
        'html5validator==0.3.1',
        'pycodestyle==2.5.0',
        'pydocstyle==4.0.1',
        'pylint==2.3.1',
        'pytest==5.1.2',
        'requests==2.22.0',
        'sh==1.12.14',
    ],
)

#pdfminer