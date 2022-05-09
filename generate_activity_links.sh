# Generate all the activity links
# This is useful for populating Brightspace
# Author:
#	Ilias Bilionis
# Date:
#	5/9/2022

base_link="https://predictivesciencelab.github.io/data-analytics-se"

cd lecturebook
for ((i=1; i<29; i++)); do
	lecture_dir=lecture`printf "%02d" $i`
	echo "** $lecture_dir ** "
	echo ""
	for f in $lecture_dir/{reading*,hands-on*}.ipynb
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
for f in homework/*.ipynb
do
	g=${f%.ipynb}
	url=$base_link/$g.html
	echo "+ $url"
	echo ""
done
cd ..