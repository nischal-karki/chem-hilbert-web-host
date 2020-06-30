#!/bin/bash
cwd=$(pwd)
cd /opt/prepare
if ! $( python hash_check.py ); then
	echo running prepare.sh
	bash prepare.sh
fi
cd $cwd
