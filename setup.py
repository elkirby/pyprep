import os

from setuptools import Command, find_packages, setup


class CleanCommand(Command):
    """Custom clean command to tidy up the project root."""

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.system('rm -vrf ./build ./dist ./*.pyc ./*.tgz ./*.egg-info')


setup(name='py-prep',
      version='0.0.1',
      packages=find_packages(),
      entry_points={
          'console_scripts': [
              'pyprep = prep_parser.__main__:main'
          ]
      },
      cmdclass={
          'clean': CleanCommand,
      },
      )
