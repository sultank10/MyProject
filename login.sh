#!/bin/bash

#log into c2c train remotely as long as you have access to corporate VPN and your .ssh/config file has backdoor server i.e. matrail@10.99.99.1 for proxy jump

clear #clears the screen when this script is run

echo "Enter MIG number, (example mig1) [ENTER]:" #prompt user for input
read INPUT # sets the INPUT variable from the user's answer

MIG=`echo $INPUT` #variable is set from the user's input 

clear #clears the screen after entering the MIG number

echo ""
echo "Logging into $MIG, please wait ............" #informs user what MIG is logging into 
echo ""
export MIG #export global variable to expect script

	#Take the gobal env variable from bash script above i.e. $MIG and pass it into the expect script below
	#beginning of expect script, note -c is to say that this is an embeded expect script within a bash script

	/usr/bin/expect -c ' 
	#set password variable
	set password "wifiBART07" 

		#this is the default server timeout being set to 10 secs. This can be shortened or extended
		set timeout 5
		#hides console display from user
		log_user 0 
		#ssh into train using the global env variable exported from the bash script above
		spawn ssh $env(MIG)
		#backdoor server
                expect "matrail@10.99.99.1*:" 
		#default password for backdoor server
                send "$password\r" 
		#this is the expected console prompt after successful login
		expect {
			"* ~ $"
			timeout {set ret 42; exit } 
		}
		#clears the screen
		send "clear\r"
		#allows user to now interact with server and enter commands
		interact 
		#shows console display
		log_user 1 

exit
#end of expect script
#expect eof '
