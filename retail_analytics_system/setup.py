from setuptools import setup, find_packages

setup(
    name="retail_analytics_system",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'opencv-python',
        'mediapipe',
        'numpy',
        'ultralytics',
        'pyyaml',
        'flask'
    ],
    entry_points={
        'console_scripts': [
            'retail_analytics=src.main:main',
        ],
    },
)