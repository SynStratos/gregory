import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='gregory',
    packages=setuptools.find_packages(),
    version='3.0.1',
    description='Python framework to manage time series structured as one-level dictionaries.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='SynStratos',
    author_email='synstratos.dev@gmail.com',
    url='https://github.com/SynStratos/gregory',
    python_requires='>=3.8, <3.11',
    include_package_data=True,
    classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
    ],
    keywords=['time series', 'ts', 'timeseries', 'temporal data'],
    install_requires=[
        'outatime>=3.0.1,<4.0.0',
        'python-dateutil',
        'statsmodels',
        'numpy ',
        'scipy'
    ]
)
