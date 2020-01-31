from setuptools import setup

with open("README.md","r") as fh:
      long_description=fh.read()

setup(name='regionconnect',
      version='0.1',
      description='IIT Human Brain Atlas regionconnect tool',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/SheridanQ/regionconnect.git',
      author='Xiaoxiao Qi',
      author_email='xqi10@hawk.iit.edu',
      license='MIT',
      packages=['regionconnect'],
      install_requires=[
      'numpy',
      'nibabel'],
      classifiers=['Development Status :: 3 - Alpha', 
                  'Intended Audience :: Developers',
                  'Topic :: Software Development :: Build Tools'],
      package_data={'atlas':['LICENSE','README.md']},
      entry_points={'console_scripts':['regionconnect=regionconnect:regionconnect']})
