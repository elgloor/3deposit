### Build
```
cd unpack
python3 setup.py sdist bdist_wheel
```
### Upload
```
python3 -m twine upload dist/*
```