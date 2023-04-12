# hdash

## Note:  this project is now deprecated.  Please use hdash_air instead.

Command Line Interface (CLI) for generating a bare bones HTAN Dashboard.

## Installation

To install ```hdash```, make sure you are running Python 3.6 or above:

```
python --version
```

Next, it is recommended that you create a virtual environment:

```
cd hdash
python -m venv .venv
```

To activate the virtual environment, run:

```
source .venv/bin/activate
```

You are now ready to install the package:

```
pip install -r requirements.txt
pip install -e .
```

## Set your Synapse Credentials

To generate the HTAN dashboard, you must set your Synapse credentials as
environment variables.  For example, I added the following to 
my ```.bash_profile```:

```
export SYNAPSE_USER="XXXXX"
export SYNAPSE_PASSWORD="YYYY"
```

## To run hdash

To run the tool, run:

```
hdash
```

## Developer Notes

The Makefile includes a number of useful targets for developing new code.

    make test:  runs Pytests
    make format:  runs black
    make lint:  runs Flake8
    make check:  runs all of the above

## LicenseMIT License

Copyright (c) ecerami

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
