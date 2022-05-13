fd index.rst --exec head -1 | sort | awk '{ print $2 }' | egrep -v '^$' | sed 's/^_//;s/:/`/;s/^/`/' 
