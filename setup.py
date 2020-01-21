from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()
VERSION = '0.1.28'

setup(
    name='QuickStart_Rhy',
    version=VERSION,
    description='Simplify the operation in terminal!',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords='Simplify the operation in terminal!',
    author='RhythmLian',
    author_mail='RhythmLian@outlook.com',
    url="https://github.com/Rhythmicc/QuickStart",
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    install_requires=['pyperclip', 'requests', 'psutil', 'matplotlib', 'numpy', 'urllib3', 'Crypto', 'colorama'],
    entry_points={
        'console_scripts': [
            'qs = QuickStart_Rhy.main:main'
        ]
    },
)
