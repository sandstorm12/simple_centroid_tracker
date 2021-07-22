from setuptools import setup


def read_requirements(path="./requirements.txt"):
    with open(path) as file:
        install_requires = file.readlines()

    return install_requires


setup(
    name="centroid_tracker",
    version="0.1.5",
    author="Hamid Mohammadi",
    author_email="sandstormeatwo@gmail.com",
    description=("Simple centroid tracker."),
    packages=[
        "centroid_tracker"
    ],
    install_requires=read_requirements()
)
