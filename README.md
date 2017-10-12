# S3 Sync Tool
This is the python project to download all account data (structure and report) from Line API and store it on S3 storage.

## Getting Started
### Prerequisites
Firstly, you should install all package in the requirements.txt
```
pip install -r requirements.txt
```
Secondly, you should input the environment variables for S3 service and SmartDevice Database. For example:
```
export AWS_BUCKET_NAME=p4l-s3
export AWS_ACCESS_KEY_ID=AKIAJNYCYKYSCHXXXXX
export AWS_SECRET_ACCESS_KEY=hB1+3LSVdWYSI7w3QjUSaEpNlyI2cjxxxxxxxxx
export SMDB_USER=sat_read_only
export SMDB_PASSWORD=xxxxxxx
export SMDB_HOST=xxx.rds.amazonaws.com
export SMDB_DATABASE=p4l
export SLACK_API_TOKEN=xoxp-3548876161-xxxxx
export LINE_CLIENT_SECRET=123456abc
export LINE_CLIENT_ID=123456
export LINE_ACCESS_TOKEN_URL=http://localhost:443/v2/oauth/accessToken
```
### Running
```
chmod +x run.sh
#running without arguments, it will synchronize all account with 4 threads
./run.sh
#you can input the account_id and thread number by: -i and -n
./run.sh -i 3962 -n 3
```
You also check the log of the application at `/var/log/s3_sync.log` (You should check permission to write log)

### Structure
This project contains: 
* modules/line_helper: support to access Line via Line API (get all structure and report data)
* modules/s3_helper: support to upload file to S3 storage
* modules/smdb_helper: support to get data from SmartDevice DB
* modules/slack: support to notify Slack message
* modules/common: provide some utility functions
* modules/constants: store all url, prefix, path
* synchronization: the class support to sync structure and report data
* sync_thread: make the thread to sync multi threads
* main: only to get arguments and run