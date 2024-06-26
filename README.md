# HalpyBOT
This is the repository for HalpyBOT, the Hull Seals IRC Chatbot Assistant.

# Description
This repository houses all the files required to build and host your own version of the Hull Seals IRC Chat Assistant, known to us as HalpyBOT. The system is how we manage cases, recite prepared instructions for Clients and Seals, and monitor our IRC network - all in one convenient bot.

This bot is in ACTIVE DEVELOPMENT.

# Installation

## Requirements
* Python 3.8-3.9
* Poetry Package Manager
* Linux systems may require libmariadbclient-dev or libmysqlclient-dev

## Usage
- To install, download the latest [release](https://github.com/HullSeals/HalpyBOT/releases) from our repository.
- Upload and extract the files to the directory or subdirectory you wish to install from.
- Acquire the Diversions and DSSA datafiles from [Our Website](https://hullse.al/hbotassets), or build them yourself with our included CLI tools.
- Create your own .env file to fit your server, following the example config file provided.
- Install mandatory requirements with Poetry (`poetry install`).
- Run the bot (`python halpybot`) from the command line using Python.

## Troubleshooting
- Upon installation, be sure to replace the information in .env to match your own details.
- Additionally, be sure to create a user account and SASL credentials for your IRC user.
- One of the most common sources of issues is your TLS settings in the bot - check these!
- If you are having issues, look through the closed bug reports.
- If no issue is similar, open a new bug report. Be sure to be detailed.
- The notification module will not load if no Amazon Web Services config data is provided.
The bot will run just fine without these, but staff notification functions will not be available.
- The Twitter module (disabled by default) requires Twitter APIv2 access. Do not enable this module without API access.

# Support
The best way to receive support is through the issue section of this repository. As every setup is different, support may be unable to help you, but in general we will try when we can.
If for some reason you are unable to do so, emailing us at [code@hullseals.space](mailto:code@hullseals.space) will also reach the same team.

If you are a member of the Hull Seals, please file a ticket [here](https://hullseals.space/support) instead.

# Roadmap
The project has now entered a preparatory state in which several more utility functions will be added, and core frameworks made future-proof, before
work on the long awaited Dispatch Board project can finally begin.

As always, bugfixes, speed, and stability updates are priorities as discovered, as well as general enhancements over time.

# Contributing
Interested in joining the Hull Seals Cyberseals? Read up on [the Welcome Board](https://github.com/HullSeals/.github).

# Authors and Acknowledgements
Project developers:

* [Rik Overveld](https://github.com/rik079)
* [David Sangrey](https://github.com/Rixxan)
* [Feliksas](https://github.com/feliksas)
* [Ned Stevenson](https://github.com/stuntphish)

Many thanks to all of our [Contributors](https://github.com/HullSeals/.github/blob/main/CONTRIBUTORS.md).

# License
This project is governed under the [GNU General Public License v3.0](LICENSE) license.

# Project Status
The bot is running v1.6.5 in production, and still under active development.
