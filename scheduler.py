import pandas as pd

# Input
time_limit = 200  # Time limit

# FP timeline (padat steps)
isi_padat = int(input("Waktu isi padat: "))
cuci1_padat = int(input("Waktu cuci air recycling: "))
cuci2_padat = int(input("Waktu cuci air bersih: "))
sec_press_padat = int(input("Waktu second pressing: "))
cuci3_padat = int(input("Waktu cuci air bersih 2: "))
bongkar_padat = int(input("Waktu bongkar padat: "))

# GT timeline (becek steps)
isi_becek = int(input("Waktu isi becek: "))
cuci1_becek = int(input("Waktu cuci air recycling: "))
cuci2_becek = int(input("Waktu cuci air bersih: "))
sec_press_becek = int(input("Waktu second pressing: "))
bongkar_becek = int(input("Waktu bongkar becek: "))

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

# Initialize schedule trackers
time_machine_1 = 0  # Machine 1 for padat
time_machine_2 = 0  # Machine 2 for padat
time_machine_3 = 0  # Machine 3 for becek
supply_available = 0
finished_goods = 0

# Timeframe in 10-minute steps
time_steps = list(range(0, time_limit + 10, 10))

# Initialize empty schedule grid
schedule_grid = {
    "Timeframe": time_steps,
    "Machine 1": [""] * len(time_steps),
    "Machine 2": [""] * len(time_steps),
    "Machine 3": [""] * len(time_steps)
}



# prevent machine run not full cycle step
def can_complete_cycle(current_time, steps):
    total_duration = sum(step['Duration'] for step in steps)
    return current_time + total_duration <= time_limit

# Machine 3 operates for becek steps
def run_machine_3(time_machine_3, steps_becek):
    global supply_available
    while time_machine_3 < time_limit:
        # Check if there is enough time for the full cycle
        if can_complete_cycle(time_machine_3, steps_becek):
            for step in steps_becek:
                start_time = time_machine_3
                end_time = time_machine_3 + step['Duration']
                for t in range(start_time, end_time, 10):
                    if t < max(time_steps):  # Only update within the defined time steps range
                        schedule_grid["Machine 3"][time_steps.index(t)] = step['Step']
                time_machine_3 = end_time
            supply_available += 2  # 1 cycle machine 3 produce 2 supply and can be used to machine 1 and 2
        else:
            break  # Stop if not enough time for a full cycle

run_machine_3(time_machine_3, steps_becek)

# analysis last in here

# Machine 1 and 2 will perform padat steps
def run_machine(time_machine, machine_name, steps):
    global supply_available, finished_goods
    while time_machine < time_limit:
        
        if can_complete_cycle(time_machine, steps):
            for step in steps:
                start_time = time_machine
                end_time = time_machine + step['Duration']
                for t in range(start_time, end_time, 10):
                    if t < max(time_steps):  
                        schedule_grid[machine_name][time_steps.index(t)] = step['Step']
                time_machine = end_time
            supply_available -= 1
            finished_goods += 2  
        else:
            break  

run_machine(time_machine_1, "Machine 1", steps_padat)
run_machine(time_machine_2, "Machine 2", steps_padat)



# Convert the schedule grid to a DataFrame
schedule_df = pd.DataFrame(schedule_grid)

# Display the schedule
print(schedule_df)
pd.options.display.max_rows = 1000
print(f"\nTotal finished goods produced: {finished_goods}")
print(f"Available supply: {supply_available}")
