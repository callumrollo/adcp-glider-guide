#!/bin/bash

# if directory not passed, use working directory
_dir="${1:-${PWD}}"

# Die if given a bad directory path
[ ! -d "$_dir" ] && { echo "Error: Directory $_dir not found."; exit 2; }

for i in $_dir/pcp*a.dat; do
	num=${i: -9:4}
	tele_fn="adcp_tele$num.txt"
	> $tele_fn	
	echo "junk,date,time,cell_no,cell_dist,v1,v2,v3,amp1,amp2,amp3,corr1,corr2,corr3" >> $tele_fn
	grep PNORC1 $i | awk '{print substr($0, 1, length($0)-4)}' >> $tele_fn
done
