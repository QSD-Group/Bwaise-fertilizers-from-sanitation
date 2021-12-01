# Title: Novel financing strategies to simultaneously advance development goals for sanitation and agriculture
# through nutrient recovery
# Author: Hannah A.C. Lohman
# Created: February 27, 2019
# Updated: February 27, 2019

# This script, per_capita_nutrients.py, calculates the nutrients (N, P, K) excreted in urine.
# This quantity is reported in kg nutrient (N, P, or K) per capita per year in urine.

# ~~~~~~~IMPORT DATA AND FILES NECESSARY~~~~~~~

import pandas as pd  # import pandas for matrix data manipulation

triangle_parameter = pd.read_excel('OUTPUT_uncertainty_ranges.xlsx', sheetname='RR_triangle')
uniform_parameter = pd.read_excel('OUTPUT_uncertainty_ranges.xlsx', sheetname='RR_uniform')
nutrient_rec_efficiency = pd.read_excel('OUTPUT_uncertainty_ranges.xlsx', sheetname='nutrient_recovery_efficiency')

# ~~~~~~~CONSTANTS~~~~~~~

N_runs = 10000

# ~~~~~~~CALCULATING PER CAPITA NUTRIENT EXCRETION IN URINE~~~~~~~

writer = pd.ExcelWriter('RESULTS_per_capita_nutrients.xlsx', engine='xlsxwriter')
nutrients_FINAL = pd.DataFrame()
UDDT_nutrients_FINAL = pd.DataFrame()
ALL_nutrients_FINAL = pd.DataFrame()

for i in range(N_runs):

    # Per capita food intake and food waste parameters
    e_cal = uniform_parameter.e_cal[i]  # (kcal/cap/d) annual caloric intake
    p_veg = uniform_parameter.p_veg[i]  # (g/cap/d) vegetable derived protein intake
    p_anim = uniform_parameter.p_anim[i]  # (g/cap/d) animal derived protein intake
    p_tot = p_veg + p_anim  # (g/cap/d) total protein intake
    loss_cons = triangle_parameter.loss_cons[i]  # fraction of food wasted due to consumption losses at household

    # Nutrient content in protein/calorie parameters
    N_prot = uniform_parameter.N_prot[i]  # fraction of N contained in total protein
    P_prot_v = triangle_parameter.P_prot_v[i]  # fraction of P contained in vegetable derived protein
    P_prot_a = triangle_parameter.P_prot_a[i]  # fraction of P contained in animal derived protein
    K_cal = uniform_parameter.K_cal[i]  # (kg K/kcal) potassium content relative to caloric intake

    # Fraction of nutrients excreted
    N_exc = uniform_parameter.N_exc[i]  # fraction of N excreted in urine and feces per intake
    P_exc = uniform_parameter.P_exc[i]  # fraction of P excreted in urine and feces per intake
    K_exc = uniform_parameter.K_exc[i]  # fraction of K excreted in urine and feces per intake

    # Fraction of nutrients in urine
    N_urine = triangle_parameter.N_urine[i]  # (%) percent of total nitrogen excreted in urine
    P_urine = triangle_parameter.P_urine[i]  # (%) percent of total phosphorus excreted in urine
    K_urine = triangle_parameter.K_urine[i]  # (%) percent of total potassium excreted in urine

    # Per capita nitrogen excreted in urine and feces
    N_exc_tot = (p_tot * N_prot * (1 - loss_cons) * N_exc)/1000  # (kg N/cap/d total)
    N_exc_urine = N_exc_tot * (N_urine / 100)  # (kg N/cap/d in urine)
    N_exc_feces = N_exc_tot - N_exc_urine  # (kg N/cap/d in feces)

    # Per capita phosphorus excreted in urine and feces
    P_exc_tot = (((P_prot_v * p_veg) + (P_prot_a * p_anim)) * (1 - loss_cons) * P_exc)/1000  # (kg P/cap/d total)
    P_exc_urine = P_exc_tot * (P_urine / 100)  # (kg P/cap/d in urine)
    P_exc_feces = P_exc_tot - P_exc_urine  # (kg P/cap/d in feces)

    # Per capita potassium excreted in urine and feces
    K_exc_tot = e_cal * K_cal * (1 - loss_cons) * K_exc  # (kg K/cap/d total)
    K_exc_urine = K_exc_tot * (K_urine / 100)  # (kg K/cap/d in urine)
    K_exc_feces = K_exc_tot - K_exc_urine  # (kg K/cap/d in feces)

    output = pd.DataFrame([N_exc_tot, N_exc_urine, N_exc_feces, P_exc_tot, P_exc_urine, P_exc_feces, K_exc_tot,
                           K_exc_urine, K_exc_feces])

    output = output.transpose()
    nutrients_FINAL = pd.concat([nutrients_FINAL, output]).reset_index(drop=True)

    # Accounting for Nutrient Losses in UDDT, Transport, and Storage

    N_rec_after_UDDT_tot = N_exc_tot * (nutrient_rec_efficiency.UDDT_N[i]/100)  # (kg N/cap/d)
    N_rec_after_UDDT_urine = N_exc_urine * (nutrient_rec_efficiency.UDDT_N[i]/100)  # (kg N/cap/d)
    N_rec_after_UDDT_feces = N_exc_feces * (nutrient_rec_efficiency.UDDT_N[i]/100)  # (kg N/cap/d)

    N_rec_UDDT_transport_storage_tot = N_rec_after_UDDT_tot * (1 - (nutrient_rec_efficiency.transport_N[i]/100)) \
                                       * (1 - (nutrient_rec_efficiency.storage_N[i]/100))  # (kg N/cap/d)
    N_rec_UDDT_transport_strange_urine = N_rec_after_UDDT_urine * (1 - (nutrient_rec_efficiency.transport_N[i]/100)) \
                                         * (1 - (nutrient_rec_efficiency.storage_N[i]/100))  # (kg N/cap/d)
    N_rec_UDDT_transport_storage_feces = N_rec_after_UDDT_feces * (1 - (nutrient_rec_efficiency.transport_N[i]/100)) \
                                         * (1 - (nutrient_rec_efficiency.storage_N[i]/100))  # (kg N/cap/d)

    P_rec_after_UDDT_tot = P_exc_tot * (nutrient_rec_efficiency.UDDT_P[i]/100)  # (kg P/cap/d)
    P_rec_after_UDDT_urine = P_exc_urine * (nutrient_rec_efficiency.UDDT_P[i]/100)  # (kg P/cap/d)
    P_rec_after_UDDT_feces = P_exc_feces * (nutrient_rec_efficiency.UDDT_P[i]/100)  # (kg P/cap/d)

    P_rec_UDDT_transport_storage_tot = P_rec_after_UDDT_tot * (1 - (nutrient_rec_efficiency.transport_P[i]/100)) \
                                       * (1 - (nutrient_rec_efficiency.storage_P[i]/100))  # (kg P/cap/d)
    P_rec_UDDT_transport_strange_urine = P_rec_after_UDDT_urine * (1 - (nutrient_rec_efficiency.transport_P[i]/100)) \
                                         * (1 - (nutrient_rec_efficiency.storage_P[i]/100))  # (kg P/cap/d)
    P_rec_UDDT_transport_storage_feces = P_rec_after_UDDT_feces * (1 - (nutrient_rec_efficiency.transport_P[i]/100)) \
                                         * (1 - (nutrient_rec_efficiency.storage_P[i]/100))  # (kg P/cap/d)

    K_rec_after_UDDT_tot = K_exc_tot * (nutrient_rec_efficiency.UDDT_K[i]/100)  # (kg K/cap/d)
    K_rec_after_UDDT_urine = K_exc_urine * (nutrient_rec_efficiency.UDDT_K[i]/100)  # (kg K/cap/d)
    K_rec_after_UDDT_feces = K_exc_feces * (nutrient_rec_efficiency.UDDT_K[i]/100)  # (kg K/cap/d)

    K_rec_UDDT_transport_storage_tot = K_rec_after_UDDT_tot * (1 - (nutrient_rec_efficiency.transport_K[i]/100)) \
                                       * (1 - (nutrient_rec_efficiency.storage_K[i]/100))  # (kg K/cap/d)
    K_rec_UDDT_transport_strange_urine = K_rec_after_UDDT_urine * (1 - (nutrient_rec_efficiency.transport_K[i]/100)) \
                                         * (1 - (nutrient_rec_efficiency.storage_K[i]/100))  # (kg K/cap/d)
    K_rec_UDDT_transport_storage_feces = K_rec_after_UDDT_feces * (1 - (nutrient_rec_efficiency.transport_K[i]/100)) \
                                         * (1 - (nutrient_rec_efficiency.storage_K[i]/100))  # (kg K/cap/d)

    output1 = pd.DataFrame([N_rec_after_UDDT_tot, N_rec_after_UDDT_urine, N_rec_after_UDDT_feces,
                            P_rec_after_UDDT_tot, P_rec_after_UDDT_urine, P_rec_after_UDDT_feces,
                            K_rec_after_UDDT_tot, K_rec_after_UDDT_urine, K_rec_after_UDDT_feces])

    output1 = output1.transpose()

    UDDT_nutrients_FINAL = pd.concat([UDDT_nutrients_FINAL, output1]).reset_index(drop=True)

    output2 = pd.DataFrame([N_rec_UDDT_transport_storage_tot, N_rec_UDDT_transport_strange_urine,
                            N_rec_UDDT_transport_storage_feces, P_rec_UDDT_transport_storage_tot,
                            P_rec_UDDT_transport_strange_urine, P_rec_UDDT_transport_storage_feces,
                            K_rec_UDDT_transport_storage_tot, K_rec_UDDT_transport_strange_urine,
                            K_rec_UDDT_transport_storage_feces])

    output2 = output2.transpose()

    ALL_nutrients_FINAL = pd.concat([ALL_nutrients_FINAL, output2]).reset_index(drop=True)

nutrients_FINAL.columns = ('N_exc_tot', 'N_exc_urine', 'N_exc_feces', 'P_exc_tot', 'P_exc_urine', 'P_exc_feces',
                           'K_exc_tot', 'K_exc_urine', 'K_exc_feces')
UDDT_nutrients_FINAL.columns = ('N_rec_UDDT_tot', 'N_rec_UDDT_urine', 'N_rec_UDDT_feces', 'P_rec_UDDT_tot',
                                'P_rec_UDDT_urine', 'P_rec_UDDT_feces', 'K_rec_UDDT_tot', 'K_rec_UDDT_urine',
                                'K_rec_UDDT_feces')
ALL_nutrients_FINAL.columns = ('N_rec_U_T_S_tot', 'N_rec_U_T_S_urine', 'N_rec_U_T_S_feces', 'P_rec_U_T_S_tot',
                               'P_rec_U_T_S_urine', 'P_rec_U_T_S_feces', 'K_rec_U_T_S_tot', 'K_rec_U_T_S_urine',
                               'K_rec_U_T_S_feces')

nutrients_FINAL.to_excel(writer, sheet_name='per_capita_nutrients')
UDDT_nutrients_FINAL.to_excel(writer, sheet_name='rec_nutrients_after_UDDT')
ALL_nutrients_FINAL.to_excel(writer, sheet_name='rec_nutrients_after_U_T_S')

writer.save()





