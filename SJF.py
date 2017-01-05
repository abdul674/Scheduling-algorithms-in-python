import Queue

number_of_process = 0
try:
    number_of_process = input("How many processes are there : ")
except NameError:
    print "Invalid Input"

if number_of_process == 0:
    exit()

process = []

for index in range(number_of_process):
    number = index + 1

    try:
        arrival_time = input("Arrival Time of p{number} : ".format(number=number))
        burst_time = input("Burst Time of p{number} : ".format(number=number))
    except NameError:
        print "Invalid Input\n"
        index -= 1
        continue

    process.append({"name": "p{number}".format(number=number),
                    "burst_time": burst_time,
                    "arrival_time": arrival_time,
                    "start_time": -1})

print("\nProcess             Arrival Time           Burst Time")

width = 20
process.sort(key=lambda k: (k["arrival_time"]))

for p in process:
    print("   {name} {arrival_time}  {burst_time}".format(name=p["name"].ljust(width),
                                                          arrival_time=str(p["arrival_time"]).ljust(width),
                                                          burst_time=str(p["burst_time"])))

ticks = process[0]["arrival_time"]
total_waiting_time = 0.00
total_turnaround_time = 0.00
process_counter = 1
process_completed = 0

process_queue = Queue.PriorityQueue()

process_queue.put((process[0]["burst_time"], process[0]))
current_process = process_queue.get()

while process_completed < number_of_process:

    if not current_process[1]["start_time"] < 0:
        current_process = process_queue.get()

    if current_process[1]["arrival_time"] <= ticks:
        current_process[1]["start_time"] = ticks
        ticks += current_process[1]["burst_time"]
        total_waiting_time += current_process[1]["start_time"] - current_process[1]["arrival_time"]
        total_turnaround_time += ticks - current_process[1]["arrival_time"]
        process_completed += 1

    else:
        ticks += 1

    try:
        while process[process_counter]["arrival_time"] <= ticks:
            process_queue.put((process[process_counter]["burst_time"], process[process_counter]))
            process_counter += 1
    except IndexError:
        process_counter += 1

print("\nAverage Waiting Time : {Average_Waiting_Time}"
      .format(Average_Waiting_Time=(total_waiting_time/number_of_process)))

print("\nAverage Turnaround Time : {Average_Turnaround_Time}"
      .format(Average_Turnaround_Time=(total_turnaround_time/number_of_process)))
