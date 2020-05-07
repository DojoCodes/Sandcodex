import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

requires = ["docker>4", "celery>4", "redis>3", "flask>1", "connexion", "swagger_ui_bundle", "requests"]

tests_require = ["pytest", "pycov"]

dev_require = ["flake8", "black"]

setup(
    name="SandCodex",
    version="0.1.0",
    description="Execute code in a container-based sandbox",
    packages=["sandcodex"],
    entry_points ={ 
        'console_scripts': [ 
            'sandcodex = sandcodex.app:cli'
        ] 
    },
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    extra_requires={"test": tests_require, "dev": dev_require},
)
