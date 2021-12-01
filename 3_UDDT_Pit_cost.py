# Title: Novel financing strategies to simultaneously advance development goals for sanitation and agriculture
# through nutrient recovery
# Author: Hannah A.C. Lohman
# Created: March 11, 2019
# Updated: March 11, 2019

# This script, UDDT_Pit_cost.py, calculates the capital, labor, and O&M costs for a pit latrine (D402 & D403)
# and UDDT (D406)

# ~~~~~~~IMPORT DATA AND FILES NECESSARY~~~~~~~

import pandas as pd  # import pandas for matrix data manipulation
material_cost = pd.read_excel('RESULTS_UDDT_Pit_capital_costs.xlsx', sheetname='capital_cost')
labor_cost_ratio = pd.read_excel('OUTPUT_uncertainty_ranges.xlsx', sheetname='labor_cost_ratio')
op_cost_ratio = pd.read_excel('OUTPUT_uncertainty_ranges.xlsx', sheetname='op_cost_ratio')
maint_cost_ratio = pd.read_excel('OUTPUT_uncertainty_ranges.xlsx', sheetname='maint_cost_ratio')

# ~~~~~~~CONSTANTS~~~~~~~
N_runs = 10000
usd_to_ugx = 3693.8  # UGX to USD conversion as of August 7, 2018

writer = pd.ExcelWriter('RESULTS_UDDT_pit_costs.xlsx')
pit_UDDT_cost_FINAL = pd.DataFrame()

for i in range(N_runs):
    cap_UDDT = material_cost.D406[i]/usd_to_ugx
    labor_UDDT = cap_UDDT * labor_cost_ratio.D406[i]
    op_UDDT = cap_UDDT * op_cost_ratio.D406[i]
    maint_UDDT = cap_UDDT * maint_cost_ratio.D406[i]

    cap_slab = material_cost.D402[i]/usd_to_ugx
    labor_slab = cap_slab * labor_cost_ratio.D402[i]
    op_slab = cap_slab * op_cost_ratio.D402[i]
    maint_slab = cap_slab * maint_cost_ratio.D402[i]

    cap_pit = material_cost.D403[i]/usd_to_ugx
    labor_pit = cap_pit * labor_cost_ratio.D403[i]
    op_pit = cap_pit * op_cost_ratio.D403[i]
    maint_pit = cap_pit * maint_cost_ratio.D403[i]

    cap_pit_total = cap_slab + cap_pit
    labor_pit_total = labor_slab + labor_pit
    op_pit_total = op_slab + op_pit
    maint_pit_total = maint_slab + maint_pit

    output = pd.DataFrame([cap_pit_total, labor_pit_total, op_pit_total, maint_pit_total, cap_UDDT, labor_UDDT,
                           op_UDDT, maint_UDDT])
    output = output.transpose()
    pit_UDDT_cost_FINAL = pd.concat([pit_UDDT_cost_FINAL, output]).reset_index(drop=True)

pit_UDDT_cost_FINAL.columns = ('cap_pit', 'labor_pit', 'op_pit', 'maint_pit', 'cap_UDDT', 'labor_UDDT',
                               'op_UDDT', 'maint_UDDT')

pit_UDDT_cost_FINAL.to_excel(writer)
writer.save()



