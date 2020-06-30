#!/bin/bash
cd /opt/prepare
tar -xzf dictionary.tar.gz
tar -xzf ligand.tar.gz
tar -xzf protein.tar.gz
python plot_hill.py dictionary_scores
rm -rf *.py __pycache__ *.tar.gz
if [ ! -d /app/data ]; then mkdir /app/data/; fi
mv * /app/data/