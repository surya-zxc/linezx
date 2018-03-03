from setuptools import setup
setup(
  name = 'tcr',
  packages = ['tcr'], 
  version = '0.1',
  description = 'A unofficial line bot lib',
  author = 'Ahmad Suryani',
  author_email = 'zxchidden@gmail.com',
  keywords = ['unofficial', 'line-bot', 'test'], 
  classifiers = ['Programming Language :: Python','Topic :: Internet :: WWW/HTTP :: Dynamic Content','Topic :: Communications :: Chat',],
  install_requires=[
            'tcr',
            'requests',
            'rsa',
            'thrift==0.9.3'
        ],
)