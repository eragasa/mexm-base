from setuptools import setup
from setuptools import find_packages

test_deps = [
    'coverage',
    'pytest',
]

setup(name="mexm",
      version="0.1.0",
      description="Materials Ex Machina",
      url="https://github.com/eragasa/mexm-base",
      author="Eugene J. Ragasa",
      author_email="ragasa.2@osu.edu",
      license="MIT License",
      package_dir={'':'src'},
      packages=["mexm"],
      tests_require=test_deps,
      zip_safe=True)
