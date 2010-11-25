try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

from repoman.__version__ import version

setup(
    name='repoman',
    version=version,
    description='RESTful virtual machine image manager',
    author='Matthew Vliet',
    author_email='mvliet@uvic.ca',
    url='https://github.com/hep-gc/repoman',
    license="GPLv3 or Apache v2",
    install_requires=[
        "Pylons>=1.0",
        "SQLAlchemy>=0.5",
        "markupsafe",
        'uuid',
        'pysqlite'
    ],
    setup_requires=["PasteScript>=1.6.3"],
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    test_suite='nose.collector',
    package_data={'repoman': ['i18n/*/LC_MESSAGES/*.mo']},
    #message_extractors={'repoman': [
    #        ('**.py', 'python', None),
    #        ('templates/**.mako', 'mako', {'input_encoding': 'utf-8'}),
    #        ('public/**', 'ignore', None)]},
    zip_safe=False,
    paster_plugins=['PasteScript', 'Pylons'],
    entry_points="""
    [paste.app_factory]
    main = repoman.config.middleware:make_app

    [paste.app_install]
    main = pylons.util:PylonsInstaller

    [paste.paster_command]
    make-wsgi-config = repoman.commands.wsgi_config:WSGIConfigCommand
    """,
)

