__author__ = 'clyde'

import state_codes
import csv
from validator import prohibited_states

class Validator(object):
    """Validator class created with an orders file object.
       When an instance is called it iteratively validates each order and returns a
       list of validated orders"""

    def __init__(self, csvfile):
        self.csvfile = csvfile
        reader = csv.reader(self.csvfile, delimiter='|')
        self.headers = reader.next()
        self.orders = (row for row in reader)
        self.prev_record = []


    def __call__(self, *args, **kwargs):
        self.validated_records = []
        self.errors =[]
        self.test_results = []
        while True:
            try:
                self.test_state(dict(zip(self.headers, self.orders.next())))
            except StopIteration:
                return self.validated_records
    def test_state(self, record):
        #test prohibited states
        # print map(str, [self, record])
        # print state_codes.states[record['state']]
        if state_codes.states[record['state']] in prohibited_states:
            self.errors.append({"rule": "ZipcodeFormat", "message": "We don't ship to %s"%record['state']})
            self.test_results.append(False)
        self.validated_records.append(record)

csvfile = open('/home/clyde/lot18/orders.csv')
v = Validator(csvfile)
r = v()
csvfile.close()
print r