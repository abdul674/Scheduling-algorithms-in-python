import Queue


def check_and_put_new_process_in_ready_queue(processes, current_time, current, processes_queue):
    try:
        while processes[current]["arrival_time"] <= current_time:
            processes_queue.put(processes[current])
            current += 1
    except IndexError:
        current += 0
    finally:
        return current, processes_queue


def check_and_return_process_from_waiting_to_auxiliary_queue(waiting, auxiliary, current_time):
    temp_arr = []

    for i in range(len(waiting_queue)):
        if waiting[i]["return_time"] <= current_time:
            auxiliary.put(waiting_queue[i])
            temp_arr.append(i)
    for i in temp_arr:
        waiting_queue.pop(i)

    return waiting, auxiliary


def take_integer_input(prompt, minimum_value):
    while True:
        try:
            inp = input(prompt)
            if inp >= minimum_value:
                return inp
            else:
                print "Invalid Input"
        except NameError:
            print "Invalid Input"

time_quanta = take_integer_input("Time Slice: ", 1)

number_of_process = take_integer_input("How many processes are there : ", 0)

if number_of_process == 0:
    exit()

process = []

for index in range(0, number_of_process):
    number = index + 1

    cpu_bursts = []
    io_bursts = []

    arrival_time = take_integer_input("Arrival Time of p{number} : ".format(number=number), 0)
    no_of_cpu_bursts = take_integer_input("How many CPU Bursts are there : ", 1)
    no_of_io_bursts = no_of_cpu_bursts - 1

    print "\n"

    for b in range(no_of_cpu_bursts):
        temp = take_integer_input("\tEnter Time for CPU Burst {number} : ".format(number=b), 1)
        cpu_bursts.append(temp)

    print "\n"

    for b in range(no_of_io_bursts):
        temp = take_integer_input("\tEnter Time for IO Burst {number} : ".format(number=b), 1)
        io_bursts.append(temp)

    process.append({"name": "p{number}".format(number=number),
                    "cpu_bursts": cpu_bursts,
                    "io_bursts": io_bursts,
                    "current_cpu_burst": 0,
                    "arrival_time": arrival_time,
                    "start_time": -1,
                    "remaining_time": 0,
                    "remaining_quanta": time_quanta,
                    "finish_time": -1,
                    "return_time": -1})
    print "\n"

print("\nProcess             Arrival Time           Burst Time")

width = 20
process.sort(key=lambda k: k["arrival_time"])

for p in process:
    print("   {name} {arrival_time}  {burst_time}".format(name=p["name"].ljust(width),
                                                          arrival_time=str(p["arrival_time"]).ljust(width),
                                                          burst_time=str(sum(p["cpu_bursts"]))))

ticks = process[0]["arrival_time"]
total_waiting_time = 0.00
total_turnaround_time = 0.00

process_queue = Queue.Queue()
auxiliary_queue = Queue.Queue()
waiting_queue = []

process_completed = 0
process_counter = 1

process_queue.put(process[0])

while process_completed < number_of_process:

    if auxiliary_queue.empty():
        if process_queue.empty():
            ticks += 1
            waiting_queue, auxiliary_queue = check_and_return_process_from_waiting_to_auxiliary_queue(waiting_queue,
                                                                                                      auxiliary_queue,
                                                                                                      ticks)

            current_process, process_queue = check_and_put_new_process_in_ready_queue(process, ticks,
                                                                                      process_counter,
                                                                                      process_queue)
            continue

        current_process = process_queue.get()
        current_process["remaining_quanta"] = time_quanta
    else:
        current_process = auxiliary_queue.get()

    if current_process["start_time"] < 0:
        current_process["start_time"] = ticks
        current_process["remaining_time"] = current_process["cpu_bursts"][0]

    remaining_time = current_process["remaining_time"]
    ticks += min(time_quanta, current_process["remaining_quanta"], current_process["remaining_time"])
    current_process["remaining_time"] -= \
        min(time_quanta, current_process["remaining_time"], current_process["remaining_quanta"])
    current_process["remaining_quanta"] -= remaining_time

    process_counter, process_queue = check_and_put_new_process_in_ready_queue(process, ticks,
                                                                              process_counter, process_queue)

    w, a = check_and_return_process_from_waiting_to_auxiliary_queue(waiting_queue, auxiliary_queue, ticks)
    waiting_queue = w
    auxiliary_queue = a

    if current_process["remaining_time"] > 0:
        process_queue.put(current_process)
    else:
        if current_process["current_cpu_burst"] < (current_process["cpu_bursts"].__len__() - 1):
            current_process["return_time"] = ticks + current_process["io_bursts"][current_process["current_cpu_burst"]]
            current_process["current_cpu_burst"] += 1
            current_process["remaining_time"] = current_process["cpu_bursts"][current_process["current_cpu_burst"]]
            waiting_queue.append(current_process)
        else:
            current_process["finish_time"] = ticks

            total_waiting_time += \
                (current_process["finish_time"] - current_process["arrival_time"] -
                 sum(current_process["cpu_bursts"]) - sum(current_process["io_bursts"]))

            total_turnaround_time += (ticks - current_process["arrival_time"])

            process_completed += 1

print("\nAverage Waiting Time : {Average_Waiting_Time}"
      .format(Average_Waiting_Time=(total_waiting_time/number_of_process)))

print("\nAverage Turnaround Time : {Average_Turnaround_Time}"
      .format(Average_Turnaround_Time=(total_turnaround_time/number_of_process)))
