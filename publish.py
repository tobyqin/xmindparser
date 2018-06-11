"""
Use this script to upload a pypi package, require below package:

    pip install setuptools -U
    pip install wheel -U
    pip install twine -U

"""
import os

egg = 'dist'

if os.path.exists(egg):
    for f in os.listdir(egg):
        os.remove(os.path.join(egg, f))

os.system('python setup.py sdist bdist_wheel')
os.system('twine upload dist/*')
