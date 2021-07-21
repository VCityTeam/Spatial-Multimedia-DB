A small utility that strips a CityGML 2.0 (XML)file from its 
appearences and generic attributes and serializes the result
back into a new CityGML (XML) file.

## Installation
```bash
$ virtualenv -p python3 venv
$ . venv/bin/activate
(venv)$ pip install -r requirements.txt
```

## Usages
* With input files:
```bash
(venv)$ python CityGML2Stripper.py --input filename_1.gml --output output.gml
```
