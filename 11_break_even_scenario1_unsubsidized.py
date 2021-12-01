# Title: Novel financing strategies to simultaneously advance development goals for sanitation and agriculture
# through nutrient recovery
# Author: Hannah A.C. Lohman
# Created: May 30, 2019
# Updated: May 30, 2019

# This script, DCA_break_even_transport_storage_unsubsidized.py, calculates the break even resource payment necessary to
# incentivize urine diversion dry toilet construction and urine treatment (without aid payment from aid agency)

# ~~~~~~~IMPORT DATA AND FILES NECESSARY~~~~~~~

import pandas as pd  # import pandas for matrix data manipulation
import numpy as np

UDDT_pit_cost = pd.read_excel('RESULTS_UDDT_pit_costs.xlsx')  # import costs related to pit latrine and UDDT (USD)
RR_material_cost = pd.read_excel('RESULTS_RR_costs_FilterReuse.xlsx', sheetname='capital_cost')  # material costs (USD)
RR_labor_cost = pd.read_excel('RESULTS_RR_costs_FilterReuse.xlsx', sheetname='labor_cost')  # labor costs for treatment (USD)
RR_op_cost = pd.read_excel('RESULTS_RR_costs_FilterReuse.xlsx', sheetname='op_cost')  # operation costs for treatment (USD)
RR_maint_cost = pd.read_excel('RESULTS_RR_costs_FilterReuse.xlsx', sheetname='maint_cost')  # maint costs for treatment (USD)

tank_maint_ratio = pd.read_excel('OUTPUT_uncertainty_ranges.xlsx', sheetname='maint_cost_ratio')
tank_op_ratio = pd.read_excel('OUTPUT_uncertainty_ranges.xlsx', sheetname='op_cost_ratio')
tank_labor_ratio = pd.read_excel('OUTPUT_uncertainty_ranges.xlsx', sheetname='labor_cost_ratio')
tank_cost = pd.read_excel('OUTPUT_uncertainty_ranges.xlsx', sheetname='RR_uniform')  # (USD/tank)
urine_volume = pd.read_excel('OUTPUT_uncertainty_ranges.xlsx', sheetname='RR_triangle')  # (L/cap/d)

nutrients = pd.read_excel('RESULTS_per_capita_nutrients.xlsx', sheetname='rec_nutrients_after_U_T_S')  # (kg/cap/day)
DCA_parameters = pd.read_excel('OUTPUT_uncertainty_ranges.xlsx', sheetname='DCA_parameters')  # tax and discount rates

# ~~~~~~~CONSTANTS~~~~~~~

N_runs = 10000
UDDT_users = 40  # (people) number of people using a UDDT unit (with 2 toilets)
UDDT_qty = 500  # assume 1,000 toilets and UDDT has 2 per unit
pit_qty = 500  # assume 1,000 toilets and pit has 1 per unit
UDDT_lifetime = 8  # (years) can eventually vary
pit_lifetime = 8  # (years) can eventually vary
tank_lifetime = 8  # (years) can eventually vary
currency_conversion = 3693.8  # UGX to USD conversion as of August 7, 2018
urine_storage_time = 80  # (days)
tanks_per_land = 154  # number of tanks per 50'x100' plot of land

# ~~~~~~~BREAK EVEN IN 8 YEARS CALCULATION~~~~~~~

# positive costs indicate a cost to the contractor/NGO and negative costs indicate a payment to the contractor/NGO

writer = pd.ExcelWriter('RESULTS_break_even_Scenario1_unsubsidized_July31.xlsx', engine='xlsxwriter')
break_even_scenario_FINAL = pd.DataFrame()

# Break Even Calculation for UDDT, Transport, and Storage (ALL)
for i in range(N_runs):

    # Income Tax Rate and Discount Rate

    income_tax = DCA_parameters.income_tax[i]  # (no unit) income tax rate in decimal form
    discount_rate = DCA_parameters.discount_rate[i]  # (no unit) discount rate in decimal form

    # Capital Costs (Total to Treat 20,000 People Reference Flow)

    material_UDDT = UDDT_pit_cost.cap_UDDT[i] * UDDT_qty  # (USD) total material cost of 500 UDDT units
    total_tank_volume = urine_volume.urine_volume[i] * UDDT_qty * UDDT_users * urine_storage_time  # (L) 80-day volume
    qty_tanks = total_tank_volume/1000  # total number of 1000 L urine storage tanks
    qty_tanks = np.ceil(qty_tanks)  # round tanks up to the nearest whole tank
    material_tank = tank_cost.cost_urine_tank1[i] * qty_tanks  # (USD)

    labor_UDDT = UDDT_pit_cost.labor_UDDT[i] * UDDT_qty  # (USD) total construction labor cost of 500 UDDT units
    labor_tank = tank_labor_ratio.tank[i] * material_tank  # (USD)

    # Ongoing Costs (Ei)

    # Operation Costs for Equipment/Capital
    annual_op_UDDT = UDDT_pit_cost.op_UDDT[i] * UDDT_qty  # (USD/yr) annual operation cost of 500 UDDT units
    op_tank = tank_op_ratio.tank[i] * material_tank  # (USD/yr)
    annual_op_TOTAL = annual_op_UDDT + op_tank  # (USD/yr) total annual operation cost of capital

    # Land Costs for Off Site Tanks
    land_qty = qty_tanks/tanks_per_land
    land_qty = np.ceil(land_qty)
    annual_land_cost = land_qty * tank_cost.lease_50_100[i]

    # Maintenance Costs for Equipment/Capital (Maintenance Occurs at 1/2 Lifetime)
    maint_UDDT = UDDT_pit_cost.maint_UDDT[i] * UDDT_qty  # (USD) maintenance (at 1/2 lifetime) cost of 500 UDDT units
    maint_tank = tank_maint_ratio.tank[i] * material_tank  # (USD) at year 4
    maint_TOTAL = maint_UDDT + maint_tank  # (USD)

    annual_ongoing_costs = annual_op_TOTAL + annual_land_cost  # (USD/yr) total op and consumables cost (different yr 4)
    annual_ongoing_costs_yr4 = annual_ongoing_costs + maint_TOTAL  # (USD/yr) total ongoing costs at year 4 with maint

    # Depreciation Charge (Di)

    depreciation_charge_UDDT = material_UDDT/UDDT_lifetime
    depreciation_charge_tank = material_tank/tank_lifetime

    # Discount Factor (di)

    di1 = 1/(1 + discount_rate)**1
    di2 = 1/(1 + discount_rate)**2
    di3 = 1/(1 + discount_rate)**3
    di4 = 1/(1 + discount_rate)**4
    di5 = 1/(1 + discount_rate)**5
    di6 = 1/(1 + discount_rate)**6
    di7 = 1/(1 + discount_rate)**7
    di8 = 1/(1 + discount_rate)**8

    discount1 = di1 * ((annual_ongoing_costs + depreciation_charge_UDDT
                        + depreciation_charge_tank) * (1 - income_tax) - depreciation_charge_UDDT
                       - depreciation_charge_tank)

    discount2 = di2 * ((annual_ongoing_costs + depreciation_charge_UDDT
                        + depreciation_charge_tank) * (1 - income_tax) - depreciation_charge_UDDT
                       - depreciation_charge_tank)

    discount3 = di3 * ((annual_ongoing_costs + depreciation_charge_UDDT
                        + depreciation_charge_tank) * (1 - income_tax) - depreciation_charge_UDDT
                       - depreciation_charge_tank)

    discount4 = di4 * ((annual_ongoing_costs_yr4 + depreciation_charge_UDDT
                        + depreciation_charge_tank) * (1 - income_tax) - depreciation_charge_UDDT
                       - depreciation_charge_tank)

    discount5 = di5 * ((annual_ongoing_costs + depreciation_charge_UDDT
                        + depreciation_charge_tank) * (1 - income_tax) - depreciation_charge_UDDT
                       - depreciation_charge_tank)

    discount6 = di6 * ((annual_ongoing_costs + depreciation_charge_UDDT
                        + depreciation_charge_tank) * (1 - income_tax) - depreciation_charge_UDDT
                       - depreciation_charge_tank)

    discount7 = di7 * ((annual_ongoing_costs + depreciation_charge_UDDT
                        + depreciation_charge_tank) * (1 - income_tax) - depreciation_charge_UDDT
                       - depreciation_charge_tank)

    discount8 = di8 * ((annual_ongoing_costs + depreciation_charge_UDDT
                        + depreciation_charge_tank) * (1 - income_tax) - depreciation_charge_UDDT
                       - depreciation_charge_tank)

    discount_total = discount1 + discount2 + discount3 + discount4 + discount5 + discount6 + discount7 + discount8

    # Calculations for Payment per kg of Nutrient

    annual_mass_nutrients = 365 * (UDDT_users * UDDT_qty) * (nutrients.N_rec_U_T_S_urine[i]
                                                             + nutrients.P_rec_U_T_S_urine[i]
                                                             + nutrients.K_rec_U_T_S_urine[i])  # (kg/year)

    discount_nutrient_calc1 = di1 * annual_mass_nutrients * (1 - income_tax)
    discount_nutrient_calc2 = di2 * annual_mass_nutrients * (1 - income_tax)
    discount_nutrient_calc3 = di3 * annual_mass_nutrients * (1 - income_tax)
    discount_nutrient_calc4 = di4 * annual_mass_nutrients * (1 - income_tax)
    discount_nutrient_calc5 = di5 * annual_mass_nutrients * (1 - income_tax)
    discount_nutrient_calc6 = di6 * annual_mass_nutrients * (1 - income_tax)
    discount_nutrient_calc7 = di7 * annual_mass_nutrients * (1 - income_tax)
    discount_nutrient_calc8 = di8 * annual_mass_nutrients * (1 - income_tax)

    discount_nutrient_calc_total = discount_nutrient_calc1 + discount_nutrient_calc2 + discount_nutrient_calc3 + \
        discount_nutrient_calc4 + discount_nutrient_calc5 + discount_nutrient_calc6 + \
        discount_nutrient_calc7 + discount_nutrient_calc8

    nutrient_payment = ((material_UDDT + labor_UDDT + material_tank + labor_tank) + discount_total)/discount_nutrient_calc_total

    output1 = pd.DataFrame([nutrient_payment])  # (USD/kg total nutrients)
    output1 = output1.transpose()
    break_even_scenario_FINAL = pd.concat([break_even_scenario_FINAL, output1]).reset_index(drop=True)

break_even_scenario_FINAL.to_excel(writer, sheet_name='break_even_total')

writer.save()
