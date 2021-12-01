# Title: Novel financing strategies to simultaneously advance development goals for sanitation and agriculture
# through nutrient recovery
# Author: Hannah A.C. Lohman
# Created: February 26, 2019
# Updated: March 4, 2019

# This script, resource_recovery_cost.py, calculates the cost of each downstream nutrient recovery process:
# (1) phosphorus recovery through struvite precipitation, (2) nitrogen recovery through ion exchange, and
# (3) potassium recovery by reuse of resulting waste stream (K remains in liquid). The calculations are for one year
# of treatment.

# ~~~~~~~IMPORT DATA AND FILES NECESSARY~~~~~~~

import pandas as pd  # import pandas for matrix data manipulation
import numpy as np  # import NumPy library to use mathematical functions and preserve index information

general_parameters_triangle = pd.read_excel('OUTPUT_uncertainty_ranges.xlsx', sheetname='RR_triangle')
general_parameters_uniform = pd.read_excel('OUTPUT_uncertainty_ranges.xlsx', sheetname='RR_uniform')
P_recovery_parameters_uniform = pd.read_excel('OUTPUT_uncertainty_ranges.xlsx', sheetname='RR_P_recovery_uniform')
N_recovery_parameters_uniform = pd.read_excel('OUTPUT_uncertainty_ranges.xlsx', sheetname='RR_N_recovery_uniform')
N_recovery_parameters_triangle = pd.read_excel('OUTPUT_uncertainty_ranges.xlsx', sheetname='RR_N_recovery_triangle')
K_recovery_parameters_triangle = pd.read_excel('OUTPUT_uncertainty_ranges.xlsx', sheetname='RR_N_recovery_triangle')
per_capita_nutrients = pd.read_excel('RESULTS_per_capita_nutrients.xlsx', sheetname='rec_nutrients_after_U_T_S')
maint_cost_ratio = pd.read_excel('OUTPUT_uncertainty_ranges.xlsx', sheetname='maint_cost_ratio')
op_cost_ratio = pd.read_excel('OUTPUT_uncertainty_ranges.xlsx', sheetname='op_cost_ratio')
labor_cost_ratio = pd.read_excel('OUTPUT_uncertainty_ranges.xlsx', sheetname='labor_cost_ratio')
transport_costs = pd.read_excel('OUTPUT_uncertainty_ranges.xlsx', sheetname='transport_costs')

# ~~~~~~~CONSTANTS~~~~~~~

# General Constants
N_runs = 10000
usd_to_ugx = 3693.8  # UGX to USD conversion as of August 7, 2018
l_to_m3 = 1000  # 1000 L in 1 m^3
km_to_mi = 1.60934  # 1.60934 km in 1 mile
reference_flow = 1000  # Number of UDDTs assumed to be 1,000 (or 500 of the modeled units)
UDDT_users = 20  # UNHCR assumes 20 users per UDDT and modeled unit is 2 UDDTs combined
t_urine_storage = 3  # (days) Assume 3 day storage time in 1000 L tanks before emptied and trucked to treatment plant

# Phosphorus Recovery Constants (Struvite)
Mg_dose = 1.1  # (mol Mg per mol P) Mg:P ratio is 1.1 mol Mg per mol P
P_rec_1 = 0.90  # (%) Percent of phosphorus recovered as struvite; N_rec_1 will be calculated with stoichiometry
K_rec_1 = 0  # (%) Percent of potassium recovered as struvite; Value is zero because no K is recovered
t_treatment_cycle = 1  # (hr) Duration of a treatment cycle e.g. time liquid is in reactor
cycles_per_day = 8  # (d^-1) Assume an 8 hour work day and that 8 cycles can be completed in 1 day
reactor_volume = 500  # (L) Volume of a single stainless steel tank with tapered bottom used as reactor
required_filter_bag_area = 1  # (m^2) Area of required nylon filter bag by design
actual_filer_bag_area = 0.5  # (m^2) Area of selected filter bag (will need 2 filter bags to meet design requirement)
MW_MgOH2 = 58.3197  # (g Mg(OH)2 per mol Mg(OH)2) molecular weight of magnesium hydroxide
MW_MgCO3 = 84.3139  # (g MgCO3 per mol MgCO3) molecular weight of magnesium carbonate
MW_Mg = 24.305  # (g Mg per mol Mg) molecular weight of magnesium
MW_P = 30.973762  # (g P per mol P) molecular weight of phosphorus
MW_N = 14.01  # (g N per mol N) molecular weight of nitrogen
N_P_ratio_struvite = 1  # (mol N per mol P in struvite) N:P ratio in struvite
Mg_MgOH2_ratio = 1  # (mol Mg per mol Mg(OH)2) molar ratio of Mg to Mg(OH)2
Mg_MgCO3_ratio = 1  # (mol Mg per mol MgCO3) molar ratio of Mg to MgCO3

# Nitrogen Recovery Constants (Ion Exchange)
P_rec_2 = 0  # (%) Percent of phosphorus recovered during ion exchange; Value is zero because no P is recovered
K_rec_2 = 0  # (%) Percent of potassium recovered during ion exchange; Value is zero because no K is recovered
column_loading = 100  # (L/day) Daily loading rate of a single ion exchange column
column_length = 15.7/12  # (ft) column length is 15.7 inches and divide by 12 to convert to ft
U_regenerant = 0.000135  # (L/(g resin * cycle)) 98% H2SO4 regenerant volume
density_H2SO4 = 1  # (kg/L)  assume density of water

# Potassium Recovery Constants (Remaining Fluid)
P_rec_3 = 0  # (%) Percent of phosphorus recovered during potassium recovery; Value is zero because no P is recovered
N_rec_3 = 0  # (%) Percent of nitrogen recovered during potassium recovery; Value is zero because no N is recovered

# ~~~~~~~COST CALCULATIONS~~~~~~~
writer = pd.ExcelWriter('RESULTS_RR_costs_FilterReuse.xlsx', engine='xlsxwriter')
nutrients_recovered_FINAL = pd.DataFrame()
cap_cost_FINAL = pd.DataFrame()
labor_cost_FINAL = pd.DataFrame()
op_cost_FINAL = pd.DataFrame()
maint_cost_FINAL = pd.DataFrame()
struvite_cost_FINAL = pd.DataFrame()
ion_exchange_cost_FINAL = pd.DataFrame()

for i in range(N_runs):

    # ~~~~~~~Off Site Urine Storage Tank Calculations~~~~~~~

    urine_volume = general_parameters_triangle.urine_volume[i]  # (L/cap/d) daily volume of urine produced per capita
    daily_urine_volume = urine_volume * UDDT_users * reference_flow  # (L/d) total urine volume of reference flow
    total_tank_volume_L = UDDT_users * reference_flow * ((0.33 * 1 * urine_volume) + (0.33 * 2 * urine_volume) +
        (0.33 * 3 * urine_volume))  # (L) assume tank emptied every 3 days
    number_of_tanks = total_tank_volume_L/1000  # total number of 1000 L tanks for 1,000 UDDTs serving 20 people each
    number_of_tanks = np.ceil(number_of_tanks)  # round the number of tanks up to the nearest whole number
    number_of_urine_tanks1 = number_of_tanks  # total number of storage tanks in community

    cost_urine_tank1 = general_parameters_uniform.cost_urine_tank1[i]  # (USD/tank) cost of 1,000 L tank
    cap_cost_storage_tanks1 = number_of_urine_tanks1 * cost_urine_tank1

    # ~~~~~~~Urine Transport Calculations~~~~~~~

    cart_transport_cost = reference_flow * UDDT_users * transport_costs.cart[i]  # (USD/d)
    annual_cart_cost = cart_transport_cost * 365  # (USD/yr)

    truck_transport_cost = (daily_urine_volume/1000) * (transport_costs.truck[i]/usd_to_ugx)  # (USD/d)
    annual_truck_cost = truck_transport_cost * 365  # (USD/yr)

    # ~~~~~~~On Site Urine Storage Tanks~~~~~~~
    total_tank2_volume_L = daily_urine_volume  # (L/d) volume of a day's worth of urine
    number_of_urine_tanks2 = total_tank2_volume_L/1000  # total number of 1000 L urine storage tanks at facility
    number_of_urine_tanks2 = np.ceil(number_of_urine_tanks2)
    cost_urine_tank2 = general_parameters_uniform.cost_urine_tank2[i]
    cap_cost_storage_tanks2 = number_of_urine_tanks2 * cost_urine_tank2

    # ~~~~~~~Struvite Precipitation Calculations~~~~~~~

    # Nutrient recovery %
    N_influent1 = per_capita_nutrients.N_rec_U_T_S_urine[i] * reference_flow * UDDT_users  # (kg N/d) total N in system
    P_influent1 = per_capita_nutrients.P_rec_U_T_S_urine[i] * reference_flow * UDDT_users  # (kg P/d) total P in system
    K_influent1 = per_capita_nutrients.K_rec_U_T_S_urine[i] * reference_flow * UDDT_users  # (kg K/d) total K in system

    N_recovered1 = P_rec_1 * P_influent1 * (1 / MW_P) * N_P_ratio_struvite * MW_N  # (kg N/d) total N recovered
    P_recovered1 = P_rec_1 * P_influent1  # (kg P/d) total P recovered
    K_recovered1 = K_rec_1 * K_influent1  # (kg K/d) total K recovered

    N_effluent1 = N_influent1 - N_recovered1  # (kg N/d) total nitrogen left in waste stream
    P_effluent1 = P_influent1 - P_recovered1  # (kg P/d) total phosphorus left in waste stream
    K_effluent1 = K_influent1 - K_recovered1  # (kg K/d) total potassium left in waste stream

    N_rec_1 = 100 * (N_recovered1/N_influent1)  # (%) recovery percentage of nitrogen

    # Precipitation reactor
    cost_P_reactor = P_recovery_parameters_uniform.cost_P_reactor[i]  # (USD) cost of a precipitation reactor
    number_of_P_reactors = total_tank2_volume_L / cycles_per_day / reactor_volume  # number of struvite precip. reactors
    number_of_P_reactors = np.ceil(number_of_P_reactors)  # round number of reactors up to the nearest whole number
    cap_cost_P_reactors = number_of_P_reactors * cost_P_reactor  # (USD) total cost of all reactors at treatment facility

    # Reactor stirrer
    cap_cost_P_stirrers = number_of_P_reactors * P_recovery_parameters_uniform.material_P_stirrer[i] * \
                        (P_recovery_parameters_uniform.cost_P_stirrer[i]/usd_to_ugx) # (USD) total cost of all stirrers
    #  Note: cost_P_stirrer was originally in form of UGX/m2, this is why a conversion to USD is needed

    # Reactor pipes
    cap_cost_P_pipe = number_of_P_reactors * P_recovery_parameters_uniform.material_P_pipe[i] * \
                      P_recovery_parameters_uniform.cost_P_pipe[i]  # (USD) total cost of pipe for all reactors

    # Consumable: Filter bags
    filter_reuse = P_recovery_parameters_uniform.filter_reuse[i]  # number of times the filter can be reused
    daily_qty_filter_bags = number_of_P_reactors * cycles_per_day / filter_reuse
    cons_daily_filter_bag_cost = daily_qty_filter_bags * (P_recovery_parameters_uniform.cost_filter_bag[i]/20)
    # (USD/d) daily cost of filter bags, assuming bags cannot be reused and 8 cycles per day
    # Note: filter bags are priced per 20 bags, this is why the cost is divided by 20
    annual_qty_filter_bags = daily_qty_filter_bags * 365
    cons_annual_filter_bag_cost = cons_daily_filter_bag_cost * 365  # (USD/yr)  annual filter bag cost

    # Consumable: Magnesium source

    daily_MgOH2_dose = P_influent1 * (1/MW_P) * (1/Mg_dose) * Mg_MgOH2_ratio * MW_MgOH2  # (kg Mg(OH)2 per day)
    annual_MgOH2_dose = daily_MgOH2_dose * 365  # (kg Mg(OH)2 per year) annual dose of Mg(OH)2

    cons_daily_MgOH2_cost = daily_MgOH2_dose * (P_recovery_parameters_uniform.cost_MgOH2_powder[i]/1000)  # (USD/d)
    # Note: Mg(OH)2 powder is priced in USD per metric ton, this is why the cost is divided by 1000
    cons_annual_MgOH2_cost = cons_daily_MgOH2_cost * 365  # (USD/yr)

    daily_MgCO3_dose = P_influent1 * (1/MW_P) * (1/Mg_dose) * Mg_MgCO3_ratio * MW_MgCO3  # (kg MgCO3 per day)
    annual_MgCO3_dose = daily_MgCO3_dose * 365  # (kg MgCO3 per year) annual dose of MgCO3

    cons_daily_MgCO3_cost = daily_MgCO3_dose * (P_recovery_parameters_uniform.cost_MgCO3_powder[i]/1000)  # (USD/d)
    # Note: MgCO3 powder is priced in USD per metric ton, this is why the cost is divided by 1000
    cons_annual_MgCO3_cost = cons_daily_MgCO3_cost * 365  # (USD/yr)

    # ~~~~~~~Ion Exchange Calculations~~~~~~~

    # Nutrient Recovery %

    N_influent2 = N_effluent1  # (kg N/d) total nitrogen in influent to ion exchange process
    P_influent2 = P_effluent1  # (kg P/d) total phosphorus in influent to ion exchange process
    K_influent2 = K_effluent1  # (kg K/d) total potassium in influent to ion exchange process

    N_recovered2 = (N_recovery_parameters_uniform.N_rec_2[i]/100) * N_influent2  # (kg N/d) total N recovered
    P_recovered2 = (P_rec_2/100) * P_influent2  # (kg P/d) total P recovered
    K_recovered2 = (K_rec_2/100) * K_influent2  # (kg K/d) total K recovered

    N_effluent2 = N_influent2 - N_recovered2  # (kg N/d) total N left in waste stream after ion exchange
    P_effluent2 = P_influent2 - P_recovered2  # (kg P/d) total P left in waste stream after ion exchange
    K_effluent2 = K_influent2 - K_recovered2  # (kg K/d) total K left in waste stream after ion exchange

    # Ion Exchange Column
    # (USD) cap_cost_columns is the total cost of all ion exchange columns (including PVC pipe and tubing)

    qty_columns = total_tank2_volume_L/column_loading  # number of ion exchange columns needed
    qty_columns = np.ceil(qty_columns)
    cap_cost_columns = qty_columns * (N_recovery_parameters_uniform.cost_PVC_column[i] * column_length +
                                      N_recovery_parameters_uniform.material_tubing[i] *
                                      N_recovery_parameters_uniform.cost_tubing[i])

    # Consumable: Adsorbent/Resin

    cost_resin = N_recovery_parameters_uniform.cost_resin[i]  # (USD/kg) unit cost of resin
    N_concentration = N_influent2 / daily_urine_volume * 1000  # (g N/L urine) nitrogen concentration
    N = N_recovery_parameters_triangle.resin_lifetime[i]  # number of resin uses before replacement
    N = np.ceil(N)  # rounding number of uses up to the nearest whole number
    q0 = N_recovery_parameters_triangle.ad_density[i]  # (mmol N/g resin) adsorption density of resin

    cons_cost_resin = (cost_resin * N_concentration * 1000)/(N * q0 * MW_N)  # (USD/m3 urine) cost of resin per m3
    cons_daily_cost_resin = (cons_cost_resin/1000) * daily_urine_volume  # (USD/d) cost of resin per day
    # Note: cons_cost_resin was in USD/m3 and daily urine volumne is in L/d, so divide by 1000 to convert to L
    cons_annual_cost_resin = cons_daily_cost_resin * 365  # (USD/yr) annual cost of resin

    # Consumable: Regenerant, 98% H2SO4

    cost_H2SO4 = N_recovery_parameters_uniform.cost_H2SO4[i]  # (USD/metric ton) unit cost of H2SO4
    cost_H2SO4 = cost_H2SO4/1000  # (USD/L)  unit cost of H2SO4, assume density of water 1000 L 1000 kg = 1 metric ton

    cons_cost_H2SO4 = (cost_H2SO4 * U_regenerant * N_concentration * 1000 * 1000)/(q0 * MW_N)  # (USD/m3 urine)

    cons_daily_cost_H2SO4 = (cons_cost_H2SO4/1000) * daily_urine_volume  # (USD/d) cost of H2SO4 per day
    # Note: cons_cost_H2SO4 was in USD/m3 and daily urine volume is in L/d, so divide by 1000 to convert to L
    cons_annual_cost_H2SO4 = cons_daily_cost_H2SO4 * 365  # (USD/yr) annual cost of H2SO4

    # ~~~~~~~Total Capital Cost Calculations~~~~~~~

    total_cap_cost_off_site_tanks = cap_cost_storage_tanks1  # (USD) total capital cost of off site storage tanks
    total_cap_cost_on_site_tanks = cap_cost_storage_tanks2  # (USD) total capital cost of on site storage tanks
    total_cap_cost_struvite = cap_cost_P_reactors + cap_cost_P_stirrers + cap_cost_P_pipe  # (USD)
    total_cap_cost_ion_exchange = cap_cost_columns  # (USD) total capital cost of ion exchange columns

    # ~~~~~~~Labor Calculations~~~~~~~
    # This calculation considers the cost of construction labor
    labor_cost_off_site_tanks = labor_cost_ratio.tank[i] * total_cap_cost_off_site_tanks  # (USD)
    labor_cost_on_site_tanks = labor_cost_ratio.tank[i] * total_cap_cost_on_site_tanks  # (USD)
    labor_cost_struvite = labor_cost_ratio.struvite[i] * total_cap_cost_struvite  # (USD)
    labor_cost_ion_exchange = labor_cost_ratio.ion_exchange[i] * total_cap_cost_ion_exchange  # (USD)

    # ~~~~~~~Operation Calculations~~~~~~~
    # This calculated value is an annual operation cost (includes labor for operation)
    op_cost_off_site_tanks = op_cost_ratio.tank[i] * total_cap_cost_off_site_tanks  # (USD)
    op_cost_on_site_tanks = op_cost_ratio.tank[i] * total_cap_cost_on_site_tanks  # (USD)
    op_cost_struvite = op_cost_ratio.struvite[i] * total_cap_cost_struvite  # (USD)
    op_cost_ion_exchange = op_cost_ratio.ion_exchange[i] * total_cap_cost_ion_exchange  # (USD)

    # ~~~~~~~Maintenance Calculations~~~~~~~
    # This calculation is a maintenance cost that occurs at half of the system lifetime (~4 years)

    maint_cost_off_site_tanks = maint_cost_ratio.tank[i] * total_cap_cost_off_site_tanks  # (USD)
    maint_cost_on_site_tanks = maint_cost_ratio.tank[i] * total_cap_cost_on_site_tanks  # (USD)
    maint_cost_struvite = maint_cost_ratio.struvite[i] * total_cap_cost_struvite  # (USD)
    maint_cost_ion_exchange = maint_cost_ratio.ion_exchange[i] * total_cap_cost_ion_exchange  # (USD)

    # ~~~~~~~Total Nutrients Recovered~~~~~~~

    annual_N_recovery = (N_influent1 - N_effluent2) * 365  # (kg N/yr) annual total N recovered
    annual_P_recovery = (P_influent1 - P_effluent2) * 365  # (kg P/yr) annual total P recovered
    annual_K_recovery = K_effluent2 * 365  # (kg K/yr) annual total K recovered

    # ~~~~~~~Output Values to Excel~~~~~~~

    # Recovered Nutrients
    output1 = pd.DataFrame([N_influent1, P_influent1, K_influent1, N_influent2, P_influent2, K_influent2,
                            annual_N_recovery, annual_P_recovery, annual_K_recovery])
    output1 = output1.transpose()
    nutrients_recovered_FINAL = pd.concat([nutrients_recovered_FINAL, output1]).reset_index(drop=True)

    # Capital Cost
    output2 = pd.DataFrame([total_cap_cost_off_site_tanks, total_cap_cost_on_site_tanks, total_cap_cost_struvite,
                            total_cap_cost_ion_exchange])
    output2 = output2.transpose()
    cap_cost_FINAL = pd.concat([cap_cost_FINAL, output2]).reset_index(drop=True)

    # Labor Cost
    output3 = pd.DataFrame([labor_cost_off_site_tanks, labor_cost_on_site_tanks, labor_cost_struvite,
                            labor_cost_ion_exchange])
    output3 = output3.transpose()
    labor_cost_FINAL = pd.concat([labor_cost_FINAL, output3]).reset_index(drop=True)

    # Operation Cost
    output4 = pd.DataFrame([op_cost_off_site_tanks, op_cost_on_site_tanks, op_cost_struvite,
                            op_cost_ion_exchange, annual_cart_cost, annual_truck_cost])
    output4 = output4.transpose()
    op_cost_FINAL = pd.concat([op_cost_FINAL, output4]).reset_index(drop=True)

    # Maintenance Cost
    output5 = pd.DataFrame([maint_cost_off_site_tanks, maint_cost_on_site_tanks, maint_cost_struvite,
                            maint_cost_ion_exchange])
    output5 = output5.transpose()
    maint_cost_FINAL = pd.concat([maint_cost_FINAL, output5]).reset_index(drop=True)

    # Detailed Struvite Cost
    output6 = pd.DataFrame([number_of_P_reactors, cap_cost_P_reactors, cap_cost_P_stirrers, cap_cost_P_pipe,
                            daily_qty_filter_bags, cons_daily_filter_bag_cost, annual_qty_filter_bags,
                            cons_annual_filter_bag_cost, daily_MgOH2_dose, cons_daily_MgOH2_cost, annual_MgOH2_dose,
                            cons_annual_MgOH2_cost, daily_MgCO3_dose, cons_daily_MgCO3_cost, annual_MgCO3_dose,
                            cons_annual_MgCO3_cost])
    output6 = output6.transpose()
    struvite_cost_FINAL = pd.concat([struvite_cost_FINAL, output6]).reset_index(drop=True)

    # Detailed Ion Exchange Cost
    output7 = pd.DataFrame([qty_columns, cap_cost_columns, cons_daily_cost_resin, cons_annual_cost_resin,
                            cons_daily_cost_H2SO4, cons_annual_cost_H2SO4])
    output7 = output7.transpose()
    ion_exchange_cost_FINAL = pd.concat([ion_exchange_cost_FINAL, output7]).reset_index(drop=True)

nutrients_recovered_FINAL.columns = ('N_influent1', 'P_influent1', 'K_influent1', 'N_influent2', 'P_influent2',
                                     'K_influent2', 'annual_N_recovery', 'annual_P_recovery', 'annual_K_recovery')
nutrients_recovered_FINAL.to_excel(writer, sheet_name='nutrients_recovered')

cap_cost_FINAL.columns = ('total_cap_cost_off_site_tanks', 'total_cap_cost_on_site_tanks', 'total_cap_cost_struvite',
                          'total_cap_cost_ion_exchange')
cap_cost_FINAL.to_excel(writer, sheet_name='capital_cost')

labor_cost_FINAL.columns = ('labor_cost_off_site_tanks', 'labor_cost_on_site_tanks', 'labor_cost_struvite',
                            'labor_cost_ion_exchange')
labor_cost_FINAL.to_excel(writer, sheet_name='labor_cost')

op_cost_FINAL.columns = ('op_cost_off_site_tanks', 'op_cost_on_site_tanks', 'op_cost_struvite',
                         'op_cost_ion_exchange', 'annual_cart_cost', 'annual_truck_cost')
op_cost_FINAL.to_excel(writer, sheet_name='op_cost')

maint_cost_FINAL.columns = ('maint_cost_off_site_tanks', 'maint_cost_on_site_tanks', 'maint_cost_struvite',
                            'maint_cost_ion_exchange')
maint_cost_FINAL.to_excel(writer, sheet_name='maint_cost')

struvite_cost_FINAL.columns = ('number_of_P_reactors', 'cap_cost_P_reactors', 'cap_cost_P_stirrers', 'cap_cost_P_pipe',
                               'daily_qty_filter_bags', 'cons_daily_filter_bag_cost', 'annual_qty_filter_bags',
                               'cons_annual_filter_bag_cost', 'daily_MgOH2_dose', 'cons_daily_MgOH2_cost',
                               'annual_MgOH2_dose', 'cons_annual_MgOH2_cost', 'daily_MgCO3_dose',
                               'cons_daily_MgCO3_cost', 'annual_MgCO3_dose', 'cons_annual_MgCO3_cost')
struvite_cost_FINAL.to_excel(writer, sheet_name='struvite_cost')

ion_exchange_cost_FINAL.columns = ('qty_columns', 'cap_cost_columns', 'cons_daily_cost_resin', 'cons_annual_cost_resin',
                                   'cons_daily_cost_H2SO4', 'cons_annual_cost_H2SO4')
ion_exchange_cost_FINAL.to_excel(writer, sheet_name='ion_exchange_cost')

writer.save()
