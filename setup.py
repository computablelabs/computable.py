import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

test_deps = [
        "pytest==4.4.1",
        "eth-tester==0.1.0b39",
        "web3==4.9.2",
        "web3[tester]",
        ]

extras = {
        "test": test_deps,
        }

setuptools.setup(
        name="computable",
        version="1.1.0",
        author="computable.io",
        author_email="rob@computable.io",
        description="Higher Order Contracts and helpers for the Computable Protocol",
        keywords="computable, ethereum, blockchain",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/computablelabs/computable.py",
        packages=setuptools.find_packages(exclude="tests"),
        python_requires=">=3.6", # NOTE: web3 may have issues with 3.7 and above
        classifiers=[
            "Development Status :: 3 - Alpha",
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            ],
        tests_require=test_deps,
        extras_require=extras,
        package_data={
            "":["*.abi", "*.bin"],
            }
        )
