from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='image-processor',
    version='1.0.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A powerful image processing toolkit for format conversion and manipulation',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/image-processor',
    packages=find_packages(),
    install_requires=[
        'Pillow>=8.0.0',
    ],
    entry_points={
        'console_scripts': [
            'image-processor=image_processor.cli:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Multimedia :: Graphics',
    ],
    python_requires='>=3.6',
)
