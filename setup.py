from setuptools import setup, find_packages

setup(
    name='glamkit-blogtools',
    author='Julien Phalip',
    author_email='julien@interaction.net.au',
    version='0.5.0',
    description='Mini framework for making Django blog apps.',
    long_description=open('README.rst').read(),
    url='http://github.com/glamkit/glamkit-blogtools',
    packages=find_packages(),
    package_data={
        'blogtools': [
            'tests/templates/*.html',
            'tests/blug/templates/blug/*.html'
            'tests/blug/templates/admin/blug/*.html'
        ]
    },
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ]
)