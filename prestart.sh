#! /usr/bin/env sh

echo "Running inside /app/prestart.sh, you could add migrations to this file, e.g.:"

echo "
#! /usr/bin/env bash

# Let the DB start
sleep 10;
# Run migrations
alembic upgrade head
"
job () {
	cwd=$(pwd)
	cd /app/data
	mv /opt/prepare/* /app/data
	tar -xzf dictionary.tar.gz && rm -rf dictionary.tar.gz
	python plot_hill.py dictionary_scores &
	tar -xzf ligand.tar.gz && rm -rf ligand.tar.gz
	tar -xzf protein.tar.gz && rm -rf protein.tar.gz
	wait
	rm -rf *.py *cache*
	for i in /opt/prepare/hilbert_bar/hilbert/*/*
	do
		pngquant --skip-if-larger $i
		echo ${i%.*}
		mv "${i%.*}"-fs8.png $i
	done
	cd $cwd
}
job &
