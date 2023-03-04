# PagoPro
## PAgoPro: a tool for Picking Ago from Prokaryotes and detecting its family

## Installation
- Install deltablast. Please download the blast toolkit and add the path to PATH.
The BLAST toolkit can be avaiable at https://blast.ncbi.nlm.nih.gov/doc/blast-help/downloadblastdata.html, and download the cdd_delta database at https://ftp.ncbi.nlm.nih.gov/blast/db/cdd_delta.tar.gz. Unzip the cdd_delta into db file of PagoPro.
- download and install InterProScan, and put them into bin folder of PagoPro.
The folder architecture looks like this after property configuration. Among them GCF_000203835.1.faa is our test data
```
PagoPro
├── bin
│   ├── interproscan-5.60-92.0
├── db
│   ├── cdd_delta.aux
│   ├── cdd_delta.freq
│   ├── cdd_delta.loo
│   ├── cdd_delta.obsr
│   ├── cdd_delta.pdb
│   ├── cdd_delta.phr
│   ├── cdd_delta.pin
│   ├── cdd_delta.pos
│   ├── cdd_delta.pot
│   ├── cdd_delta.psd
│   ├── cdd_delta.psi
│   ├── cdd_delta.psq
│   ├── cdd_delta.ptf
│   ├── cdd_delta.pto
│   ├── cdd_delta.rps
│   ├── cdd_delta.wcounts
│   └── piwi.fa
├── GCF_000203835.1.faa
├── PagaPro.py
``
