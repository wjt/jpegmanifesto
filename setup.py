try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'JPEG Manifesto',
    'author': 'Will Thompson',
    'url': 'https://github.com/wjt/jpegmanifesto',
    'download_url': 'https://github.com/wjt/jpegmanifesto',
    'author_email': 'will@willthompson.co.uk',
    'version': '0.1',
    'install_requires': ['pytest'],
    'packages': ['jpegmanifesto'],
    'scripts': [],
    'name': 'jpegmanifesto',
    'entry_points': {
        'console_scripts': ['jpegmanifesto=jpegmanifest.__main__:main'],
    },
    'include_package_data': True,
}

setup(**config)