from setuptools import setup, find_packages

setup(
    name="IntelliPresence",
    version="1.0.0",
    description="2014 Freshman Imaging Project RIT",
    project_url="https://github.com/ajl2612/fip2013",
    author="Freshman Imaging Team",
    license="MIT",
    install_requires=['nose', 'netifaces_py3'],
    entry_points={
        "console_scripts": [
            "tantive_iv=intellipresence:main",
            "fip_run=intellipresence:main",
            "fip_test=tests:main",
        ],
    },
)
