## About this fork
Instead of exporting from Zotero, then importing to Abstrackr-web, then doing the screening, then exporting again and importing back into Zotero... this fork aims to use the Abstrackr machine-learning algorithm to sort existing Zotero libraries. The web interface of abstrackr is not used. Instead, an alternative javascript client to the Zotero is provided for efficient user interaction for screening abstracts.

## Requirements
A server with MySQL or derivative (eg. MariaDB)
Python 2.7 for the Abstrackr sorting algorithm
Pyzotero for syncing of Zotero libraries

## Install instructions
git clone this repo 
create conda environment with python 2.7, then  conda activate this environment
in this environment run pip install -r requirements.txt

WIP
