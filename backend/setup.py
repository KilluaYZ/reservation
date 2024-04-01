from setuptools import setup, find_packages
setup(
    name='reservation',
    version='0.1.3',
    packages=find_packages(),
    install_requires=[
        "flask",
        "flask_cors",
        "pymongo",
        "requests"
    ],
    include_package_data=True,
    zip_safe=False,
    author="Killuayz"
)