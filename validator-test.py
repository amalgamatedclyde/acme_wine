__author__ = 'clyde'

import unittest2
from validator import Validator
import validator
import ConfigParser
import datetime

config = ConfigParser.ConfigParser()
l = config.read('rules.cfg')
prohibited_states = config.get('ProhibitedStates', 'states').split(',')
# validators = config.get('ValidationRules', 'validators').split(',')

# 'New Jersey', 'Connecticut', 'Pennsylvania', 'Massachusetts', 'Illinois', 'Idaho', 'Oregon'
# validators = ['state', 'zipcode', 'age', 'email', 'ny_nets']

class ValidatorTestCase(unittest2.TestCase):

    def test_state(self):
        csvfile = open('/home/clyde/lot18/state_test.csv')
        v = Validator(csvfile)
        v.validators = ['state']
        v.prohibited_states = prohibited_states
        r = v()
        csvfile.close()
        self.assertEqual([False,False,False,False,False,False,False,True,True,True,True,True,True], [i['valid'] for i in r])

    def test_zipcode(self):
        csvfile = open('/home/clyde/lot18/zipcode_test.csv')
        v = Validator(csvfile)
        v.validators = ['zipcode']
        v.prohibited_states = prohibited_states
        r = v()
        csvfile.close()
        self.assertEqual([True,True,True,False,False,False], [i['valid'] for i in r])

    def test_age(self):
        csvfile = open('/home/clyde/lot18/age_test.csv')
        v = Validator(csvfile)
        v.validators = ['age']
        v.prohibited_states = prohibited_states
        r = v()
        csvfile.close()
        self.assertEqual([True,False,True], [i['valid'] for i in r])

    def test_email(self):
        csvfile = open('/home/clyde/lot18/email_test.csv')
        v = Validator(csvfile)
        v.validators = ['email']
        v.prohibited_states = prohibited_states
        r = v()
        csvfile.close()
        self.assertEqual([False,True,False], [i['valid'] for i in r])

    def test_net(self):
        csvfile = open('/home/clyde/lot18/net_test.csv')
        v = Validator(csvfile)
        v.validators = ['ny_net']
        v.prohibited_states = prohibited_states
        r = v()
        csvfile.close()
        self.assertTrue([i['valid'] for i in r][0])


if __name__ == '__main__':
    unittest2.main()
