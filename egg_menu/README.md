# Egg Menu

## Requirements:

- Python >= 3.8
- pip

---

## Installation:

It is highly recommended to use a [venv](https://docs.python.org/3/library/venv.html) using pip to install this module. [venv](https://docs.python.org/3/library/venv.html) allows you to control dependencies, versions, and allows library installation without requiring system install permissions.

Step 1) Create a workspace to develop (skip to 2 if already created):

Bash
```bash
mkdir <myworkpace>
cd <myworkspace>
python -m venv <your-env>
```

Windows
```dos
mkdir <myworkpace>
cd <myworkspace>
python -m venv <your-env>
```

Step 2) Activate venv

Bash
```bash
source ./<your-env>/bin/active
```

Windows
```dos
source .\<your-env>\Scripts\activate.bat
```

Step 3) Clone the repo to your local workspace:

```bash
git clone https://github.com/Preocts/egg_menu.git
```

Step 4) Ensure `setuptools`, `wheel`, and `pip` are latest versions and install the library to your venv:

```bash
pip install --upgrade pip setuptools wheel
pip install egg_menu
```

Step 5) *Optional* Cleanup

Bash
```bash
rm -rf egg_menu
```

Windows
```dos
rmdir /S /Q egg_menu
```

---

## Usage

To be completed