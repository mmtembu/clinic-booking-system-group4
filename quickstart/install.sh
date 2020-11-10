#!/bin/bash

error_function(){
	echo "$1" #1>&2
	# exit 1
}

# This welcomes the user to the system and the creates the 'clinix' directory.
# If it exists then it throws an error
echo "Welcome to Clinics"
if mkdir ~/.config/clinix; then
	echo "Clinix directory has been created."
else
	error_function "Cannot create a 'clinix' directory, it already exists!"
fi

#Moves the files to the relevant directories
if cp -f ~/Downloads/quickstart/* ~/.config/clinix/; then #change from 'cp' -> 'mv'

	echo 'Relevant files have been moved.'
	echo 'source ~/.config/clinix/clinix.sh' >> ~/.zshrc
	chmod +x ~/.config/clinix/clinix.sh
else
	error_function 'Unfortunately the files cannot be moved'
fi

