from setuptools import setup, find_packages

setup(
    name='webnest',
    version='0.1.0',
    packages=find_packages(include=['webnest','webnest.example_project','webnest.db']),
    install_requires=['Jinja2==3.1.4','colorama==0.4.6','black==24.8.0'],
    entry_points={
        'console_scripts': [
            'webnest=webnest.example_project.cli:main',
        ],
    },
    include_package_data=True,
    author='Yahia Badr',
    author_email='yahialord4315@gmail.com',
    description='webnest (yahia web app package or framework) is a simple framework to create web application',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Black4315/webnest', 
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Environment :: Web Environment', 
    ],
    python_requires='>=3.12.3', 
)
