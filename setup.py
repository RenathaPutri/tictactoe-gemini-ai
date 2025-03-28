from setuptools import setup


def readme():
    with open("README.md", "r") as fh:
        long_description = fh.read()
        return long_description


setup(
    name='tictactoe-gemini-ai',
    version='1',
    packages=['tictactoe-gemini-ai'],
    url='https://github.com/RenathaPutri/tictactoe-gemini-ai',
    license='MIT',
    author='Renatha Putri',
    author_email='renathaputri72@gmail.com',
    description='This package contains implementation of a command-line Tic-Tac-Toe game with Google Gemini AI integrated into it.',
    long_description=readme(),
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence"
    ],
    entry_points={
        "console_scripts": [
            "tictactoe-gemini-ai=tictactoe-gemini-ai.tictactoe:main",
        ]
    }
)
