from setuptools import setup, find_packages

setup(
    name="investment-portfolio-allocation",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "Django>=5.2.0",
        "djangorestframework>=3.16.0",
        "numpy>=1.20.0",
        "pandas>=1.3.0",
        "scikit-learn>=1.0.0",
        "scipy>=1.7.0",
        "joblib>=1.0.0",
        "openpyxl>=3.0.0",
        "pypfopt>=1.5.0",
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="Investment Portfolio Allocation System",
    keywords="investment, portfolio, allocation, finance",
    url="https://github.com/yourusername/investment-portfolio-allocation",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Financial and Insurance Industry",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.8",
)