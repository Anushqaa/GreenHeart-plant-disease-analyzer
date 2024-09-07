import random

def format_sensor_data(sensor_data):

    random_ranges = {
        'nitrogen': (20, 80),          # Nitrogen: 20 to 80
        'phosphorus': (10, 60),        # Phosphorus: 10 to 60
        'potassium': (10, 60),         # Potassium: 10 to 60
        'temperature': (15, 35),       # Temperature: 15°C to 35°C
        'moisture': (30, 70)           # Moisture: 30% to 70%
    }
    
    soil_fertility_options = ['Low', 'Medium', 'High']
    
    def validate_npk(value, key):
        if isinstance(value, (int, float)) and value >= 0:
            return value
        return random.randint(*random_ranges[key])
    
    def validate_temperature(value):
        if isinstance(value, (int, float)):
            return value
        return random.randint(*random_ranges['temperature'])
    
    def validate_soil_fertility(value):
        if isinstance(value, str) and value in soil_fertility_options:
            return value
        return random.choice(soil_fertility_options) 
    
    def validate_moisture(value):
        if isinstance(value, (int, float)) and 0 <= value <= 100:
            return value
        return random.randint(*random_ranges['moisture'])
    
    nitrogen = validate_npk(sensor_data[0], 'nitrogen')
    phosphorus = validate_npk(sensor_data[1], 'phosphorus')
    potassium = validate_npk(sensor_data[2], 'potassium')
    temperature = validate_temperature(sensor_data[3])
    soil_fertility = validate_soil_fertility(sensor_data[4])
    moisture = validate_moisture(sensor_data[5])
    
    return f"""
    Based on the following soil and environmental conditions, suggest the best crop for maximum yield:
    1. Nitrogen: {nitrogen}
    2. Phosphorus: {phosphorus}
    3. Potassium: {potassium}
    4. Temperature: {temperature}°C
    5. Soil Fertility: {soil_fertility}
    6. Moisture: {moisture}%
    """