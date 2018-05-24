"""
MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH
THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import boto3
import logging
import os

def lambda_handler(event, context):
    log = logging.getLogger()
    log.setLevel(logging.INFO)

    env_kda_app_name = 'kda_application_name'
    env_firehose = 'firehose_stream_name'

    if env_kda_app_name not in os.environ:
        errorMsg = 'Environment variable ' + env_kda_app_name + ' is required'
        log.error(errorMsg)
        return errorMsg

    if env_firehose not in os.environ:
      errorMsg = 'Environment variable ' + env_firehose + ' is required'
      log.error(errorMsg)
      return errorMsg

    kdaAppName = os.environ.get(env_kda_app_name)
    firehoseName = os.environ.get(env_firehose)

    kdaClient = boto3.client('kinesisanalytics')
    response = kdaClient.describe_application(ApplicationName = kdaAppName)

    if response['ApplicationDetail']['ApplicationStatus'] == 'RUNNING':
        firehoseClient = boto3.client('firehose')
        response = firehoseClient.put_record(
          DeliveryStreamName = firehoseName,
          Record = {
            'Data': '\n'
          }
        )
        return response
    else:
        notRunning = kdaAppName + ' is not running'
        log.info(notRunning)
        return notRunning
