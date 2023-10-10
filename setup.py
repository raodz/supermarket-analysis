import setuptools

setuptools.setup(
    name='supermarket_analysis',
    version='0.0.1',
    author='raodz',
    author_email='raodziem@gmail.com',
    description='Exploratory data analysis of supermarket chain\'s sales dataset',
    url='https://github.com/raodz/supermarket-analysis',
    # project_urls = {
    #     "Bug Tracker": "https://github.com/mike-huls/toolbox/issues"
    # },  # kaggle?
    license='MIT',
    packages=['supermarket_analysis'],
    install_requires=['pandas', 'numpy', 'matplotlib.pyplot', 'seaborn', 'scipy'],
)
