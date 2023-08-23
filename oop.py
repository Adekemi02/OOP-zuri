class ObstructionDetector:
    def __init__(self, speed):
        self.speed = speed

    def calculate_distance(self, point_a, point_b):
        lat1, lon1 = point_a
        lat2, lon2 = point_b

        # Calculate the distance
        distance = ((lat2 - lat1)**2 + (lon2 - lon1)**2)**0.5
        return distance

    def check_obstructions(self, distance, actual_time):
        expected_time = distance / self.speed
        time_difference = actual_time - expected_time

        if time_difference > 60:
            return True
        else:
            return False

if __name__ == "__main__":
    machine_speed = 1.5  # miles per minute
    point_a = (53.5872, -2.4138)  # Latitude and longitude of Point A
    point_b = (53.474, -2.2388)   # Latitude and longitude of Point B
    actual_time_ab = 15.2         # minutes (simulated from the TimeDuration module)

    obstruction_detector = ObstructionDetector(machine_speed)

    distance_ab = obstruction_detector.calculate_distance(point_a, point_b)
    has_obstruction = obstruction_detector.check_obstructions(distance_ab, actual_time_ab)

    if has_obstruction:
        print("Impenetrable obstructions detected between Point A and Point B.")
    else:
        print("No impenetrable obstructions between Point A and Point B.")

