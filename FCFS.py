
def take_integer_input(prompt, minimum_value):
    while True:
        try:
            inp = int(raw_input(prompt))
            if inp >= minimum_value:
                return inp
            else:
                print "Invalid Input value must be greater than {min_value}".format(min_value=minimum_value-1)
        except ValueError:
            print "Invalid Input Value must be a valid Integer"

number_of_process = take_integer_input("How many processes are there : ", 0)

if number_of_process == 0:
    exit()

process = []

for index in range(number_of_process):
    number = index + 1

    arrival_time = take_integer_input("Arrival Time of p{number} : ".format(number=number), 0)
    burst_time = take_integer_input("Burst Time of p{number} : ".format(number=number), 1)

    process.append({"name": "p{number}".format(number=number),
                    "burst_time": burst_time,
                    "arrival_time": arrival_time,
                    "finish_time": 0,
                    "start_time": -1,
                    "waiting_time": 0,
                    "turnaround_time": 0})

print("\nProcess             Arrival Time           Burst Time")

width = 20
process.sort(key=lambda k: (k["arrival_time"]))

for p in process:
    print("   {name} {arrival_time}  {burst_time}".format(name=p["name"].ljust(width),
                                                          arrival_time=str(p["arrival_time"]).ljust(width),
                                                          burst_time=str(p["burst_time"])))

ticks = process[0]["arrival_time"]
process_counter = 0
total_waiting_time = 0.0
total_turnaround_time = 0.0

while process_counter < number_of_process:

    if process[process_counter]["arrival_time"] <= ticks:

        process[process_counter]["start_time"] = ticks

        process[process_counter]["finish_time"] = ticks + process[process_counter]["burst_time"]
        ticks = process[process_counter]["finish_time"]

        process[process_counter]["waiting_time"] = \
            process[process_counter]["start_time"] - process[process_counter]["arrival_time"]

        process[process_counter]["turnaround_time"] = \
            process[process_counter]["finish_time"] - process[process_counter]["arrival_time"]

        total_turnaround_time += process[process_counter]["turnaround_time"]
        total_waiting_time += process[process_counter]["waiting_time"]

        process_counter += 1

    else:
        ticks += 1


print("\nAverage Waiting Time : {Average_Waiting_Time}"
      .format(Average_Waiting_Time=(total_waiting_time/number_of_process)))

print("\nAverage Turnaround Time : {Average_Turnaround_Time}"
      .format(Average_Turnaround_Time=(total_turnaround_time/number_of_process)))
