import pandas as pd

# Input
# FP timeline
isi_padat = input("Waktu isi padat: ")
cuci1_padat = input("Waktu cuci air recycling: ")
cuci2_padat = input("Waktu cuci air bersih: ")
sec_press_padat = input("Waktu second pressing: ")
cuci3_padat = input("Waktu cuci air bersih 2: ")
bongkar_padat = input("Waktu bongkar padat: ")

# GT timeline
isi_becek = input("Waktu isi becek: ")
cuci1_becek = input("Waktu cuci air recycling: ")
cuci2_becek = input("Waktu cuci air bersih: ")
sec_press_becek = input("Waktu second pressing: ")
bongkar_becek = input("Waktu bongkar becek: ")

steps_padat = [
    {'Step': 'A', 'Duration': int(isi_padat)},
    {'Step': 'B', 'Duration': int(cuci1_padat)},
    {'Step': 'C', 'Duration': int(cuci2_padat)},
    {'Step': 'D', 'Duration': int(sec_press_padat)},
    {'Step': 'E', 'Duration': int(cuci3_padat)},
    {'Step': 'F', 'Duration': int(bongkar_padat)}
]

steps_becek = [
    {'Step': 'U', 'Duration': int(isi_becek)},
    {'Step': 'W', 'Duration': int(cuci1_becek)},
    {'Step': 'X', 'Duration': int(cuci2_becek)},
    {'Step': 'Y', 'Duration': int(sec_press_becek)},
    {'Step': 'Z', 'Duration': int(bongkar_becek)}
]

# Initialize schedules and trackers
time_machine_1 = 0  # Start time for Machine 1
time_machine_2 = 0  # Start time for Machine 2
time_machine_3 = 0  # Start time for Machine 3
supply_available = 0  # Number of available supplies
supplies_produced = 0
finished_goods = 0
time_limit = 500  
time_steps = list(range(0, time_limit + 10, 10))  # Timeframe in 10-minute steps

# Create empty schedule grid
schedule_grid = {
    "Timeframe": time_steps,
    "Machine 1": [""] * len(time_steps),
    "Machine 2": [""] * len(time_steps),
    "Machine 3": [""] * len(time_steps)
}

# Process within the time limit
while max(time_machine_1, time_machine_2, time_machine_3) < time_limit:
    # Ground Tank timeline
    for step in steps_becek:
        if time_machine_3 >= time_limit:
            break
        start_time = time_machine_3
        end_time = time_machine_3 + step['Duration']
        for t in range(start_time, end_time, 10):
            schedule_grid["Machine 3"][time_steps.index(t)] = step['Step']
        time_machine_3 = end_time

    # Bongkar becek
    if time_machine_3 <= time_limit:
        supply_available += 2
        supplies_produced += 2

    # Machine 1 operates step A if supply is available
    if supply_available > 0 and time_machine_1 < time_limit:
        start_time = max(time_machine_1, time_machine_3)
        end_time = start_time + steps_padat[0]['Duration']
        for t in range(start_time, end_time, 10):
            schedule_grid["Machine 1"][time_steps.index(t)] = 'A'
        time_machine_1 = end_time
        supply_available -= 1

    # Machine 2 operates step A after Machine 1 finishes step A
    if supply_available > 0 and time_machine_2 < time_limit:
        start_time = max(time_machine_2, time_machine_1)
        end_time = start_time + steps_padat[0]['Duration']
        for t in range(start_time, end_time, 10):
            schedule_grid["Machine 2"][time_steps.index(t)] = 'A'
        time_machine_2 = end_time
        supply_available -= 1

    # Machine 1 and 2 independently perform steps B and C
    for step in steps_padat[1:]:
        if time_machine_1 < time_limit:
            start_time = time_machine_1
            end_time = start_time + step['Duration']
            for t in range(start_time, end_time, 10):
                schedule_grid["Machine 1"][time_steps.index(t)] = step['Step']
            time_machine_1 = end_time
            if step['Step'] == 'F' and time_machine_1 <= time_limit:
                finished_goods += 2
        
        if time_machine_2 < time_limit:
            start_time = time_machine_2
            end_time = start_time + step['Duration']
            for t in range(start_time, end_time, 10):
                schedule_grid["Machine 2"][time_steps.index(t)] = step['Step']
            time_machine_2 = end_time
            if step['Step'] == 'F' and time_machine_2 <= time_limit:
                finished_goods += 2

# Convert the schedule grid to a DataFrame
schedule_df = pd.DataFrame(schedule_grid)

# Display the schedule
print(schedule_df)
print(f"\nTotal supplies produced: {supplies_produced}")
print(f"Total finished goods produced: {finished_goods}")

print(supply_available)