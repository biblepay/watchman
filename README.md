# BiblePay Watchman-on-the-Wall

An all-powerful toolset for BiblePay.

[![Build Status](https://travis-ci.org/biblepaypay/Watchman.svg?branch=master)](https://travis-ci.org/biblepaypay/Watchman)

Watchman is an autonomous agent for persisting, processing and automating Biblepay V12.1 governance objects and tasks, and for expanded functions in the upcoming Biblepay V13 release (Tribulation).

Watchman is implemented as a Python application that binds to a local version 12.1 biblepayd instance on each Biblepay V12.1 Masternode.

This guide covers installing Watchman onto an existing 12.1 Masternode in Ubuntu 14.04 / 16.04.

## Installation

### 1. Install Prerequisites

Make sure Python version 2.7.x or above is installed:

    python --version

Update system packages and ensure virtualenv is installed:

    $ sudo apt-get update
    $ sudo apt-get -y install python-virtualenv

Make sure the local Biblepay daemon running is at least version 12.1 (120100)

    $ biblepay-cli getinfo | grep version

### 2. Install Watchman

Clone the Watchman repo and install Python dependencies.

    $ git clone https://github.com/biblepaypay/Watchman.git && cd Watchman
    $ virtualenv ./venv
    $ ./venv/bin/pip install -r requirements.txt

### 3. Set up Cron

Set up a crontab entry to call Watchman every minute:

    $ crontab -e

In the crontab editor, add the lines below, replacing '/home/YOURUSERNAME/Watchman' to the path where you cloned Watchman to:

    * * * * * cd /home/YOURUSERNAME/Watchman && ./venv/bin/python bin/Watchman.py >/dev/null 2>&1

### 4. Test the Configuration

Test the config by runnings all tests from the Watchman folder you cloned into

    $ ./venv/bin/py.test ./test

With all tests passing and crontab setup, Watchman will stay in sync with biblepayd and the installation is complete

## Configuration

An alternative (non-default) path to the `biblepay.conf` file can be specified in `Watchman.conf`:

    biblepay_conf=/path/to/biblepay.conf

## Troubleshooting

To view debug output, set the `WATCHMAN_DEBUG` environment variable to anything non-zero, then run the script manually:

    $ WATCHMAN_DEBUG=1 ./venv/bin/python bin/Watchman.py

## Contributing

Please follow the [BiblepayCore guidelines for contributing](https://github.com/biblepaypay/biblepay/blob/v0.12.1.x/CONTRIBUTING.md).

Specifically:

* [Contributor Workflow](https://github.com/biblepaypay/biblepay/blob/v0.12.1.x/CONTRIBUTING.md#contributor-workflow)

    To contribute a patch, the workflow is as follows:

    * Fork repository
    * Create topic branch
    * Commit patches

    In general commits should be atomic and diffs should be easy to read. For this reason do not mix any formatting fixes or code moves with actual code changes.

    Commit messages should be verbose by default, consisting of a short subject line (50 chars max), a blank line and detailed explanatory text as separate paragraph(s); unless the title alone is self-explanatory (like "Corrected typo in main.cpp") then a single title line is sufficient. Commit messages should be helpful to people reading your code in the future, so explain the reasoning for your decisions. Further explanation [here](http://chris.beams.io/posts/git-commit/).

### License

Released under the MIT license, under the same terms as BiblepayCore itself. See [LICENSE](LICENSE) for more info.
