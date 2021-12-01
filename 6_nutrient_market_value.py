# Title: Novel financing strategies to simultaneously advance development goals for sanitation and agriculture
# through nutrient recovery
# Author: Hannah A.C. Lohman
# Created: September 27, 2018
# Updated: January 23, 2019

# This script, nutrient_market_value.py, calculates the nutrient market value for comparison (USD/kg nutrients) where
# nutrients include N, P, K

# ~~~~~~~IMPORT DATA AND FILES NECESSARY~~~~~~~

import pandas as pd  # import pandas for matrix data manipulation
nutrient_cost_input = pd.read_excel('OUTPUT_uncertainty_ranges.xlsx', sheetname='fertilizer_cost')

# ~~~~~~~CONSTANTS~~~~~~~

N_runs = 10000
currency_conversion = 3693.8  # UGX to USD conversion as of August 7, 2018
mass_sack = 50  # (kg) each fertilizer sack is 50 kg
P_P2O5 = 2.29  # (kg P2O5 per kg P)  phosphorus conversion factor
K_K2O = 1.2  # (kg K20 per kg P)  potassium conversion factor

# ~~~~~~~FERTILIZER MARKET VALUE CALCULATIONS~~~~~~~

nutrient_market_value_FINAL = pd.DataFrame()
writer1 = pd.ExcelWriter('OUTPUT_fertilizer_market_value.xlsx', engine='xlsxwriter')

for i in range(N_runs):

    # Nutrient Content in Fertilizers (eventually use uncertainty)

    urea_N_content = 0.46  # fraction of N in urea fertilizer
    CAN_N_content = 0.26  # fraction N in calcium ammonium nitrate (CAN) fertilizer
    SSP_P2O5_content = 0.20  # fraction P2O5 in single superphosphate (SSP) fertilizer
    TSP_P2O5_content = 0.46  # fraction P2O5 in triple superphosphate (TSP) fertilizer
    KCl_K_content = 0.60  # fraction K20 in potassium chloride (KCl) fertilizer

    # Fertilizer Costs per 50 kg sack (UGX/50-kg)

    nutrient_cost = nutrient_cost_input.iloc[i, :]
    nutrient_cost = pd.DataFrame([nutrient_cost])
    nutrient_cost = nutrient_cost.fillna(0)

    urea_cost = nutrient_cost.urea
    urea_cost = list(urea_cost)
    urea_cost = str(urea_cost)[1:-1]
    urea_cost = float(urea_cost)

    CAN_cost = nutrient_cost.calcium_ammonium_nitrate
    CAN_cost = list(CAN_cost)
    CAN_cost = str(CAN_cost)[1:-1]
    CAN_cost = float(CAN_cost)

    SSP_cost = nutrient_cost.single_superphosphate
    SSP_cost = list(SSP_cost)
    SSP_cost = str(SSP_cost)[1:-1]
    SSP_cost = float(SSP_cost)

    TSP_cost = nutrient_cost.triple_superphosphate
    TSP_cost = list(TSP_cost)
    TSP_cost = str(TSP_cost)[1:-1]
    TSP_cost = float(TSP_cost)

    KCl_cost = nutrient_cost.potassium_chloride
    KCl_cost = list(KCl_cost)
    KCl_cost = str(KCl_cost)[1:-1]
    KCl_cost = float(KCl_cost)

    # Nutrient (N,P,K) Cost Calculations for Market

    urea_N_cost = (urea_cost/currency_conversion)/urea_N_content/mass_sack  # cost in USD per kg N
    CAN_N_cost = (CAN_cost/currency_conversion)/CAN_N_content/mass_sack  # cost in USD per kg N
    SSP_P_cost = P_P2O5 * (SSP_cost/currency_conversion)/SSP_P2O5_content/mass_sack  # cost in USD per kg P
    TSP_P_cost = P_P2O5 * (TSP_cost/currency_conversion)/TSP_P2O5_content/mass_sack  # cost in USD per kg P
    KCl_K_cost = K_K2O * (KCl_cost/currency_conversion)/KCl_K_content/mass_sack  # cost in USD per kg K

    output = pd.DataFrame([urea_N_cost, CAN_N_cost, SSP_P_cost, TSP_P_cost, KCl_K_cost])
    output = output.transpose()

    nutrient_market_value_FINAL = pd.concat([nutrient_market_value_FINAL, output]).reset_index(drop=True)

nutrient_market_value_FINAL.columns = ['urea_N_cost', 'CAN_N_cost', 'SSP_P_cost', 'TSP_P_cost', 'KCl_K_cost']
nutrient_market_value_FINAL.to_excel(writer1)

writer1.save()

# ~~~~~~~NUTRIENT MARKET VALUE FOR COMPARISON (WEIGHTED)~~~~~~~

nutrient_market_value = pd.read_excel('OUTPUT_fertilizer_market_value.xlsx')
annual_recovered_nutrients = pd.read_excel('RESULTS_RR_costs_FilterReuse.xlsx', sheetname='nutrients_recovered')
writer2 = pd.ExcelWriter('RESULTS_weighted_fertilizer_market_value.xlsx')

# Weighted market value. Struvite, ion exchange, and K recovery nutrient recovery mix (N, P, K).
weighted_market_value_FINAL = pd.DataFrame()

for j in range(N_runs):
    annual_recovered_N = annual_recovered_nutrients.annual_N_recovery[j]  # (kg N per year)
    annual_recovered_P = annual_recovered_nutrients.annual_P_recovery[j]  # (kg P per year)
    annual_recovered_K = annual_recovered_nutrients.annual_K_recovery[j]  # (kg K per year)

    total_recovered_nutrients = annual_recovered_N + annual_recovered_P + annual_recovered_K  # (kg nutrients per year)

    N_ratio = annual_recovered_N/total_recovered_nutrients
    P_ratio = annual_recovered_P/total_recovered_nutrients
    K_ratio = annual_recovered_K/total_recovered_nutrients

    N_market_price = nutrient_market_value.CAN_N_cost[j]  # (USD per kg N)
    P_market_price = nutrient_market_value.SSP_P_cost[j]  # (USD per kg P)
    K_market_price = nutrient_market_value.KCl_K_cost[j]  # (USD per kg K)

    weighted_N_market_price = N_ratio * N_market_price  # (USD per fraction of kg N)
    weighted_P_market_price = P_ratio * P_market_price  # (USD per fraction of kg P)
    weighted_K_market_price = K_ratio * K_market_price  # (USD per fraction of kg K)

    total_weighted_market_price = weighted_N_market_price + weighted_P_market_price \
                                  + weighted_K_market_price  # (USD per kg nutrients)

    output2 = pd.DataFrame([weighted_N_market_price, weighted_P_market_price, weighted_K_market_price,
                            total_weighted_market_price])
    output2 = output2.transpose()

    weighted_market_value_FINAL = pd.concat([weighted_market_value_FINAL, output2]).reset_index(drop=True)

weighted_market_value_FINAL.columns = ['weighted_N', 'weighted_P', 'weighted_K', 'weighted_total']
weighted_market_value_FINAL.to_excel(writer2, sheet_name='N_P_K_weighted_market_value')
