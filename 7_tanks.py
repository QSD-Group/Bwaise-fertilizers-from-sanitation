# ~~~~~~~IMPORT DATA AND FILES NECESSARY~~~~~~~

import pandas as pd  # import pandas for matrix data manipulation
import numpy as np

N_runs = 10000

writer = pd.ExcelWriter('RESULTS_tank_quantity.xlsx', engine='xlsxwriter')

# Simple System Tank Requirements
urine_volume = pd.read_excel('OUTPUT_uncertainty_ranges.xlsx', sheetname='RR_triangle')  # (L/cap/d)
UDDT_users = 40  # (people) number of people using a UDDT unit (with 2 toilets)
UDDT_qty = 500  # assume 1,000 toilets and UDDT has 2 per unit
urine_storage_time = 80  # (days)

tank_simple_FINAL = pd.DataFrame()
for i in range(N_runs):
    total_tank_volume = urine_volume.urine_volume[i] * UDDT_qty * UDDT_users * urine_storage_time  # (L) 80-day volume
    qty_tanks = total_tank_volume / 1000  # total number of 1000 L urine storage tanks
    qty_tanks = np.ceil(qty_tanks)  # round tanks up to the nearest whole tank

    output1 = pd.DataFrame([qty_tanks])  # (USD/kg total nutrients)
    output1 = output1.transpose()
    tank_simple_FINAL = pd.concat([tank_simple_FINAL, output1]).reset_index(drop=True)

# Advanced System Tank Requirements
general_parameters_triangle = pd.read_excel('OUTPUT_uncertainty_ranges.xlsx', sheetname='RR_triangle')
reference_flow = 1000  # Number of UDDTs assumed to be 1,000 (or 500 of the modeled units)
UDDT_users = 20  # UNHCR assumes 20 users per UDDT and modeled unit is 2 UDDTs combined

tank_advanced_FINAL = pd.DataFrame()
for i in range(N_runs):
    urine_volume = general_parameters_triangle.urine_volume[i]  # (L/cap/d) daily volume of urine produced per capita
    daily_urine_volume = urine_volume * UDDT_users * reference_flow  # (L/d) total urine volume of reference flow

    # Community storage tanks
    total_tank_volume_L = UDDT_users * reference_flow * ((0.33 * 1 * urine_volume) + (0.33 * 2 * urine_volume) +
                                                         (0.33 * 3 * urine_volume))  # (L) assume tank emptied every 3 days
    number_of_tanks = total_tank_volume_L / 1000  # total number of 1000 L tanks for 1,000 UDDTs serving 20 people each
    number_of_tanks = np.ceil(number_of_tanks)  # round the number of tanks up to the nearest whole number
    number_of_urine_tanks1 = number_of_tanks  # total number of storage tanks in community

    output2 = pd.DataFrame([number_of_urine_tanks1])
    output2 = output2.transpose()
    tank_advanced_FINAL = pd.concat([tank_advanced_FINAL, output2]).reset_index(drop=True)

tank_simple_FINAL.to_excel(writer, sheet_name='simple_tanks')
tank_advanced_FINAL.to_excel(writer, sheet_name='advanced_tanks')

writer.save()
