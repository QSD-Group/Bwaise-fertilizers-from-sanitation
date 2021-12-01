# Title: Novel financing strategies to simultaneously advance development goals for sanitation and agriculture
# through nutrient recovery
# Author: Hannah A.C. Lohman
# Created: July 6, 2017
# Updated: March 11, 2019

# This script, capital_cost_UDDT_Pit.py, calculates the total cost to construct each technology (materials and construction
# labor) under uncertainty

# ~~~~~~~IMPORT DATA AND FILES NECESSARY~~~~~~~

import pandas as pd  # import pandas for matrix data manipulation

construction_material_quantities = pd.read_excel('input_data_file.xlsx', sheetname="material_quantities")
construction_material_unit_costs_UNCERTAINTY = pd.read_excel('OUTPUT_uncertainty_ranges.xlsx',
                                                             sheetname="material_unit_costs")

material_reuse = pd.read_excel('OUTPUT_uncertainty_ranges.xlsx', sheetname="material_reuse_ratio")
construction_material_reuse_quantities = pd.read_excel('input_data_file.xlsx', sheetname="reuse_quantities")

# ~~~~~~~CONSTANTS~~~~~~~

usd_to_ugx = 3693.8  # UGX to USD conversion as of August 7, 2018
N_runs = 10000

# ~~~~~~~CALCULATING MATERIAL COSTS FOR UDDT AND PIT LATRINE~~~~~~~

matrix_shape_cost = construction_material_unit_costs_UNCERTAINTY.shape  # [0]= number of rows and [1]= number of columns
writer0 = pd.ExcelWriter('RESULTS_UDDT_Pit_capital_costs.xlsx', engine='xlsxwriter')
intervention_material_cost_final = pd.DataFrame()

# dataframe for construction material quantities

for j in range(N_runs):
    matrix_shape = construction_material_quantities.shape  # [0] is number of rows and [1] is number of columns

    construction_material_unit_costs = construction_material_unit_costs_UNCERTAINTY.iloc[j, :]
    construction_material_unit_costs = pd.DataFrame([construction_material_unit_costs])
    construction_material_unit_costs.columns = [k for k in range(construction_material_unit_costs.shape[1])]
    construction_material_unit_costs = construction_material_unit_costs.transpose()
    construction_material_unit_costs = construction_material_unit_costs.fillna(0)

    material_reuse_ratio = material_reuse.iloc[j]
    material_reuse_ratio = list(material_reuse_ratio)
    material_reuse_ratio = str(material_reuse_ratio)[1:-1]
    material_reuse_ratio = float(material_reuse_ratio)

    material_reuse_ratio_ALL = []

    for p in range(0, matrix_shape[0]):
        ratio = material_reuse_ratio
        material_reuse_ratio_ALL.append(ratio)

    material_reuse_ratio_final = pd.DataFrame([material_reuse_ratio_ALL])
    material_reuse_ratio_final = material_reuse_ratio_final.transpose()

    # for loop calculates the sum-product of material quantities and unit costs for each intervention

    column_names = list(construction_material_quantities)  # call column names of construction material csv
    column_names = column_names[3:]  # indexing to select intervention names (ignore unit, material name, etc.)
    total_material_cost = []  # open matrix to store total material costs for each intervention scenario

    for i in range(3, matrix_shape[1]):  # index 3 is first location of intervention data

        materials_to_reuse = construction_material_reuse_quantities.iloc[0:matrix_shape[0], i]
        materials_to_reuse = pd.DataFrame([materials_to_reuse])
        materials_to_reuse = materials_to_reuse.transpose()
        materials_to_reuse.columns = [0]

        reuse_ratio_new = material_reuse_ratio_final.multiply(materials_to_reuse, axis='columns')
        reuse_ratio_new = reuse_ratio_new.fillna(1)

        material_quantity = construction_material_quantities.iloc[0:matrix_shape[0], i]
        material_quantity = pd.DataFrame([material_quantity])
        material_quantity = material_quantity.transpose()
        material_quantity.columns = [0]

        material_quantity_with_reuse = reuse_ratio_new.multiply(material_quantity, axis='columns')
        material_quantity_with_reuse.columns = [j]

        cost1 = construction_material_unit_costs.multiply(material_quantity_with_reuse, axis='columns')
        cost2 = cost1.sum()
        cost2 = list(cost2)
        cost2 = str(cost2)[1:-1]
        cost2 = float(cost2)

        total_material_cost.append(cost2)

    intervention_material_cost = pd.DataFrame([total_material_cost], columns=column_names)
    intervention_material_cost_final = pd.concat([intervention_material_cost_final,
                                                  intervention_material_cost]).reset_index(drop=True)

intervention_material_cost_final.to_excel(writer0, sheet_name='capital_cost')

# ~~~~~~~CALCULATING INDIVIDUAL DETAILED MATERIAL COSTS PER INTERVENTION~~~~~~~

writer1 = pd.ExcelWriter('RESULTS_detailed_material_costs.xlsx', engine='xlsxwriter')
matrix_shape = construction_material_quantities.shape  # [0] is number of rows and [1] is number of columns

for i in range(3, matrix_shape[1]):  # index 3 is first location of intervention data
    detailed_material_cost = []
    detailed_material_cost_FINAL = pd.DataFrame()
    column_names = list(construction_material_unit_costs_UNCERTAINTY)  # call column names of materials
    tab_names = list(construction_material_quantities)  # call column names of construction material csv

    for j in range(N_runs):
        construction_material_unit_costs = construction_material_unit_costs_UNCERTAINTY.iloc[j, :]
        construction_material_unit_costs = pd.DataFrame([construction_material_unit_costs])
        construction_material_unit_costs.columns = [k for k in range(construction_material_unit_costs.shape[1])]
        construction_material_unit_costs = construction_material_unit_costs.transpose()
        construction_material_unit_costs = construction_material_unit_costs.fillna(0)

        detailed_material_cost = construction_material_quantities.iloc[0:matrix_shape[0], i] * \
            construction_material_unit_costs.iloc[0:matrix_shape[0], 0]
        detailed_material_cost = pd.DataFrame([detailed_material_cost])
        detailed_material_cost_FINAL = pd.concat([detailed_material_cost_FINAL,
                                                  detailed_material_cost]).reset_index(drop=True)
    detailed_material_cost_FINAL.columns = column_names
    detailed_material_cost_FINAL.to_excel(writer1, sheet_name=tab_names[i])

writer1.save()