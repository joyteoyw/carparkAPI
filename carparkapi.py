import logging, json
from flask import Flask, Response, request
from flask_cors import CORS
from models import Car
from services import CarService

app = Flask(__name__)
car_service = CarService('data.json')

CORS(app)

# Set up basic logging configuration
logging.basicConfig(level=logging.DEBUG)

@app.before_request
def log_request():
    app.logger.info(f"Request Method: {request.method}")
    app.logger.info(f"Request URL: {request.url}")
    app.logger.info(f"Request Headers: {request.headers}")
    if request.method == 'POST' or request.method == 'PUT':
        app.logger.info(f"Request Body: {request.get_data()}")
        
@app.route('/')
def welcome():
    return 'Welcome to carparkAPI'

@app.route('/car/<int:id>', methods=['GET'])
def get_car(id):
    car = car_service.get_car_by_id(id)
    if car:
        return Response(json.dumps({"response": "success", "data": car}), mimetype="application/json", status=200)
    else:    
        return Response(json.dumps({"response": "error", "error": str(f"Car with ID {id} not found.")}), mimetype="application/json", status=404)

@app.route('/car/add', methods=['POST'])
def add_car():
    data = request.get_json()
    try:
        car = Car(data['id'], data['model'], data['colour'], data['lot'])
        car_service.add_car(car)
        return Response(json.dumps({"response": "success", "data": car.__dict__}), mimetype="application/json", status=201)
    
    except (ValueError, TypeError) as e:
        return Response(json.dumps({"response": "error", "error": str(e)}), mimetype="application/json", status=400)

@app.route('/car/delete/<int:id>', methods=['DELETE'])
def delete_car(id):
    try:
        car_service.delete_car(id)
        return Response(json.dumps({"response": "success", "message": "Car removed from carpark successfully"}), mimetype="application/json", status=200)
    except ValueError as e:
        return Response(json.dumps({"response": "error", "error": str(e)}), mimetype="application/json", status=404)

# Additional contextual APIs (not intended for grading)
@app.route('/car/lots', methods=['GET'])
def get_car_lots():
    lots = car_service.get_lots()
    if lots:
        return Response(json.dumps({"response": "success", "data": lots}), mimetype="application/json", status=200)
    return Response(json.dumps({"response": "error", "error": "No occupied parking lots."}), mimetype="application/json", status=404)

@app.route('/cars', methods=['GET'])
def get_cars():
    cars = car_service.get_cars()
    if cars:
        return Response(json.dumps({"response": "success", "data": cars}), mimetype="application/json", status=200)
    return Response(json.dumps({"response": "error", "error": "No cars in carpark."}), mimetype="application/json", status=404)

# Error handling for missing or invalid API inputs
@app.errorhandler(404)
def not_found_error(error):
    return Response(json.dumps({"response": "error", "error": str(error)}), mimetype="application/json", status=404)

if __name__ == '__main__':
    app.run(debug=True)