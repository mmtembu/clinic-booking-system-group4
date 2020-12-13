#!/bin/bash

error_function(){
	echo "$1" #1>&2
	# exit 1
}

# This welcomes the user to the system and the creates the 'clinix' directory.
# If it exists then it throws an error

echo ' '

echo '     ___       __    _______    ___        ________   ________   _____ ______    _______           _________   ________         
    |\  \     |\  \ |\  ___ \  |\  \      |\   ____\ |\   __  \ |\   _ \  _   \ |\  ___ \         |\___   ___\|\   __  \        
    \ \  \    \ \  \\ \   __/| \ \  \     \ \  \___| \ \  \|\  \\ \  \\\__\ \  \\ \   __/|        \|___ \  \_|\ \  \|\  \       
     \ \  \  __\ \  \\ \  \_|/__\ \  \     \ \  \     \ \  \\\  \\ \  \\|__| \  \\ \  \_|/__           \ \  \  \ \  \\\  \      
      \ \  \|\__\_\  \\ \  \_|\ \\ \  \____ \ \  \____ \ \  \\\  \\ \  \    \ \  \\ \  \_|\ \           \ \  \  \ \  \\\  \     
       \ \____________\\ \_______\\ \_______\\ \_______\\ \_______\\ \__\    \ \__\\ \_______\           \ \__\  \ \_______\    
        \|____________| \|_______| \|_______| \|_______| \|_______| \|__|     \|__| \|_______|            \|__|   \|_______|    
     ________   ________   ________   _______           ________   ___        ___   ________    ___      ___    ___             
    |\   ____\ |\   __  \ |\   ___ \ |\  ___ \         |\   ____\ |\  \      |\  \ |\   ___  \ |\  \    |\  \  /  /|            
    \ \  \___| \ \  \|\  \\ \  \_|\ \\ \   __/|        \ \  \___| \ \  \     \ \  \\ \  \\ \  \\ \  \   \ \  \/  / /            
     \ \  \     \ \  \\\  \\ \  \ \\ \\ \  \_|/__       \ \  \     \ \  \     \ \  \\ \  \\ \  \\ \  \   \ \    / /             
      \ \  \____ \ \  \\\  \\ \  \_\\ \\ \  \_|\ \       \ \  \____ \ \  \____ \ \  \\ \  \\ \  \\ \  \   /     \/              
       \ \_______\\ \_______\\ \_______\\ \_______\       \ \_______\\ \_______\\ \__\\ \__\\ \__\\ \__\ /  /\   \              
        \|_______| \|_______| \|_______| \|_______|        \|_______| \|_______| \|__| \|__| \|__| \|__|/__/ /\ __\             
                                                                                                        |__|/ \|__|             
                                                                                                                                
                                                                                                                                '

echo ' '

if mkdir ~/.config/clinix; then
	echo "Clinix directory has been created."
else
	error_function "Cannot create a 'clinix' directory, it already exists!"
fi

#Moves the files to the relevant directories
pwd=$(pwd)
if cp -rf $(pwd)/* ~/.config/clinix/; then #change from 'cp' -> 'mv'

	echo 'Relevant files have been moved.'
	echo 'source ~/.config/clinix/clinix.sh' >> ~/.zshrc
	echo 'source ~/.config/clinix/clinix.sh' >> ~/.bashrc
	chmod +x ~/.config/clinix/clinix.sh
else
	error_function 'Unfortunately the files cannot be moved'
fi

