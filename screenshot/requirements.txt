Prerequisites:
   Following packages to be installed 
   1- Python3 : apt-get install python3
   2- pip3  : apt-get install python3-pip
   3- Selenium : pip3 install selenium boto3
   4- Docker: apt-get install docker docker.io
   5- Docker-compose: 
       sudo curl -L "https://github.com/docker/compose/releases/download/1.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/bin/docker-compose
       sudo chmod +x /usr/bin/docker-compose

   Following permission to be given to server
   1- IAM role to be attached with S3 put and get policy

   Following Infra changes to be done:
   1- Create a s3 bucket
   2- Create IAM role with S3 permissions
   3- Port 4444 to be open in SG

How to use:
   1- Take the git clone of the repo
   2- Make following changes in screenshot.py file
        Edit the bucket_name to be used
   3- Execuet the script
        python3 screenshot.py
