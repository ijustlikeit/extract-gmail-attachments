Extract .jpg images from Gmail emails  and save them into a folder. 

<p>
Notes: <br>
1. Uses .netrc to obfuscate the userid/password for the email account.<br>
2. The .jpg images are stored in the parameter supplied --dst folder.<br>
3. The emails once processed can be moved to 'thrash' gmail folder with the "--thrash True" parameter <br>


<p>
I'm currently using this script with crontab to scan my gmail account so as I can save of the .jpg images from my Nest camera 
alerts.  You cannot currently retrieve these "motion detected" images with other means as Google does not provide an API 
for accessing Nest cam events. So this is my workaround.
