from flask import Flask, request
from flask import render_template, jsonify
from configparser import ConfigParser
import mongo_operations
import validator
from validator import Validator
from mongo_operations import retrieve_valid_orders, retrieve_all_orders, retrieve_one, save2mongo
import io



#######################################################
# Validator module is used to create a Validator object
# All validation rules are are applied by an instance of the
# validator object. see module for details.
# Mongo_operations module contains all database functions
#######################################################





config = ConfigParser()
config.read('/home/clyde/lot18/Acme Wine/rules.cfg')
# print config.sections()
prohibited_states = config.get('ProhibitedStates', 'states').split(',')
validators = config.get('ValidationRules', 'validators').split(',')

app = Flask(__name__)
app.debug = True

@app.route('/', methods=['GET', 'POST'])
@app.route('/orders/import', methods=['GET', 'POST'])
def import_orders():
    if request.method == 'GET':
        return render_template('import_orders.html')
    if request.method == 'POST' and request.files['file']:
        print('file present')
        # if not request.files['file'].filename.endswith('.csv'):
        #     return 'Please select a valid csv file'
        orders = request.files['file'].read().decode(encoding="utf-8")
        buf = io.StringIO(initial_value=orders)
        v = Validator(buf)
        v.prohibited_states = prohibited_states
        v.validators = validators
        validated_records = v()
        result = save2mongo(validated_records)
        if result:
            return 'your orders have been succesfully posted'
        elif not result:
            return 'there has been a problem uploading your order'
    else:
        return  render_template('import_orders.html')


@app.route('/orders/', methods=['GET'])
def get_orders():
    if not request.args:
        return render_template('get_orders.html')
    else:
        if request.args.get('checkbox') =='true':
            orders = retrieve_valid_orders()
            return jsonify(orders=orders)

        else:
            orders = retrieve_all_orders()
            return jsonify(orders=orders)


@app.route('/order_detail/<order_num>/', methods=['GET'])
@app.route('/order_detail/', methods=['GET'])
def get_one(order_num=None):
    if not order_num:
        return render_template('order detail.html')
    order = retrieve_one(order_num)
    if order:
        return jsonify(retrieve_one(order_num))
    else:
        return "That order number was not found"


if __name__ == '__main__':
    app.run()