from setuptools import setup, find_packages

setup(
    name="IntelliPrecense",
    version="1.0.0",
    description="2014 Freshman Imaging Project RIT",
    project_url="https://github.com/ajl2612/fip2013",
    author="Freshman Imaging Team",
    license="MIT",
    install_requires=['nose'],
    entry_points={
        "console_scripts": [
            "tantive_iv=IntelliPresence:main",
        ],
    },
)
