'''
Author: Abhishek Kumar Srivastava
Purpose: Take screenshot of url from firefox and chrome browser,uploads to S3 and retiurns S3 presigned URL.
'''
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from time import sleep
import os
import boto3
from botocore.client import Config
from datetime import datetime

bucket_name="<bucket_name>"

##Creating s3 boto client
s3_client=boto3.client(
      's3',
      region_name="us-east-1",
      config=Config(signature_version='s3v4')
      )

def upload_to_s3(filename):
     '''
     Purpose: Function to upload files to s3
     return: None
     '''
     file_name = filename
     key_name = filename
     try:
        print("======S3 Upload started for %s======" %(filename))
        s3_client.upload_file(file_name, bucket_name, key_name)
        print("S3 url: %s" %(create_presigned_url(filename, expiration=1800)))
        print("======S3 upload completed for %s======\n \n" %(filename))
     except Exception as e:
        print(e)

def create_presigned_url(object_name, expiration=1800):
    '''
    Purpose: Function to generate presigned s3 urls whcih gets expired after 15 minutes
    return: String
    '''
    try:
        response = s3_client.generate_presigned_url('get_object',Params={'Bucket': bucket_name,'Key': object_name},ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None
    return response

def main():
     '''
     Purpose: Take screenshot of website links and upload it to s3 and gets back the presined URL
     return: None
     '''
     now = datetime.now()
     current_time = now.strftime("%d_%m_%Y_%H_%M")
     url=input("Enter the url: ")
     try:
        print("======Starting the containers for selenium firefox and chrome=======")
        os.system("docker-compose up -d")
        sleep(10)
        print("======Taking screenshot from firefox browser======")
        firefox = webdriver.Remote("http://localhost:5555/wd/hub", DesiredCapabilities.FIREFOX)
        firefox.get(url)
        sleep(1)
        firefox.get_screenshot_as_file(str(current_time)+"_firefox.png")
        firefox.quit()
        print("======Taking screenshot from chrome browser=======")
        chrome = webdriver.Remote("http://localhost:3333/wd/hub", DesiredCapabilities.CHROME)
        chrome.get(url)
        sleep(1)
        chrome.get_screenshot_as_file(str(current_time)+"_chrome.png")
        chrome.quit()
        print("======Stopping and deleting the containers======")
        os.system("docker-compose down")
        filenames=['chrome.png','firefox.png']
        for filename in filenames:
           upload_to_s3(str(current_time)+"_"+filename)
     except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
