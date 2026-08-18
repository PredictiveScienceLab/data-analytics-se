#!/usr/bin/env bash
set -euo pipefail
shopt -s nullglob

# Generate all the activity links
# This is useful for populating Brightspace
# Author:
#	Ilias Bilionis
# Date:
#	5/9/2022

base_link="https://predictivesciencelab.github.io/data-analytics-se"

cd lecturebook
for ((i=1; i<29; i++)); do
	lecture_dir="lecture$(printf '%02d' "$i")"
	echo "** $lecture_dir ** "
	echo ""
	for f in "$lecture_dir"/reading*.ipynb
	do
		g=${f%.ipynb}
		url=$base_link/$g.html
		echo "+ $url"
		echo ""
	done
	for f in "$lecture_dir"/hands-on*.ipynb
	do
		g=${f%.ipynb}
		url=$base_link/$g.html
		echo "+ $url"
		echo ""
	done
	echo ""
done
cd ..

echo "** Homework **"
cd lecturebook

# Only the ten active Fall 2026 assignments belong in Brightspace.
for ((i=1; i<=10; i++)); do
	f="homework/homework-$(printf '%02d' "$i").ipynb"
	if [[ ! -f "$f" ]]; then
		echo "Error: missing active homework notebook: $f" >&2
		exit 1
	fi
	g=${f%.ipynb}
	url=$base_link/$g.html
	echo "+ $url"
	if ((i < 10)); then
		echo ""
	fi
done
cd ..
