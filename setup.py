from setuptools import setup, find_packages

setup(
    name='AutoQuant',
    version='1.0.0',
    description='Advanced Quantitative Trading Framework',
    author='AutoQuant Team',
    packages=find_packages(),
    install_requires=[
        'backtrader>=1.9.76.123',
        'vectorbt>=0.22.0',
        'pandas>=1.5.0',
        'numpy>=1.24.0',
        'scipy>=1.10.0',
        'TA-Lib>=0.4.25',
        'yfinance>=0.2.31',
        'tushare>=1.2.89',
        'akshare>=1.10.0',
        'matplotlib>=3.7.0',
        'plotly>=5.15.0',
        'scikit-learn>=1.2.0',
        'python-dotenv>=1.0.0',
        'pydantic>=2.0.0',
        'loguru>=0.7.0',
        'click>=8.0.0',
    ],
    entry_points={
        'console_scripts': [
            'autoquant=autoquant.cli:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='>=3.9',
)