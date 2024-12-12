import time
import board
import adafruit_mpu6050
import serial

# Initialize I2C and MPU6050
i2c = board.I2C()
mpu = adafruit_mpu6050.MPU6050(i2c)

# Initialize serial connection for the Pico
pico_serial = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

# File paths
sensor_data_file = "/var/www/html/sensor_data.txt"
event_log_file = "/var/www/html/event_log.txt"

# Thresholds (Some of these are more exaggeratted to demonstrate real time data collection)
ACC_THRESHOLD = 1.5  # g
GYRO_THRESHOLD = 1.5  # degrees/second
TEMP_HIGH_THRESHOLD = 38.0
TEMP_LOW_THRESHOLD = 0

# Function to log events
def log_event(device, message):
    with open(event_log_file, "a") as log_file:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        log_file.write(f"{timestamp} - {device}: {message}\n")
        log_file.flush()  # Ensure immediate writing to the file

# Function to check thresholds
def check_thresholds(accel, gyro, temp):
    accel_g = [a / 9.8 for a in accel]  # Convert m/s^2 to g
    events = []

    if abs(accel_g[0]) > ACC_THRESHOLD:
        events.append("X-axis acceleration exceeded threshold")
    if abs(accel_g[1]) > ACC_THRESHOLD:
        events.append("Y-axis acceleration exceeded threshold")
    if abs(accel_g[2]) > ACC_THRESHOLD:
        events.append("Z-axis acceleration exceeded threshold")
    if abs(gyro[0]) > GYRO_THRESHOLD:
        events.append("X-axis gyro exceeded threshold")
    if abs(gyro[1]) > GYRO_THRESHOLD:
        events.append("Y-axis gyro exceeded threshold")
    if abs(gyro[2]) > GYRO_THRESHOLD:
        events.append("Z-axis gyro exceeded threshold")
    if temp > TEMP_HIGH_THRESHOLD:
            events.append(f"Temperature exceeded high threshold: {temp:.2f}°C")
    if temp < TEMP_LOW_THRESHOLD:
            events.append(f"Temperature dropped below low threshold: {temp:.2f}°C")
    return events

def clear_files():
    open(sensor_data_file, "w").close()  # Truncate sensor_data.txt
    open(event_log_file, "w").close()   # Truncate event_log.txt
    print("Files cleared: sensor_data.txt and event_log.txt")

# Main program and command is sent to the Pico to start grabbing data for light levels
print("Type 'run' to start the sensor monitoring program.")
clear_files()

while True:
    sensor_input = input("Enter command: ").strip().lower()
    if sensor_input == "run":
        print("Starting sensor monitoring...")
        break
    else:
        print("Invalid command. Please type 'run' to start.")

# Monitoring loop
while True:
    pico_serial.write("run\n".encode())  # Send command to Pico

    # Get light sensor data from the Pico via Serial Communication
    try:
        response = pico_serial.readline().decode('utf-8').strip()
    except Exception as e:
        response = "No data received"
        print(f"Error reading from Pico: {e}")

    # Read MPU6050 data from sensor
    acceleration = mpu.acceleration
    gyro = mpu.gyro
    temp = mpu.temperature

    # Check for threshold events
    threshold_events = check_thresholds(acceleration, gyro, temp)

    # Log events
    if threshold_events:
        for event in threshold_events:
                    log_event("MPU6050", event)

    # Log light sensor events
    if "Box Has Been Opened" in response:
        log_event("Light Sensor", "Box has been opened")

    # Write real-time sensor data to the webpage hosted locally using apache
    with open(sensor_data_file, "w") as sensor_file:
        sensor_file.write(
            f"Light Sensor Data: {response}\n"
            f"Acceleration: X: {acceleration[0]:.2f}, Y: {acceleration[1]:.2f}, Z: {acceleration[2]:.2f} m/s^2\n"
            f"Gyro: X: {gyro[0]:.2f}, Y: {gyro[1]:.2f}, Z: {gyro[2]:.2f} rad/s\n"
            f"Temperature: {temp:.2f} Degrees Celsius\n"
        )

    print("Data written to sensor_data.txt")
    # Pause before the next reading seems to be the issue with our Pico and light sensor backlog with the data but we can't figure it out
    time.sleep(5)
