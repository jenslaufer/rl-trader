from setuptools import setup, find_packages, find_namespace_packages

setup(name='rltrader',
      version='0.1.10',
      author='Jens Laufer',
      author_email='jenslaufer@gmail.com',
      install_requires=['stable-baselines==2.6.0',
                        'scikit-learn==0.21.1',
                        'tensorflow==1.13.1',
                        'keras==2.2.4',
                        'keras-rl==0.4.2',
                        'pymongo==3.8.0',
                        'cloudpickle==1.2.1',
                        'setuptools-git==1.2'
                        ],
      packages=find_namespace_packages(where='src'),
      package_dir={'': 'src'},
      include_package_data=True
      # package_data={'rltrader': ['rltrader/*.yml']}
      # data_files=[('', ['src/rltrader/logging.yml'])]
      )
