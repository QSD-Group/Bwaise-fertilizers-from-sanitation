# UIUC Environmental Engineering and Science Master's Thesis Project Updated for Publication
# Title: Novel financing strategies to simultaneously advance development goals for sanitation and agriculture
# through nutrient recovery
# Author: Hannah A.C. Lohman
# Created: March 13, 2019
# Updated: March 14, 2019

# This script, rate_of_return_unsubsidized_shortened.py, rate of return expected over the system lifetime
# (8 years) for the scenario without aid. This is a smaller range of resource payment values.
# Costs include capital, labor, operation, consumables, and maintenance.
# Benefits result from nutrient payments.

# ~~~~~~~IMPORT PACKAGES, DATA, AND FILES NECESSARY~~~~~~~

import pandas as pd  # import pandas for matrix data manipulation
from scipy.optimize import least_squares
import numpy as np

mat_cost = pd.read_excel('RESULTS_cap_op_cons_maint_costs_FilterReuse_July31.xlsx', sheetname='material')  # (USD) import material costs
labor_cost = pd.read_excel('RESULTS_cap_op_cons_maint_costs_FilterReuse_July31.xlsx', sheetname='labor')  # (USD) import labor costs
con_cost = pd.read_excel('RESULTS_cap_op_cons_maint_costs_FilterReuse_July31.xlsx', sheetname='consumable')  # (USD/yr) consumable costs
op_cost = pd.read_excel('RESULTS_cap_op_cons_maint_costs_FilterReuse_July31.xlsx', sheetname='op')  # (USD/yr) import operation costs
maint_cost = pd.read_excel('RESULTS_cap_op_cons_maint_costs_FilterReuse_July31.xlsx', sheetname='maint')  # (USD) import maintenance costs
nutrients = pd.read_excel('RESULTS_RR_costs_FilterReuse.xlsx', sheetname='nutrients_recovered')  # import recovered nutrients
nutrient_payment_range = pd.read_excel('input_data_file.xlsx', sheetname='nutrient_payment_shortened')  # (USD per kg)

# ~~~~~~~CONSTANTS~~~~~~~

N_runs = 10000
lifetime = 8  # (years) lifetime of all technologies and project duration for rate of return calculations

# ~~~~~~~RATE OF RETURN FUNCTION DEFINITION~~~~~~~
# solving for rate of return (r)
# where mat = initial material costs (USD), labor = construction labor costs (USD),
# op = annual operation costs (USD/yr), con = annual consumables cost (USD/yr),
# maint = maintenance cost at half the lifetime (USD), lifetime = system lifetime (years)


def solve_for_r(r):

    return (mat + labor) + (op + con) * (((1.0 + r) ** lifetime - 1.0) / (r * (1.0 + r) ** lifetime)) \
           + maint * (1.0 + r) ** (-4.0) \
           - nutrient_payment * (((1.0 + r) ** lifetime - 1.0) / (r * (1.0 + r) ** lifetime))


# ~~~~~~~RATE OF RETURN CALCULATIONS (WITH AID)~~~~~~~
writer = pd.ExcelWriter('RESULTS_rate_of_return_Scenario2_unsubsidized_July31.xlsx', engine='xlsxwriter')
RoR_frontier_FINAL = pd.DataFrame()

for i in range(N_runs):
    mat = mat_cost.material_UDDT[i] + mat_cost.material_off_site_tanks[i] \
          + mat_cost.material_on_site_tanks[i] + mat_cost.material_struvite[i] \
          + mat_cost.material_ion_exchange[i]  # (USD) total material cost
    labor = labor_cost.labor_UDDT[i] + labor_cost.labor_off_site_tanks[i] \
            + labor_cost.labor_on_site_tanks[i] + labor_cost.labor_struvite[i] \
            + labor_cost.labor_ion_exchange[i]  # (USD) total construction labor cost
    op = op_cost.annual_op_UDDT[i] + op_cost.annual_op_off_site_tanks[i] \
         + op_cost.annual_op_on_site_tanks[i] + op_cost.annual_op_struvite[i] \
         + op_cost.annual_op_ion_exchange[i]  # (USD/yr) total annual operation and maintenance cost
    con = con_cost.annual_con_struvite_filter[i] + con_cost.annual_con_struvite_MgOH2[i] \
          + con_cost.annual_con_ion_exchange_resin[i] \
          + con_cost.annual_con_ion_exchange_H2SO4[i]  # (USD/yr)
    maint = maint_cost.maint_UDDT[i] + maint_cost.maint_off_site_tanks[i] + maint_cost.maint_on_site_tanks[i] \
            + maint_cost.maint_struvite[i] + maint_cost.maint_ion_exchange[i]  # (USD) total maintenance cost at year 4

    RoR_FINAL = pd.DataFrame()

    annual_mass_nutrients = nutrients.annual_N_recovery[i] + nutrients.annual_P_recovery[i] \
                            + nutrients.annual_K_recovery[i]  # (kg nutrients per year)

    for j in range(101):  # 101 because have 101 payment values ($0 to $5 increments of $0.05)
        annual_mass_nutrients = nutrients.annual_N_recovery[i] + nutrients.annual_P_recovery[i] \
                                + nutrients.annual_K_recovery[i]  # (kg nutrients per year)
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
