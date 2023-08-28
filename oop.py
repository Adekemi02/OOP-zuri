import random


class ObstructionDetector:
    def __init__(self, machine_speed, pointA, pointB):
        self.__obstruction_time_limit = 60  # time limit in minutes for obstruction to be considered impenetrable
        self.pointA = pointA
        self.pointB = pointB
        self.machine_speed = machine_speed
        self.distance = self.calculate_distance()

    @classmethod
    def check_speed(self, speed):
        if speed < 0:
            raise ValueError("Speed cannot be negative.")
        
        if type(speed) is not int and type(speed) is not float:
            raise TypeError("Speed must be a number.")
        
        return speed

    def calculate_distance(self):
        lat1, lon1 = self.pointA
        lat2, lon2 = self.pointB

        if type(self.pointA) is not tuple or type(self.pointB) is not tuple:
            raise TypeError("Points must be tuples.")

        # Calculate the distance
        distance = ((lat2 - lat1)**2 + (lon2 - lon1)**2)**0.5

        return distance

    def check_obstructions(self, speed):
        speed = self.check_speed(speed)

        if not speed:
            raise ValueError("Speed must be supplied.")

        expected_time = self.distance / speed
        simulated_time = self.simulate_time()

        if simulated_time > expected_time + self.__obstruction_time_limit:
            return f"Obstruction detected: Impenetrable obstruction detected between Point A and Point B. Expected time: {expected_time} minutes. Actual time: {simulated_time} minutes."
        
        if simulated_time > expected_time:
            return f"Obstruction detected: Expected time: {expected_time} minutes. Actual time: {simulated_time} minutes."
        
        return f"No obstructions detected. Expected time: {expected_time} minutes. Actual time: {simulated_time} minutes."
    

    def simulate_time(self):
        simulated_time_taken = random.randint(0, 100) * ((self.distance / self.machine_speed) + 180)
        return simulated_time_taken

if __name__ == "__main__":
    machine_speed = 1.5  # miles per minute
    pointA = (53.5872, -2.4138)
    pointB = (53.474, -2.2388)
    
    obstruction_detector = ObstructionDetector(machine_speed, pointA, pointB)

    has_obstruction = obstruction_detector.check_obstructions(obstruction_detector.machine_speed)
    
    print(has_obstruction)
