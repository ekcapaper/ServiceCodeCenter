from prefect import task, flow
import time

sample_dataspace = {
    "stove": False,
    "temperature": 0
}

# temp simulation
@task
def sample_simulation_stove():
    global sample_dataspace
    if sample_dataspace["stove"]:
        sample_dataspace["temperature"] += 1
    else:
        sample_dataspace["temperature"] -= 1
    print("temperature")
    print(sample_dataspace["temperature"])

# check
@task
def check_temperature():
    global sample_dataspace
    return sample_dataspace["temperature"]

# control
@task
def control_heater(temp):
    global sample_dataspace
    if temp > 100:
        print("stove off")
        sample_dataspace["stove"] = False
    elif temp < 0:
        print("stove on")
        sample_dataspace["stove"] = True

@flow
def temperature_control_flow():
    while True:
        temp = check_temperature()
        control_heater(temp)

        # temp code
        sample_simulation_stove()

        time.sleep(1)
        

if __name__ == "__main__":
    temperature_control_flow()
