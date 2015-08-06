import argparse
import datetime
import os
from boto.mturk.connection import MTurkConnection
from boto.mturk.question import ExternalQuestion
from boto.mturk.price import Price
import mturk


def main():
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('keys_file')
    parser.add_argument('--production', default=False, action='store_true')
    args = parser.parse_args()

    access_key_id, secret_key, host = mturk.get_keys_and_host(args.keys_file, args.production)



    connection = MTurkConnection(aws_access_key_id=access_key_id,
                                 aws_secret_access_key=secret_key,
                                 host=host)



    question = ExternalQuestion(
        external_url='https://mapmill-pilot.ccs.neu.edu:3000/',    # URL to serve HIT
        frame_height=800                                           # height of frame
        )

    reward=Price(
        amount=0.10                                                # reward for HIT completion
        )

    create_hit_result = connection.create_hit(
        title='Disaster Area Map Image Labeling',
        description='Label and categorize aerial images of disaster areas',
        keywords=['image', 'label', 'labeling', 'categorize', 'map'],
        max_assignments=10,
        lifetime=datetime.timedelta(days=5),                       # time HIT is available
        duration=datetime.timedelta(minutes=30),                   # time worker has to complete HIT once accepted
        question=question,
        reward=reward,
        response_groups=('Minimal', 'HITDetail')
        )



if __name__ == '__main__':
    main()
