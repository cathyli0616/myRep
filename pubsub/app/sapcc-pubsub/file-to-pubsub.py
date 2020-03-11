#!/usr/bin/env python
# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This script uses the Twitter Streaming API, via the tweepy library,
to pull in tweets and publish them to a PubSub topic.
"""

import os
import argparse
import base64
import csv
import datetime
import random
import sys
import time

from google.cloud import pubsub_v1

# Get your twitter credentials from the environment variables.
# These are set in the 'twitter-stream.json' manifest file.

#os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.environ['APPLICATION_CREDENTIALS']
#PROJECT_ID = os.environ['PROJECT_ID']
#PUBSUB_TOPIC = os.environ['PUBSUB_TOPIC']
#FILE_NAME = os.environ['FILE_NAME']
os.environ['GOOGLE_APPLICATION_CREDENTIALS']="/home/sapcc/.ssh/secret.json"
PROJECT_ID = "mygcp-test-project-001"
PUBSUB_TOPIC = "topic-ccs-billing"
FILE_NAME = "subscriber.csv"
PUBSUB_SCOPES = ['https://www.googleapis.com/auth/pubsub']
NUM_RETRIES = 3

def publish(client, data_line):
    """Publish to the given pubsub topic."""
    topic_path = client.topic_path(PROJECT_ID, PUBSUB_TOPIC)
    print("publish line: %s" % data_line)
    data = data_line.encode('utf8')
    resp = client.publish(topic_path, data=data)

    return resp

def read_file():
    client = pubsub_v1.PublisherClient()

    now = datetime.datetime.utcnow()
    ts = now.strftime("%Y-%m-%d %H:%M:%S")
    line_count = 0
    string_line = ""
    print("processing %s" % FILE_NAME)  # process the traffic data file
    with open(FILE_NAME,'r') as data_file:
        lines = csv.reader(data_file)
        for line in lines:
            line_count += 1
            try:
                msg_attributes = {'process_ts': ts}
                print("publish line number: %s" % line_count)
                pub_data = publish(client, ','.join(line))
                print(pub_data.result())
            except IOError as error:
                sys.stderr.write("---Error: %s for %s\n" % (error, line))
            except TypeError as error:
                sys.stderr.write("---Error: %s for %s\n" % (error, line))
            except NameError as error:
                sys.stderr.write("---Error: %s for %s\n" % (error, line))
            except AttributeError as error:
                sys.stderr.write("---Error: %s for %s\n" % (error, line))
            except:
                print("Unexpected error:", sys.exc_info()[0])
if __name__ == '__main__':
    print("key file: %s" % os.environ['GOOGLE_APPLICATION_CREDENTIALS'])
    print("project: %s" % PROJECT_ID)
    read_file()
