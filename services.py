import json
from models import Car

class CarService:

    def __init__(self, dataFile):
        self.dataFile = dataFile
        self._load_data()

    def _load_data(self):
        with open(self.dataFile, 'r') as file:
            self.cars = json.load(file)

    def __save__(self, data):
        with open(self.dataFile, 'w') as file:
            json.dump(data, file, indent=4)
    
    def get_car_by_id(self, id):
        self._load_data()
        for c in self.cars:
            if c['id'] == id:
                return c
            
        return None    
        
    def add_car(self, car):
        if not car.id or not car.model or not car.colour or not car.lot:
            raise ValueError("Car must have ID, model, colour, and lot.")
        
        if type(car.id) is not int:
            raise TypeError("Car ID must be an Integer value.")
        
        if type(car.model) is not str:
            raise TypeError("Model must be a String value.")
        
        if type(car.colour) is not str:
            raise TypeError("Colour must be a String value.")
        
        if type(car.lot) is not int:
            raise TypeError("Lot must be an Integer value.")

        if self.get_car_by_id(car.id):
            raise ValueError(f"Car with ID {car.id} already exists.")
        
        lots = self.get_lots()
        if car.lot in lots.keys():
            raise ValueError(f"Lot {car.lot} is already occupied.")
        
        self.cars.append(car.__dict__)
        self.__save__(self.cars)

    def delete_car(self, id):        
        if not self.get_car_by_id(id):
            raise ValueError(f"Car with ID {id} not found.")
        
        self.cars = [c for c in self.cars if c['id'] != id]
        self.__save__(self.cars)


    def get_lots(self):
        lots = {car['lot'] : f"{car['colour']} {car['model']}" for car in self.cars}
        return lots