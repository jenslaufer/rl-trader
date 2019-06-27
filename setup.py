from setuptools import setup, find_packages, find_namespace_packages

setup(name='rltrader',
      version='0.1.0',
      author='Jens Laufer',
      author_email='jenslaufer@gmail.com',
      install_requires=['stable-baselines==2.5.1',
                        'gym==0.12.1',
                        'pandas==0.24.2',
                        'scikit-learn==0.21.1',
                        'config==0.4.2',
                        'keras==2.2.4',
                        'keras-rl==0.4.2',
                        'pymongo==3.8.0'],
      packages=find_namespace_packages(where='src'),
      package_dir={'': 'src'}
      )
