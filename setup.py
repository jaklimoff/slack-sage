from setuptools import find_packages, setup

setup(
    name="slack_sage",
    version="0.1.0",
    author="Evgenii Klimov",
    author_email="jaklimoff@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    url="http://slack-sage.com",
    license='BSD',
    description="Slack bot built with the help of mighty python 3 and asyncio",
    long_description=open("README.md").read(),
    install_requires=[
        'aiohttp'
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
)
