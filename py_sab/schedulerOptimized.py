import streamlit as st
import pandas as pd

# Input for FP timeline with unique keys for UI
isi_padat = st.text_input("Waktu isi padat: ", key="isi_padat")
cuci1_padat = st.text_input("Waktu cuci air recycling: ", key="cuci1_padat")
cuci2_padat = st.text_input("Waktu cuci air bersih: ", key="cuci2_padat")
sec_press_padat = st.text_input("Waktu second pressing: ", key="sec_press_padat")
cuci3_padat = st.text_input("Waktu cuci air bersih 2: ", key="cuci3_padat")
bongkar_padat = st.text_input("Waktu bongkar padat: ", key="bongkar_padat")

# Input for GT timeline with unique keys for for UI
isi_becek = st.text_input("Waktu isi becek: ", key="isi_becek")
cuci1_becek = st.text_input("Waktu cuci air recycling: ", key="cuci1_becek")
cuci2_becek = st.text_input("Waktu cuci air bersih: ", key="cuci2_becek")
sec_press_becek = st.text_input("Waktu second pressing: ", key="sec_press_becek")
bongkar_becek = st.text_input("Waktu bongkar becek: ", key="bongkar_becek")


if isi_padat and cuci1_padat and cuci2_padat and sec_press_padat and cuci3_padat and bongkar_padat and isi_becek and cuci1_becek and cuci2_becek and sec_press_becek and bongkar_becek: # UI INPUT VALIDATION
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

    # Calculate total time
    total_time = sum(step['Duration'] for step in steps_padat + steps_becek)
    time_limit = 500  
    st.write(f"Total time from all inputs: {total_time}")

    if total_time > time_limit:
        st.write(f"Total time exceeds time limit. Current time: {total_time}. Machine Stop Process")
    else:
        st.write(f"Total time is within the limit: {total_time}")

        # Initialize schedules and trackers
        time_machine_1 = 0  
        time_machine_2 = 0  
        time_machine_3 = 0  
        supply_available = 0  
        supplies_produced = 0
        finished_goods = 0

        # Timeframe in 10-minute steps
        time_steps = list(range(0, max(time_limit, total_time) + 10, 10))

        # Initialize empty schedule grid
        schedule_grid = {
            "Timeframe": time_steps,
            "Machine 1": [""] * len(time_steps),
            "Machine 2": [""] * len(time_steps),
            "Machine 3": [""] * len(time_steps)
        }

        # Process within the time limit
        while time_machine_1 < time_limit or time_machine_2 < time_limit or time_machine_3 < time_limit:
            # Ground Tank timeline (for Machine 3)
            for step in steps_becek:
                if time_machine_3 >= time_limit:
                    break
                start_time = time_machine_3
                end_time = time_machine_3 + step['Duration']
                for t in range(start_time, end_time, 10):
                    if t < max(time_steps):  # Only update within the defined time steps range
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
                    if t < max(time_steps):
                        schedule_grid["Machine 1"][time_steps.index(t)] = 'A'
                time_machine_1 = end_time
                supply_available -= 1

            # Machine 2 operates step A after Machine 1 finishes step A
            if supply_available > 0 and time_machine_2 < time_limit:
                start_time = max(time_machine_2, time_machine_1)
                end_time = start_time + steps_padat[0]['Duration']
                for t in range(start_time, end_time, 10):
                    if t < max(time_steps):
                        schedule_grid["Machine 2"][time_steps.index(t)] = 'A'
                time_machine_2 = end_time
                supply_available -= 1

            # Machine 1 and 2 independently perform steps B and C
            for step in steps_padat[1:]:
                if time_machine_1 < time_limit:
                    start_time = time_machine_1
                    end_time = start_time + step['Duration']
                    for t in range(start_time, end_time, 10):
                        if t < max(time_steps):  
                            schedule_grid["Machine 1"][time_steps.index(t)] = step['Step']
                    time_machine_1 = end_time
                    if step['Step'] == 'F' and time_machine_1 <= time_limit:
                        finished_goods += 2

                if time_machine_2 < time_limit:
                    start_time = time_machine_2
                    end_time = start_time + step['Duration']
                    for t in range(start_time, end_time, 10):
                        if t < max(time_steps):  
                            schedule_grid["Machine 2"][time_steps.index(t)] = step['Step']
                    time_machine_2 = end_time
                    if step['Step'] == 'F' and time_machine_2 <= time_limit:
                        finished_goods += 2

        # Convert the schedule grid to a DataFrame
        schedule_df = pd.DataFrame(schedule_grid)

        # Display the schedule using Streamlit
        st.write(schedule_df)
        st.write(f"\nTotal supplies produced: {supplies_produced}")
        st.write(f"Total finished goods produced: {finished_goods}")
        st.write(f"available supply: {supply_available}")
