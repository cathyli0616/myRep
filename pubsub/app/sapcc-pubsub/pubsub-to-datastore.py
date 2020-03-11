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
"""This script grabs tweets from a PubSub topic, and stores them in BiqQuery
using the BigQuery Streaming API.
"""

import base64
import json
import os
import time

from google.cloud import pubsub_v1
from google.cloud import datastore
from datetime import datetime, date, time

# Get the project ID and pubsub topic from the environment variables set in
# the 'bigquery-controller.yaml' manifest.
#GOOGLE_APPLICATION_CREDENTIALS = os.environ['APPLICATION_CREDENTIALS']
#PROJECT_ID = os.environ['PROJECT_ID']
#PUBSUB_TOPIC = os.environ['PUBSUB_TOPIC']
#SUBSCRIPTION_NAME = os.environ['SUBSCRIPTION_NAME']
os.environ['GOOGLE_APPLICATION_CREDENTIALS']="/home/sapcc/.ssh/secret.json"
PROJECT_ID = "mygcp-test-project-001"
PUBSUB_TOPIC = "topic-ccs-billing"
SUBSCRIPTION_NAME = "async-pubsub-to-datastore"

NUM_MAX = 5

def datastore_client(project_id):
    return datastore.Client(project_id)
# [END datastore_build_service]

# [START datastore_add_entity]
def add_subscriber(client, message):
    key = client.key('subscriber')
    entity = datastore.Entity(key)

    s_message = message.data.decode("utf-8")
    data_list = [x.strip() for x in s_message.split(',')]
    print('creation time %s', data_list)

    entity.update({
        'creation_ts': datetime.strptime(data_list[0], '%Y-%m-%d %H:%M:%S'),
        'effective_ts': datetime.strptime(data_list[1], '%Y-%m-%d %H:%M:%S'),
        'product_type_cd': data_list[2],
        'status_cd': data_list[3],
        'status_dt': datetime.strptime(data_list[4], '%Y-%m-%d %H:%M:%S'),
        'subscriber_num': data_list[5],
        'update_dt': datetime.utcnow()
    })
    client.put(entity)

    print('add subscriber %s', entity['subscriber_num'])

    return entity.key
# [END datastore_add_entity]


def create_subs_client():
    """Create a new subscriber client"""
    subscriber = pubsub_v1.SubscriberClient()
    return subscriber

def get_subscription_path(subscriber, subscription_name):
    """Get subscription path"""
    subscription_path = subscriber.subscription_path(
        PROJECT_ID, subscription_name)

    print('Subscription path: %s' % subscription_path)
    # [END pubsub_create_pull_subscription]
    return subscription_path

def async_pull_messages(subscriber, subscription_path):
    """Receives messages from a pull subscription, backend run async"""
    client = datastore_client(PROJECT_ID)
    def callback(message):
        #print('Received message: {}'.format(message))
        add_subscriber(client, message)
        message.ack()

    future = subscriber.subscribe(subscription_path, callback=callback)

    # Blocks the thread while messages are coming in through the stream. Any
    # exceptions that crop up on the thread will be set on the future.
    try:
        # When timeout is unspecified, the result method waits indefinitely.
        future.result(timeout=30)
    except Exception as e:
        print(
            'Listening for messages on {} threw an Exception: {}.'.format(
                subscription_path, e))
    # [END pubsub_subscriber_error_listener]

if __name__ == '__main__':
    try:
        # try to create subscriber
        subscriber = create_subs_client()
    except:
        print("Unexpected error:", sys.exc_info()[0])

    try:
        # check if subscription exists first
        subscription_path = get_subscription_path(subscriber,SUBSCRIPTION_NAME)
    except:
        print("Unexpected error:", sys.exc_info()[0])

    async_pull_messages(subscriber, subscription_path)

    #write_to_datastore(pubsub, sub_name, bigquery)
