from flask import Flask, request , url_for
from flask import render_template, redirect, jsonify
from werkzeug.utils import secure_filename
import ConfigParser
import mongo_operations
import validator
from validator import Validator
from mongo_operations import save2mongo, retrieve_valid_orders

ALLOWED_EXTENSIONS = ['txt', 'csv']
config = ConfigParser.ConfigParser()
l = config.read('rules.cfg')
prohibited_states = config.get('ProhibitedStates', 'states').split(',')
validators = config.get('ValidationRules', 'validators').split(',')

app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS



@app.route('/', methods=['GET', 'POST'])
@app.route('/orders/import', methods=['GET', 'POST'])
def import_orders():
    if request.method == 'GET':
        return 'would you like to submit an order?'
    if request.method == 'POST':
        if 'file_' not in request.files:
            return redirect(request.url)
        file_ = request.files['file_']
        if file_.filename == '':
            return redirect(request.url)
        if file_ and allowed_file(file_.filename):
            filename = secure_filename(file_.filename)
            v = Validator(filename)
            validated_records = v()
            result = save2mongo(validated_records)
            if result:
                return 'your orders has been succesfully posted'
    return render_template('import_orders.html')


@app.route('/orders/<order_id>', methods=['GET'])
def get_orders():
    if request.args.get('valid'):
        orders = retrieve_valid_orders()
        return jsonify(orders=orders)




if __name__ == '__main__':
    app.run(debug=True)
