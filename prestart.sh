#!/bin/bash
cwd=$(pwd)
cd /opt/prepare
if ! $( python hash_check.py ); then
	bash prepare.sh &
fi
