# Title: Novel financing strategies to simultaneously advance development goals for sanitation and agriculture
# through nutrient recovery
# Author: Hannah A.C. Lohman
# Created: August 27, 2018
# Updated: April 9, 2019

# This script, DCA_break_even_scenario_subsidized.py, calculates the break even resource payment necessary to
# incentivize urine diversion dry toilet construction and urine treatment (assuming pit latrine payment from aid agency)

# ~~~~~~~IMPORT DATA AND FILES NECESSARY~~~~~~~

import pandas as pd  # import pandas for matrix data manipulation
import numpy as np

UDDT_pit_cost = pd.read_excel('RESULTS_UDDT_pit_costs.xlsx')  # import costs related to pit latrine and UDDT (USD)
RR_material_cost = pd.read_excel('RESULTS_RR_costs_FilterReuse.xlsx', sheetname='capital_cost')  # material costs (USD)
RR_labor_cost = pd.read_excel('RESULTS_RR_costs_FilterReuse.xlsx', sheetname='labor_cost')  # labor costs for treatment (USD)
RR_op_cost = pd.read_excel('RESULTS_RR_costs_FilterReuse.xlsx', sheetname='op_cost')  # operation costs for treatment (USD)
RR_maint_cost = pd.read_excel('RESULTS_RR_costs_FilterReuse.xlsx', sheetname='maint_cost')  # maint costs for treatment (USD)
RR_struvite_consumable_cost = pd.read_excel('RESULTS_RR_costs_FilterReuse.xlsx', sheetname='struvite_cost')  # struvite costs (USD)
RR_ion_exchange_consumable_cost = pd.read_excel('RESULTS_RR_costs_FilterReuse.xlsx', sheetname='ion_exchange_cost')  # (USD)
qty_tanks = pd.read_excel('RESULTS_tank_quantity.xlsx', sheetname='advanced_tanks')
land_cost = pd.read_excel('OUTPUT_uncertainty_ranges.xlsx', sheetname='RR_uniform')

DCA_parameters = pd.read_excel('OUTPUT_uncertainty_ranges.xlsx', sheetname='DCA_parameters')  # tax and discount rates
recovered_nutrients = pd.read_excel('RESULTS_RR_costs_FilterReuse.xlsx', sheetname='nutrients_recovered')  # (kg/yr) total nutrients
# recovered at the end of the treatment cycle for 20,000 people

# ~~~~~~~CONSTANTS~~~~~~~

N_runs = 10000
UDDT_users = 40  # (people) number of people using a UDDT unit (with 2 toilets)
UDDT_qty = 500  # assume 1,000 toilets and UDDT has 2 per unit
pit_qty = 500  # assume 1,000 toilets and pit has 1 per unit
UDDT_lifetime = 8  # (years) can eventually vary
pit_lifetime = 8  # (years) can eventually vary
on_site_tank_lifetime = 8  # (years) can eventually vary
off_site_tank_lifetime = 8  # (years) can eventually vary
struvite_lifetime = 8  # (years) can eventually vary
ion_exchange_lifetime = 8  # (years) can eventually vary
currency_conversion = 3693.8  # UGX to USD conversion as of August 7, 2018
tanks_per_land = 154  # number of tanks per 50'x100' plot of land

# ~~~~~~~BREAK EVEN IN 8 YEARS CALCULATION~~~~~~~

# positive costs indicate a cost to the contractor/NGO and negative costs indicate a payment to the contractor/NGO

writer1 = pd.ExcelWriter('RESULTS_break_even_Scenario2_subsidized_July31.xlsx', engine='xlsxwriter')
break_even_scenario_FINAL = pd.DataFrame()

writer2 = pd.ExcelWriter('RESULTS_cap_op_cons_maint_costs_FilterReuse_July31.xlsx', engine='xlsxwriter')
material_cost_FINAL = pd.DataFrame()
labor_cost_FINAL = pd.DataFrame()
op_cost_FINAL = pd.DataFrame()
cons_cost_FINAL = pd.DataFrame()
maint_cost_FINAL = pd.DataFrame()

for i in range(N_runs):

    # Income Tax Rate and Discount Rate

    income_tax = DCA_parameters.income_tax[i]  # (no unit) income tax rate in decimal form
    discount_rate = DCA_parameters.discount_rate[i]  # (no unit) discount rate in decimal form

    # Capital Costs (Total to Treat 20,000 People Reference Flow)

    material_pit = UDDT_pit_cost.cap_pit[i] * pit_qty  # (USD) total material cost of 1,000 pit latrine units
    material_UDDT = UDDT_pit_cost.cap_UDDT[i] * UDDT_qty  # (USD) total material cost of 500 UDDT units
    material_off_site_tanks = RR_material_cost.total_cap_cost_off_site_tanks[i]  # (USD) total material cost tanks
    material_on_site_tanks = RR_material_cost.total_cap_cost_on_site_tanks[i]  # (USD) total material cost tanks
    material_struvite = RR_material_cost.total_cap_cost_struvite[i]  # (USD) total struvite capital costs
    material_ion_exchange = RR_material_cost.total_cap_cost_ion_exchange[i]  # (USD) total ion exchange capital costs

    labor_pit = UDDT_pit_cost.labor_pit[i] * pit_qty  # (USD) total construction labor cost of 1,000 pit latrine units
    labor_UDDT = UDDT_pit_cost.labor_UDDT[i] * UDDT_qty  # (USD) total construction labor cost of 500 UDDT units
    labor_off_site_tanks = RR_labor_cost.labor_cost_off_site_tanks[i]  # (USD) total construction labor cost tanks
    labor_on_site_tanks = RR_labor_cost.labor_cost_on_site_tanks[i]  # (USD) total construction labor cost tanks
    labor_struvite = RR_labor_cost.labor_cost_struvite[i]  # (USD) total struvite construction labor costs
    labor_ion_exchange = RR_labor_cost.labor_cost_ion_exchange[i]  # (USD) total ion exchange construction labor costs

    # Ongoing Costs (Ei)

    # Operation Costs for Equipment/Capital
    annual_op_UDDT = UDDT_pit_cost.op_UDDT[i] * UDDT_qty  # (USD/yr) annual operation cost of 500 UDDT units
    annual_op_off_site_tanks = RR_op_cost.op_cost_off_site_tanks[i]  # (USD/yr) annual op cost of off site tanks
    annual_op_on_site_tanks = RR_op_cost.op_cost_on_site_tanks[i]  # (USD/yr) annual op cost of on site tanks
    annual_op_cost_struvite = RR_op_cost.op_cost_struvite[i]  # (USD/yr) annual op cost of struvite capital
    annual_op_cost_ion_exchange = RR_op_cost.op_cost_ion_exchange[i]  # (USD/yr) annual op cost of ion exchange capital
    annual_op_TOTAL = annual_op_UDDT + annual_op_off_site_tanks + annual_op_on_site_tanks + annual_op_cost_struvite + \
        annual_op_cost_ion_exchange  # (USD/yr) total annual operation cost of capital

    # Land Costs for Off Site Tanks
    land_qty = qty_tanks.tanks[i]/tanks_per_land
    land_qty = np.ceil(land_qty)
    annual_land_cost = land_qty * land_cost.lease_50_100[i]

    # Annual Consumable Costs for Transportation & Struvite and Ion Exchange Processes
    annual_con_struvite_filter = RR_struvite_consumable_cost.cons_annual_filter_bag_cost[i]  # (USD/yr) filter bags
    annual_con_struvite_MgOH2 = RR_struvite_consumable_cost.cons_annual_MgOH2_cost[i]  # (USD/yr) Mg source cost
    annual_con_ion_exchange_H2SO4 = RR_ion_exchange_consumable_cost.cons_annual_cost_H2SO4[i]  # (USD/yr) H2SO4 cost
    annual_con_ion_exchange_resin = RR_ion_exchange_consumable_cost.cons_annual_cost_resin[i]  # (USD/yr) resin cost
    annual_con_TOTAL = annual_con_struvite_filter + annual_con_struvite_MgOH2 + annual_con_ion_exchange_H2SO4 \
        + annual_con_ion_exchange_resin  # (USD/yr)

    # Maintenance Costs for Equipment/Capital (Maintenance Occurs at 1/2 Lifetime)
    maint_UDDT = UDDT_pit_cost.maint_UDDT[i] * UDDT_qty  # (USD) maintenance (at 1/2 lifetime) cost of 500 UDDT units
    maint_off_site_tanks = RR_maint_cost.maint_cost_off_site_tanks[i]  # (USD) maintenance cost of tanks
    maint_on_site_tanks = RR_maint_cost.maint_cost_on_site_tanks[i]  # (USD) maintenance cost of tanks
    maint_struvite = RR_maint_cost.maint_cost_struvite[i]  # (USD) maintenance cost of struvite capital
    maint_ion_exchange = RR_maint_cost.maint_cost_ion_exchange[i]  # (USD) maintenance cost of ion exchange capital
    maint_TOTAL = maint_UDDT + maint_off_site_tanks + maint_on_site_tanks + maint_struvite + maint_ion_exchange  # (USD)

    annual_ongoing_costs = annual_op_TOTAL + annual_con_TOTAL + annual_land_cost  # (USD/yr) total op and consumables cost (different yr 4)
    annual_ongoing_costs_yr4 = annual_ongoing_costs + maint_TOTAL  # (USD/yr) total ongoing costs at year 4 with maint

    # Ongoing Aid Agency Payments to NGO/Contractor (Pi)

    annual_op_pit = -UDDT_pit_cost.op_pit[i] * pit_qty # (USD/yr) aid agency pays op costs of a pit latrine
    maint_pit = -UDDT_pit_cost.maint_pit[i] * pit_qty # (USD) aid agency pays maint costs of a pit latrine
    annual_ongoing_payments = annual_op_pit  # (USD/yr) (different in year 4)
    annual_ongoing_payments_yr4 = annual_ongoing_payments + maint_pit  # (USD/yr) total ongoing payments at year 4

    # Depreciation Charge (Di)

    depreciation_charge_UDDT = material_UDDT/UDDT_lifetime
    depreciation_charge_pit = -material_pit/pit_lifetime
    depreciation_charge_off_site_tanks = material_off_site_tanks/off_site_tank_lifetime
    depreciation_charge_on_site_tanks = material_on_site_tanks/on_site_tank_lifetime
    depreciation_charge_struvite = material_struvite/struvite_lifetime
    depreciation_charge_ion_exchange = material_ion_exchange/ion_exchange_lifetime

    # Discount Factor (di)

    di1 = 1/(1 + discount_rate)**1
    di2 = 1/(1 + discount_rate)**2
    di3 = 1/(1 + discount_rate)**3
    di4 = 1/(1 + discount_rate)**4
    di5 = 1/(1 + discount_rate)**5
    di6 = 1/(1 + discount_rate)**6
    di7 = 1/(1 + discount_rate)**7
    di8 = 1/(1 + discount_rate)**8

    discount1 = di1 * ((annual_ongoing_costs + annual_ongoing_payments + depreciation_charge_UDDT
                        + depreciation_charge_pit + depreciation_charge_off_site_tanks
                        + depreciation_charge_on_site_tanks + depreciation_charge_struvite
                        + depreciation_charge_ion_exchange) * (1 - income_tax) - depreciation_charge_UDDT
                       - depreciation_charge_pit - depreciation_charge_off_site_tanks
                       - depreciation_charge_on_site_tanks - depreciation_charge_struvite
                       - depreciation_charge_ion_exchange)

    discount2 = di2 * ((annual_ongoing_costs + annual_ongoing_payments + depreciation_charge_UDDT
                        + depreciation_charge_pit + depreciation_charge_off_site_tanks
                        + depreciation_charge_on_site_tanks + depreciation_charge_struvite
                        + depreciation_charge_ion_exchange) * (1 - income_tax) - depreciation_charge_UDDT
                       - depreciation_charge_pit - depreciation_charge_off_site_tanks
                       - depreciation_charge_on_site_tanks - depreciation_charge_struvite
                       - depreciation_charge_ion_exchange)

    discount3 = di3 * ((annual_ongoing_costs + annual_ongoing_payments + depreciation_charge_UDDT
                        + depreciation_charge_pit + depreciation_charge_off_site_tanks
                        + depreciation_charge_on_site_tanks + depreciation_charge_struvite
                        + depreciation_charge_ion_exchange) * (1 - income_tax) - depreciation_charge_UDDT
                       - depreciation_charge_pit - depreciation_charge_off_site_tanks
                       - depreciation_charge_on_site_tanks - depreciation_charge_struvite
                       - depreciation_charge_ion_exchange)

    discount4 = di4 * ((annual_ongoing_costs_yr4 + annual_ongoing_payments_yr4 + depreciation_charge_UDDT
                        + depreciation_charge_pit + depreciation_charge_off_site_tanks
                        + depreciation_charge_on_site_tanks + depreciation_charge_struvite
                        + depreciation_charge_ion_exchange) * (1 - income_tax) - depreciation_charge_UDDT
                       - depreciation_charge_pit - depreciation_charge_off_site_tanks
                       - depreciation_charge_on_site_tanks - depreciation_charge_struvite
                       - depreciation_charge_ion_exchange)

    discount5 = di5 * ((annual_ongoing_costs + annual_ongoing_payments + depreciation_charge_UDDT
                        + depreciation_charge_pit + depreciation_charge_off_site_tanks
                        + depreciation_charge_on_site_tanks + depreciation_charge_struvite
                        + depreciation_charge_ion_exchange) * (1 - income_tax) - depreciation_charge_UDDT
                       - depreciation_charge_pit - depreciation_charge_off_site_tanks
                       - depreciation_charge_on_site_tanks - depreciation_charge_struvite
                       - depreciation_charge_ion_exchange)

    discount6 = di6 * ((annual_ongoing_costs + annual_ongoing_payments + depreciation_charge_UDDT
                        + depreciation_charge_pit + depreciation_charge_off_site_tanks
                        + depreciation_charge_on_site_tanks + depreciation_charge_struvite
                        + depreciation_charge_ion_exchange) * (1 - income_tax) - depreciation_charge_UDDT
                       - depreciation_charge_pit - depreciation_charge_off_site_tanks
                       - depreciation_charge_on_site_tanks - depreciation_charge_struvite
                       - depreciation_charge_ion_exchange)

    discount7 = di7 * ((annual_ongoing_costs + annual_ongoing_payments + depreciation_charge_UDDT
                        + depreciation_charge_pit + depreciation_charge_off_site_tanks
                        + depreciation_charge_on_site_tanks + depreciation_charge_struvite
                        + depreciation_charge_ion_exchange) * (1 - income_tax) - depreciation_charge_UDDT
                       - depreciation_charge_pit - depreciation_charge_off_site_tanks
                       - depreciation_charge_on_site_tanks - depreciation_charge_struvite
                       - depreciation_charge_ion_exchange)

    discount8 = di8 * ((annual_ongoing_costs + annual_ongoing_payments + depreciation_charge_UDDT
                        + depreciation_charge_pit + depreciation_charge_off_site_tanks
                        + depreciation_charge_on_site_tanks + depreciation_charge_struvite
                        + depreciation_charge_ion_exchange) * (1 - income_tax) - depreciation_charge_UDDT
                       - depreciation_charge_pit - depreciation_charge_off_site_tanks
                       - depreciation_charge_on_site_tanks - depreciation_charge_struvite
                       - depreciation_charge_ion_exchange)

    discount_total = discount1 + discount2 + discount3 + discount4 + discount5 + discount6 + discount7 + discount8

    # Calculations for Payment per kg of Nutrient

    annual_mass_nutrients = recovered_nutrients.annual_N_recovery[i] + recovered_nutrients.annual_P_recovery[i] \
        + recovered_nutrients.annual_K_recovery[i]  # (kg/year) total nutrients recovered in year

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

    nutrient_payment = ((material_UDDT + labor_UDDT + material_off_site_tanks + labor_off_site_tanks
                         + material_on_site_tanks + labor_on_site_tanks + material_struvite + labor_struvite
                         + material_ion_exchange + labor_ion_exchange - material_pit - labor_pit)
                         + discount_total)/discount_nutrient_calc_total

    output1 = pd.DataFrame([nutrient_payment])  # (USD/kg total nutrients)
    output1 = output1.transpose()
    break_even_scenario_FINAL = pd.concat([break_even_scenario_FINAL, output1]).reset_index(drop=True)

    output2 = pd.DataFrame([material_pit, material_UDDT, material_off_site_tanks, material_on_site_tanks,
                            material_struvite, material_ion_exchange])
    output2 = output2.transpose()
    material_cost_FINAL = pd.concat([material_cost_FINAL, output2]).reset_index(drop=True)

    output3 = pd.DataFrame([labor_pit, labor_UDDT, labor_off_site_tanks, labor_on_site_tanks,
                            labor_struvite, labor_ion_exchange])
    output3 = output3.transpose()
    labor_cost_FINAL = pd.concat([labor_cost_FINAL, output3]).reset_index(drop=True)

    output4 = pd.DataFrame([-annual_op_pit, annual_op_UDDT, annual_op_off_site_tanks, annual_op_on_site_tanks,
                            annual_op_cost_struvite, annual_op_cost_ion_exchange])
    output4 = output4.transpose()
    op_cost_FINAL = pd.concat([op_cost_FINAL, output4]).reset_index(drop=True)

    output5 = pd.DataFrame([annual_con_struvite_filter, annual_con_struvite_MgOH2,
                            annual_con_ion_exchange_resin, annual_con_ion_exchange_H2SO4])
    output5 = output5.transpose()
    cons_cost_FINAL = pd.concat([cons_cost_FINAL, output5]).reset_index(drop=True)

    output6 = pd.DataFrame([-maint_pit, maint_UDDT, maint_off_site_tanks, maint_on_site_tanks, maint_struvite,
                            maint_ion_exchange])
    output6 = output6.transpose()
    maint_cost_FINAL = pd.concat([maint_cost_FINAL, output6]).reset_index(drop=True)

material_cost_FINAL.columns = ('material_pit', 'material_UDDT', 'material_off_site_tanks', 'material_on_site_tanks',
                               'material_struvite', 'material_ion_exchange')

labor_cost_FINAL.columns = ('labor_pit', 'labor_UDDT', 'labor_off_site_tanks', 'labor_on_site_tanks', 'labor_struvite',
                            'labor_ion_exchange')

op_cost_FINAL.columns = ('annual_op_pit', 'annual_op_UDDT', 'annual_op_off_site_tanks', 'annual_op_on_site_tanks',
                         'annual_op_struvite', 'annual_op_ion_exchange')

cons_cost_FINAL.columns = ('annual_con_struvite_filter', 'annual_con_struvite_MgOH2', 'annual_con_ion_exchange_resin',
                           'annual_con_ion_exchange_H2SO4')

maint_cost_FINAL.columns = ('maint_pit', 'maint_UDDT', 'maint_off_site_tanks', 'maint_on_site_tanks', 'maint_struvite',
                            'maint_ion_exchange')

break_even_scenario_FINAL.to_excel(writer1, sheet_name='break_even_scenario')
material_cost_FINAL.to_excel(writer2, sheet_name='material')
labor_cost_FINAL.to_excel(writer2, sheet_name='labor')
op_cost_FINAL.to_excel(writer2, sheet_name='op')
cons_cost_FINAL.to_excel(writer2, sheet_name='consumable')
maint_cost_FINAL.to_excel(writer2, sheet_name='maint')

writer1.save()
writer2.save()
