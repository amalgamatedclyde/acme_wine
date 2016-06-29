__author__ = 'clyde'

import csv
import re
import datetime
import state_codes
from bson import objectid
# state codes is a dictionary of state names and their 2 letter abbreviations

class ValidationError(Exception):

    def __init__(self, value):
        self.value = value


class Validator(object):
    """Validator class is instantiated with an orders file object as the
        argument passed to __init__. When the instance is called it
        iteratively validates each order and returns a list of validated orders.
        The validators and prohibited states attributes are set from a config file,
        rules.cfg, after instantiating the object
        """
    validators = []
    prohibited_states =[]

    def __init__(self, csvfile):
        self.csvfile = csvfile
        reader = csv.reader(self.csvfile, delimiter='|')
        self.headers = reader.__next__()
        self.orders = (row for row in reader)
        self.prev_record = []


    def __call__(self, *args, **kwargs):
        self.validated_records = []
        while True:
            try:
                self.__validate(dict(zip(self.headers, self.orders.__next__())))
            except StopIteration:
                return self.validated_records


    def __validate(self, record):
        """each validation test runs independently and updates
           the test results list"""
        self.test_results = [True]
        self.errors = []
        if [record.get('state'), record.get('zipcode')] == self.prev_record:
            record['valid'] = True
            self.validated_records.append(record)
            return
        else:
            #check if validator in config file. check key presence for unittest

            if 'state' in self.validators and record.get('state'):
                self.test_state(record)
            if 'zipcode' in self.validators and record.get('zipcode'):
                self.validate_zipcode(record)
            if 'age' in self.validators and record.get('birthday'):
                self.validate_age(record)
            if 'email' in self.validators and record.get('email'):
                self.validate_email(record)
            if 'ny_nets' in self.validators and record.get('state'):
                self.no_ny_nets(record)

        if all(self.test_results):
            try:
                self.prev_record = [record['state'], record['zipcode']]

            except KeyError:
                pass

            finally:
                record['valid'] = True
                record['_id'] = str(objectid.ObjectId())
        else:
            record['valid'] = False
            # record['_id'] = str(objectid.ObjectId())

        record['errors'] = self.errors
        # print 'error', self.errors
        self.validated_records.append(record)
        return


    ###################  VALIDATORS  #####################

    def test_state(self, record):
        #test prohibited states
        if state_codes.states[record['state']] in self.prohibited_states:
            self.errors.append({"rule": "ZipcodeFormat", "message": "We don't ship to %s"%state_codes.states[record['state']]})
            self.test_results.append(False)


    def validate_zipcode(self, record):
        #validate zipcode
        try:
            parsed_zipcode = re.match('(\d{5})([- ])?(\d{4})?', record['zipcode'])
        except AttributeError:
            self.errors.append({"rule": "AllowedStates", "message": "Zipcode doesn't match zip + 4 format"})
            self.test_results.append(False)
        if not parsed_zipcode:
            self.errors.append({"rule": "AllowedStates", "message": "Zipcode doesn't match zip + 4 format"})
            self.test_results.append(False)
        elif parsed_zipcode:
            if sum([int(char) for char in parsed_zipcode.groups()[0]]) > 20:
                # print 'zip', parsed_zipcode[0]
                self.errors.append({"rule": "ZipCodeSum", "message": "Your zipcode sum is too large"})
                self.test_results.append(False)

    def validate_age(self, record):
        #validate age
        birthday = datetime.datetime.strptime(record['birthday'], '%b %d, %Y')
        age = (datetime.datetime.now() - birthday).days/365.25
        if age < 21:
            self.errors.append({"rule": "Age", "message": "You must be at least 21 years old to place an order"})
            self.test_results.append(False)

    def validate_email(self, record):
        #validate email
        if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", record['email']):
            self.errors.append({"rule": "email", "message": "You must provide a valid email address"})
            self.test_results.append(False)

    def no_ny_nets(self, record):
        #NY users can't orderfrom .net address
        if record['state'] == 'NY' and record['email'].endswith('.net'.lower()):
            self.errors.append({"rule": "email", "message": "NY customers cannot order from a .net email address"})
            self.test_results.append(False)






