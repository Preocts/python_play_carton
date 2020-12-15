import setuptools

long_description = open("README.md", "r").read()

setuptools.setup(
    name="eggmenu",  # Replace with your own username
    version="1.0.0",
    author="Preocts",
    author_email="preocts@preocts.com",
    description="Simple text menu for running commands",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Preocts/egg_menu",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
