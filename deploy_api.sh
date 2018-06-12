#!/bin/sh



tar -czvf "db.tar.gz" "api"


scp -i /home/matthieu/Documents/mbkey.pem "db.tar.gz" "ec2-user@13.250.249.221:~/crawlers"



ssh -i /home/matthieu/Documents/mbkey.pem "ec2-user@13.250.249.221" << EOF 
  cd crawlers
  if [ -d "db" ]; then
	# Control will enter here if $DIRECTORY exists.
	rm -R db
  fi
  tar -xzvf "db.tar.gz"
  rm "db.tar.gz"
EOF