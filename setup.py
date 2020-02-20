from setuptools import setup, find_packages

test_deps = [
    'coverage',
    'pytest',
]


setup(name="mexm",
      version="0.1.0",
      description="Materials Ex Machina",
      url="https://github.com/eragasa/mexm-base",
      author="Eugene J. Ragasa",
      author_email="eragasa@osu.edu",
      license="MIT License",
      packages=["src/mexm", find_packages()],
      tests_require=test_deps,
      zip_safe=True)
