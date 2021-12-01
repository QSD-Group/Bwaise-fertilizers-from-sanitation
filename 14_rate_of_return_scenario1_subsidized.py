# UIUC Environmental Engineering and Science Master's Thesis Project Updated for Publication
# Title: Novel financing strategies to simultaneously advance development goals for sanitation and agriculture
# through nutrient recovery
# Author: Hannah A.C. Lohman
# Created: April 11, 2019
# Updated: April 11, 2019

# This script, rate_of_return_scenario1_subsidized.py, rate of return expected over the system lifetime
# (8 years) for the scenario with aid assuming UDDT, transport, and storage of urine (no downstream processing).
# Costs include capital, labor, operation, consumables, and maintenance.
# Benefits result from nutrient payments and pit latrine payments.

# ~~~~~~~IMPORT PACKAGES, DATA, AND FILES NECESSARY~~~~~~~

import pandas as pd  # import pandas for matrix data manipulation
from scipy.optimize import least_squares
import numpy as np

mat_cost = pd.read_excel('RESULTS_cap_op_cons_maint_costs_FilterReuse_July31.xlsx', sheetname='material')  # (USD) import material costs
labor_cost = pd.read_excel('RESULTS_cap_op_cons_maint_costs_FilterReuse_July31.xlsx', sheetname='labor')  # (USD) import labor costs
con_cost = pd.read_excel('RESULTS_cap_op_cons_maint_costs_FilterReuse_July31.xlsx', sheetname='consumable')  # (USD/yr) consumable costs
op_cost = pd.read_excel('RESULTS_cap_op_cons_maint_costs_FilterReuse_July31.xlsx', sheetname='op')  # (USD/yr) import operation costs
maint_cost = pd.read_excel('RESULTS_cap_op_cons_maint_costs_FilterReuse_July31.xlsx', sheetname='maint')  # (USD) import maintenance costs
nutrients = pd.read_excel('RESULTS_per_capita_nutrients.xlsx', sheetname='rec_nutrients_after_U_T_S')  # import recovered nutrients
nutrient_payment_range = pd.read_excel('input_data_file.xlsx', sheetname='nutrient_payment_shortened')  # (USD/kg)

tank_maint_ratio = pd.read_excel('OUTPUT_uncertainty_ranges.xlsx', sheetname='maint_cost_ratio')
tank_op_ratio = pd.read_excel('OUTPUT_uncertainty_ranges.xlsx', sheetname='op_cost_ratio')
tank_labor_ratio = pd.read_excel('OUTPUT_uncertainty_ranges.xlsx', sheetname='labor_cost_ratio')
tank_cost = pd.read_excel('OUTPUT_uncertainty_ranges.xlsx', sheetname='RR_uniform')  # (USD/tank)
urine_volume = pd.read_excel('OUTPUT_uncertainty_ranges.xlsx', sheetname='RR_triangle')  # (L/cap/d)

# ~~~~~~~CONSTANTS~~~~~~~

N_runs = 10000
lifetime = 8  # (years) lifetime of all technologies and project duration for rate of return calculations
UDDT_users = 40  # (people) number of people using a UDDT unit (with 2 toilets)
UDDT_qty = 500  # assume 1,000 toilets and UDDT has 2 per unit
urine_storage_time = 80  # (days)

# ~~~~~~~RATE OF RETURN FUNCTION DEFINITION~~~~~~~
# solving for rate of return (r)
# where mat = initial material costs (USD), labor = construction labor costs (USD),
# op = annual operation costs (USD/yr), con = annual consumables cost (USD/yr),
# maint = maintenance cost at half the lifetime (USD), lifetime = system lifetime (years)


def solve_for_r(r):

    return (mat_FINAL + labor_FINAL) \
           + op_FINAL * (((1.0 + r) ** lifetime - 1.0) / (r * (1.0 + r) ** lifetime)) \
           + maint_FINAL * (1.0 + r) ** (-4.0) \
           - nutrient_payment * (((1.0 + r) ** lifetime - 1.0) / (r * (1.0 + r) ** lifetime))


# ~~~~~~~RATE OF RETURN CALCULATIONS (WITH AID)~~~~~~~
writer = pd.ExcelWriter('RESULTS_rate_of_return_Scenario1_subsidized_July31_test.xlsx', engine='xlsxwriter')
RoR_frontier_FINAL = pd.DataFrame()

for i in range(N_runs):  # N_runs
    total_tank_volume = urine_volume.urine_volume[i] * UDDT_qty * UDDT_users * urine_storage_time  # (L) 80-day volume
    qty_tanks = total_tank_volume/1000  # total number of 1000 L urine storage tanks
    qty_tanks = np.ceil(qty_tanks)  # round tanks up to the nearest whole tank
    mat_cost_tank = tank_cost.cost_urine_tank1[i] * qty_tanks  # (USD)
    labor_cost_tank = tank_labor_ratio.tank[i] * mat_cost_tank  # (USD)
    op_cost_tank = tank_op_ratio.tank[i] * mat_cost_tank  # (USD/yr)
    maint_cost_tank = tank_maint_ratio.tank[i] * mat_cost_tank  # (USD) at year 4

    mat1 = mat_cost.material_UDDT[i] + mat_cost_tank  # (USD) total material cost
    labor1 = labor_cost.labor_UDDT[i] + labor_cost_tank  # (USD) total construction labor cost
    op1 = op_cost.annual_op_UDDT[i] + op_cost_tank  # (USD/yr) total annual operation cost
    maint1 = maint_cost.maint_UDDT[i] + maint_cost_tank  # (USD) total maintenance cost at year 4
    mat2 = mat_cost.material_pit[i]  # (USD) material cost payment of a pit latrine
    labor2 = labor_cost.labor_pit[i]  # (USD) labor cost payment of a pit latrine
    op2 = op_cost.annual_op_pit[i]  # (USD/yr) annual operation cost payment of a pit latrine
    maint2 = maint_cost.maint_pit[i]  # (USD) maintenance cost payment of a pit latrine at year 4

    mat_FINAL = mat1 - mat2  # (USD) total material cost minus material payment for pit latrine
    labor_FINAL = labor1 - labor2  # (USD) total labor cost minus labor payment for pit latrine
    op_FINAL = op1 - op2  # (USD/yr) total annual operation cost minus operation payment for pit latrine
    maint_FINAL = maint1 - maint2  # (USD) maintenance cost minus maintenance cost payment of a pit latrine at year 4

    RoR_FINAL = pd.DataFrame()

    for j in range(101):  # 101 because have 101 payment values ($0 to $5.00 increments of $0.05)
        annual_mass_nutrients = 365 * UDDT_users * UDDT_qty * (nutrients.N_rec_U_T_S_urine[i]
                                                               + nutrients.P_rec_U_T_S_urine[i]
                                                               + nutrients.K_rec_U_T_S_urine[i])  # (kg nutrients/year)
        nutrient_payment = nutrient_payment_range.nutrient_payment[j] * annual_mass_nutrients  # (USD/yr)
        sol = least_squares(solve_for_r, 1, bounds=(0, 50))  # upper bound is a rate of return of 50 or 5000%

        RoR = sol.x
        RoR = list(RoR)
        RoR = str(RoR)[1:-1]
        RoR = float(RoR)

        output = pd.DataFrame([RoR])
        RoR_FINAL = pd.concat([RoR_FINAL, output])

    RoR_FINAL = RoR_FINAL.transpose()
    RoR_frontier_FINAL = pd.concat([RoR_frontier_FINAL, RoR_FINAL]).reset_index(drop=True)

RoR_frontier_FINAL.columns = [nutrient_payment_range.nutrient_payment]
RoR_frontier_FINAL.to_excel(writer)

writer.save()
