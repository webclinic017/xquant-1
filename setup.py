from setuptools import setup, find_packages


setup(
    name='xquant', 
    version='0.1.0', 
    packages=find_packages(),
    description='cross market backtesting/live-trading quant framework',
    install_requires = [],
    scripts=[],
    python_requires = '>=3',
    include_package_data=True,
    author='Liu Shengli',
    url='https://www.github.com/gseismic/xquant',
    zip_safe=False,
    author_email='liushengli203@163.com'
)
