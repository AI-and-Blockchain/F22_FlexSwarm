## Usage 
Mac & Linux:

1. Navigate to backend directory, 
2. Create venv, `python3.8 -m venv venv`
3. Activate venv, `source venv/bin/activate`
4. Install requirements `python(version) pip install -r requirements.txt`
5. Deactivate use `deactivate`
6. `python3.8 server.py`


Note that `torch<=1.10.0 and >=1.8.1` is required by `syft 0.6.0`. And `torch==1.10.0` installation, some newer versions of python3 might return the following errors. Recommended to initialize `venv` with `python3.7` or `python3.8`

```
pip3.10 install torch==1.10.1 torchvision==0.11.2
ERROR: Could not find a version that satisfies the requirement torch==1.10.1 (from versions: 1.11.0, 1.12.0, 1.12.1, 1.13.0)
ERROR: No matching distribution found for torch==1.10.1
```

```
ERROR: Cannot install -r requirements.txt (line 11), -r requirements.txt (line 14), -r requirements.txt (line 15), -r requirements.txt (line 8), -r requirements.txt (line 9) and numpy==1.20.3 because these package versions have conflicting dependencies.

The conflict is caused by:
    The user requested numpy==1.20.3
    albumentations 1.3.0 depends on numpy>=1.11.1
    matplotlib 3.4.3 depends on numpy>=1.16
    pandas 1.3.4 depends on numpy>=1.17.3; platform_machine != "aarch64" and platform_machine != "arm64" and python_version < "3.10"
    scikit-learn 1.1.3 depends on numpy>=1.17.3
    syft 0.6.0 depends on numpy==1.21.4

To fix this you could try to:
1. loosen the range of package versions you've specified
2. remove package versions to allow pip attempt to solve the dependency conflict
```
