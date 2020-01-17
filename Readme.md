## Installation

#### System Requirements
* MySQL or compatible database
* Python 2.7 with pip
* recommended: virtualenv or conda environment

#### Steps
1. `mkdir abstrackr-web && cd abstrackr-web`
2. `git clone https://github.com/bwallace/abstrackr .`
3. `pip install .`
4. `pip install numpy pygooglechart git+https://github.com/hpiwowar/eutils "biopython==1.57"`
5. `cp sample.ini run.ini`
6. `nano run.ini`
7. things to edit:
    * both mysql connection lines
    * new random cookie secret
    * uncomment `set debug = false`
8. `save (^o) and exit (^x)`
9. `paster setup-app run.ini`
10. `paster serve run.ini`
11. Consider a supervisor daemon to keep the site running.
