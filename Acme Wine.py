from flask import Flask, request , url_for
from flask import render_template, redirect, jsonify
from werkzeug.utils import secure_filename
import ConfigParser
import mongo_operations
import validator
from validator import Validator
from mongo_operations import save2mongo, retrieve_valid_orders, retrieve_all_orders, retrieve_one

config = ConfigParser.ConfigParser()
config.read('/home/clyde/lot18/Acme Wine/rules.cfg')
# print config.sections()
prohibited_states = config.get('ProhibitedStates', 'states').split(',')
validators = config.get('ValidationRules', 'validators').split(',')

app = Flask(__name__)



@app.route('/', methods=['GET', 'POST'])
@app.route('/orders/import', methods=['GET', 'POST'])
def import_orders():
    if request.method == 'GET':
        return render_template('import_orders.html')
    if request.method == 'POST':
        orders = request.files['file']
        v = Validator(orders)
        v.prohibited_states = prohibited_states
        v.validators = validators
        validated_records = v()
        result = save2mongo(validated_records)
        if result:
            return 'your orders have been succesfully posted'
        elif not result:
            return 'there has been a problem uploading your order'


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
    app.run(debug=True)
