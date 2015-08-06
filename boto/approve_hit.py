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
    parser.add_argument('label_count_file')
    parser.add_argument('hit_id')
    parser.add_argument('--production', default=False, action='store_true')
    args = parser.parse_args()

    access_key_id, secret_key, host = mturk.get_keys_and_host(args.keys_file, args.production)

    connection = MTurkConnection(aws_access_key_id=access_key_id,
                                 aws_secret_access_key=secret_key,
                                 host=host)


    
    label_count_dict = {}
    execfile(args.label_count_file, label_count_dict)
    get_label_count = label_count_dict['get_label_count']


          
    for assignment in connection.get_assignments(args.hit_id):
        if assignment.AssignmentStatus != 'Submitted':
            continue

        label_count = get_label_count(assignment)

        if label_count == None:
            print 'label-count not found or not integer, skipping'
            continue

        if label_count < 0:
            print 'label-count below 0, skipping'
            continue

        if label_count > 100:
            print 'label-count too large, skipping'
            continue

        bonus_amount = label_count * 0.01

        print
        print 'approving label-count of %d with bonus of $%0.2f' % (label_count, bonus_amount)
        okay = raw_input('okay? ')

        if okay == '':
            connection.approve_assignment(assignment.AssignmentId, 'Thank you!')
            if label_count != 0:
                connection.grant_bonus(assignment.WorkerId, assignment.AssignmentId, Price(bonus_amount), 'For rating %d images.' % (label_count))

        else:
            print 'skipping'



if __name__ == '__main__':
    main()
