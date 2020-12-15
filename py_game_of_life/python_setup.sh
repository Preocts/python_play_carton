echo Creating directory structure...
mkdir src
mkdir tests
mkdir docs
echo Done.

echo Setting up venv...
python3.8 -m venv venv
source ./venv/bin/activate
echo Done.

echo Updating pip, wheel, and setuptools...
pip install --upgrade pip wheel setuptools
echo Done.

echo Installing dev tools
pip install pylint autopep8 flake8
echo Done.

echo Happy coding.