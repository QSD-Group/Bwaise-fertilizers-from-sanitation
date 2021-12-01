# Title: Novel financing strategies to simultaneously advance development goals for sanitation and agriculture
# through nutrient recovery
# Author: Hannah A.C. Lohman
# Created: February 21, 2018
# Updated: February 26, 2019

# This script, uncertainty_ranges_SAN.py, develops parameter ranges for sensitivity and uncertainty

# ~~~~~~~IMPORT DATA AND FILES NECESSARY~~~~~~~

import pandas as pd  # import pandas for matrix data manipulation
from scipy import stats
from pyDOE import *

# UDDT and Pit Latrine Input Data
construction_material_unit_costs = pd.read_excel('input_data_file.xlsx', sheetname="material_unit_costs")  # import cost
material_reuse_ratio_input = pd.read_excel('input_data_file.xlsx', sheetname='material_reuse_ratio')

# General Input Data for UDDT, Pit Latrine, Tanks, and Resource Recovery Processes
technology_life_span = pd.read_excel('input_data_file.xlsx', sheetname="tech_life_span")  # import technology life span
technology_maintenance_time = pd.read_excel('input_data_file.xlsx', sheetname="tech_maint_time")  # import file
maintenance_cost_ratio = pd.read_excel('input_data_file.xlsx', sheetname="maint_cost_ratio")  # import file
operation_cost_ratio = pd.read_excel('input_data_file.xlsx', sheetname="op_cost_ratio")  # import file
labor_cost_ratio = pd.read_excel('input_data_file.xlsx', sheetname="labor_cost_ratio")  # import file

# Resource Recovery Input Data
nutrient_rec_efficiency_UNIFORM_input = pd.read_excel('input_data_file.xlsx', sheetname='nutrient_recovery_efficiency')
transport_costs_UNIFORM_input = pd.read_excel('input_data_file.xlsx', sheetname='transport_costs')
resource_recovery_TRIANGLE_input = pd.read_excel('input_data_file.xlsx', sheetname='RR_triangle')
resource_recovery_UNIFORM_input = pd.read_excel('input_data_file.xlsx', sheetname='RR_uniform')
RR_fertilizer_cost = pd.read_excel('input_data_file.xlsx', sheetname='fertilizer_cost')
RR_P_recovery_UNIFORM = pd.read_excel('input_data_file.xlsx', sheetname='RR_P_recovery_uniform')
RR_N_recovery_UNIFORM = pd.read_excel('input_data_file.xlsx', sheetname='RR_N_recovery_uniform')
RR_N_recovery_TRIANGLE = pd.read_excel('input_data_file.xlsx', sheetname='RR_N_recovery_triangle')
RR_K_recovery_TRIANGLE = pd.read_excel('input_data_file.xlsx', sheetname='RR_K_recovery_triangle')

# Discounted Cash Flow Analysis Input Data
DCA_parameters_TRIANGLE = pd.read_excel('input_data_file.xlsx', sheetname='DCA_parameters')

# ~~~~~~~GENERIC UNCERTAINTY PARAMETERS~~~~~~~
N_samples = 10000  # number runs for uncertainty analysis (10,000)
writer = pd.ExcelWriter('OUTPUT_uncertainty_ranges.xlsx', engine='xlsxwriter')

# ~~~~~~~UDDT & PIT LATRINE MATERIAL COST UNCERTAINTY RANGES~~~~~~~

# Material Unit Costs

matrix_shape = construction_material_unit_costs.shape  # [0] is number of rows and [1] is number of columns
unit_costs_TRIANGLE = []
unit_costs_TRIANGLE_df = []
unit_costs_TRIANGLE_final = pd.DataFrame()

for i in range(matrix_shape[0]):
    minimum = construction_material_unit_costs.minimum[i]
    width = construction_material_unit_costs.width[i]

    unit_costs_TRIANGLE = stats.uniform.ppf(lhs(1, samples=N_samples), loc=minimum, scale=width)
    unit_costs_TRIANGLE_df = pd.DataFrame.from_records(unit_costs_TRIANGLE)
    unit_costs_TRIANGLE_final = pd.concat([unit_costs_TRIANGLE_final, unit_costs_TRIANGLE_df], axis=1)

unit_costs_TRIANGLE_final.columns = [construction_material_unit_costs.label]
unit_costs_TRIANGLE_final.to_excel(writer, sheet_name="material_unit_costs")

# Material Reuse Ratios (Materials reused 5-15 times)

minimum = material_reuse_ratio_input.minimum
width = material_reuse_ratio_input.width

material_reuse_UNIFORM = stats.uniform.ppf(lhs(1, samples=N_samples), loc=minimum, scale=width)
material_reuse_UNIFORM_df = pd.DataFrame.from_records(material_reuse_UNIFORM)

material_reuse_UNIFORM_df.to_excel(writer, sheet_name='material_reuse_ratio')

# ~~~~~~~ GENERAL LABOR & O&M UNCERTAINTY RANGES~~~~~~~

# UDDT & Pit Latrine Technology Life Span

matrix_shape = technology_life_span.shape  # [0] is number of rows and [1] is number of columns
life_span_TRIANGLE = []
life_span_TRIANGLE_df = []
life_span_TRIANGLE_final = pd.DataFrame()

for i in range(matrix_shape[0]):
    peak = technology_life_span.peak_distance[i]
    minimum = technology_life_span.minimum[i]
    width = technology_life_span.width[i]

    life_span_TRIANGLE = stats.triang.ppf(lhs(1, samples=N_samples), peak, loc=minimum, scale=width)
    life_span_TRIANGLE_df = pd.DataFrame.from_records(life_span_TRIANGLE)
    life_span_TRIANGLE_final = pd.concat([life_span_TRIANGLE_final, life_span_TRIANGLE_df], axis=1)

life_span_TRIANGLE_final.columns = [technology_life_span.label]
life_span_TRIANGLE_final.to_excel(writer, sheet_name="tech_life_span")

# UDDT & Pit Latrine Technology Maintenance Time

matrix_shape = technology_maintenance_time.shape  # [0] is number of rows and [1] is number of columns
maintenance_time_TRIANGLE = []
maintenance_time_TRIANGLE_df = []
maintenance_time_TRIANGLE_final = pd.DataFrame()

for i in range(matrix_shape[0]):
    peak = technology_maintenance_time.peak_distance[i]
    minimum = technology_maintenance_time.minimum[i]
    width = technology_maintenance_time.width[i]

    maintenance_time_TRIANGLE = stats.triang.ppf(lhs(1, samples=N_samples), peak, loc=minimum, scale=width)
    maintenance_time_TRIANGLE_df = pd.DataFrame.from_records(maintenance_time_TRIANGLE)
    maintenance_time_TRIANGLE_final = pd.concat([maintenance_time_TRIANGLE_final, maintenance_time_TRIANGLE_df], axis=1)

maintenance_time_TRIANGLE_final.columns = [technology_maintenance_time.label]
maintenance_time_TRIANGLE_final.to_excel(writer, sheet_name="tech_maint_time")

# Maintenance Cost Ratio of Capital Material Cost

matrix_shape = maintenance_cost_ratio.shape  # [0] is number of rows and [1] is number of columns
maintenance_ratio_TRIANGLE = []
maintenance_ratio_TRIANGLE_df = []
maintenance_ratio_TRIANGLE_final = pd.DataFrame()

for i in range(matrix_shape[0]):
    peak = maintenance_cost_ratio.peak_distance[i]
    minimum = maintenance_cost_ratio.minimum[i]
    width = maintenance_cost_ratio.width[i]

    maintenance_ratio_TRIANGLE = stats.triang.ppf(lhs(1, samples=N_samples), peak, loc=minimum, scale=width)
    maintenance_ratio_TRIANGLE_df = pd.DataFrame.from_records(maintenance_ratio_TRIANGLE)
    maintenance_ratio_TRIANGLE_final = pd.concat([maintenance_ratio_TRIANGLE_final, maintenance_ratio_TRIANGLE_df],
                                                 axis=1)

maintenance_ratio_TRIANGLE_final.columns = [maintenance_cost_ratio.label]
maintenance_ratio_TRIANGLE_final.to_excel(writer, sheet_name="maint_cost_ratio")

# Operation Cost Ratio of Capital Material Cost

matrix_shape = operation_cost_ratio.shape  # [0] is number of rows and [1] is number of columns
operation_ratio_TRIANGLE = []
operation_ratio_TRIANGLE_df = []
operation_ratio_TRIANGLE_final = pd.DataFrame()

for i in range(matrix_shape[0]):
    peak = operation_cost_ratio.peak_distance[i]
    minimum = operation_cost_ratio.minimum[i]
    width = operation_cost_ratio.width[i]

    operation_ratio_TRIANGLE = stats.triang.ppf(lhs(1, samples=N_samples), peak, loc=minimum, scale=width)
    operation_ratio_TRIANGLE_df = pd.DataFrame.from_records(operation_ratio_TRIANGLE)
    operation_ratio_TRIANGLE_final = pd.concat([operation_ratio_TRIANGLE_final, operation_ratio_TRIANGLE_df], axis=1)

operation_ratio_TRIANGLE_final.columns = [operation_cost_ratio.label]
operation_ratio_TRIANGLE_final.to_excel(writer, sheet_name="op_cost_ratio")

# Labor Cost Ratio of Capital Material Cost

matrix_shape = labor_cost_ratio.shape  # [0] is number of rows and [1] is number of columns
labor_ratio_TRIANGLE = []
labor_ratio_TRIANGLE_df = []
labor_ratio_TRIANGLE_final = pd.DataFrame()

for i in range(matrix_shape[0]):
    peak = labor_cost_ratio.peak_distance[i]
    minimum = labor_cost_ratio.minimum[i]
    width = labor_cost_ratio.width[i]

    labor_ratio_TRIANGLE = stats.triang.ppf(lhs(1, samples=N_samples), peak, loc=minimum, scale=width)
    labor_ratio_TRIANGLE_df = pd.DataFrame.from_records(labor_ratio_TRIANGLE)
    labor_ratio_TRIANGLE_final = pd.concat([labor_ratio_TRIANGLE_final, labor_ratio_TRIANGLE_df], axis=1)

labor_ratio_TRIANGLE_final.columns = [labor_cost_ratio.label]
labor_ratio_TRIANGLE_final.to_excel(writer, sheet_name="labor_cost_ratio")

# ~~~~~~~RESOURCE RECOVERY UNCERTAINTY RANGES~~~~~~~

# Uniform Distribution for Nutrient Recovery Efficiencies (UDDT, transport, storage)
matrix_shape = nutrient_rec_efficiency_UNIFORM_input.shape  # [0] is number of rows and [1] is number of columns
nutrient_rec_efficiency_UNIFORM = []
nutrient_rec_efficiency_UNIFORM_df = []
nutrient_rec_efficiency_UNIFORM_final = pd.DataFrame()

for i in range(matrix_shape[0]):
    minimum = nutrient_rec_efficiency_UNIFORM_input.minimum[i]
    width = nutrient_rec_efficiency_UNIFORM_input.width[i]

    nutrient_rec_efficiency_UNIFORM = stats.uniform.ppf(lhs(1, samples=N_samples), loc=minimum, scale=width)
    nutrient_rec_efficiency_UNIFORM_df = pd.DataFrame.from_records(nutrient_rec_efficiency_UNIFORM)
    nutrient_rec_efficiency_UNIFORM_final = pd.concat([nutrient_rec_efficiency_UNIFORM_final,
                                                       nutrient_rec_efficiency_UNIFORM_df], axis=1)

# Uniform Distribution for Urine Transport Costs (cart & truck)
matrix_shape = transport_costs_UNIFORM_input.shape  # [0] is number of rows and [1] is number of columns
transport_costs_UNIFORM = []
transport_costs_UNIFORM_df = []
transport_costs_UNIFORM_final = pd.DataFrame()

for i in range(matrix_shape[0]):
    minimum = transport_costs_UNIFORM_input.minimum[i]
    width = transport_costs_UNIFORM_input.width[i]

    transport_costs_UNIFORM = stats.uniform.ppf(lhs(1, samples=N_samples), loc=minimum, scale=width)
    transport_costs_UNIFORM_df = pd.DataFrame.from_records(transport_costs_UNIFORM)
    transport_costs_UNIFORM_final = pd.concat([transport_costs_UNIFORM_final, transport_costs_UNIFORM_df], axis=1)

# Triangle Distribution for Resource Recovery Parameters
matrix_shape = resource_recovery_TRIANGLE_input.shape  # [0] is number of rows and [1] is number of columns
resource_recovery_TRIANGLE = []
resource_recovery_TRIANGLE_df = []
resource_recovery_TRIANGLE_final = pd.DataFrame()

for i in range(matrix_shape[0]):
    peak = resource_recovery_TRIANGLE_input.peak_distance[i]
    minimum = resource_recovery_TRIANGLE_input.minimum[i]
    width = resource_recovery_TRIANGLE_input.width[i]

    resource_recovery_TRIANGLE = stats.triang.ppf(lhs(1, samples=N_samples), peak, loc=minimum, scale=width)
    resource_recovery_TRIANGLE_df = pd.DataFrame.from_records(resource_recovery_TRIANGLE)
    resource_recovery_TRIANGLE_final = pd.concat([resource_recovery_TRIANGLE_final, resource_recovery_TRIANGLE_df],
                                                 axis=1)

# Uniform Distribution for Resource Recovery Parameters
matrix_shape = resource_recovery_UNIFORM_input.shape  # [0] is number of rows and [1] is number of columns
resource_recovery_UNIFORM = []
resource_recovery_UNIFORM_df = []
resource_recovery_UNIFORM_final = pd.DataFrame()

for i in range(matrix_shape[0]):
    minimum = resource_recovery_UNIFORM_input.minimum[i]
    width = resource_recovery_UNIFORM_input.width[i]

    resource_recovery_UNIFORM = stats.uniform.ppf(lhs(1, samples=N_samples), loc=minimum, scale=width)
    resource_recovery_UNIFORM_df = pd.DataFrame.from_records(resource_recovery_UNIFORM)
    resource_recovery_UNIFORM_final = pd.concat([resource_recovery_UNIFORM_final, resource_recovery_UNIFORM_df], axis=1)

# Resource Recovery Fertilizer Unit Costs (uniform distribution)
matrix_shape = RR_fertilizer_cost.shape  # [0] is number of rows and [1] is number of columns
resource_recovery_nutrient_cost = []
resource_recovery_nutrient_cost_df = []
resource_recovery_nutrient_cost_final = pd.DataFrame()

for i in range(matrix_shape[0]):
    minimum = RR_fertilizer_cost.minimum[i]
    width = RR_fertilizer_cost.width[i]

    resource_recovery_nutrient_cost = stats.uniform.ppf(lhs(1, samples=N_samples), loc=minimum, scale=width)
    resource_recovery_nutrient_cost_df = pd.DataFrame.from_records(resource_recovery_nutrient_cost)
    resource_recovery_nutrient_cost_final = pd.concat([resource_recovery_nutrient_cost_final,
                                                       resource_recovery_nutrient_cost_df], axis=1)

# Phosphorus Recovery Parameters UNIFORM Distribution
matrix_shape = RR_P_recovery_UNIFORM.shape  # [0] is number of rows and [1] is number of columns
P_recovery_UNIFORM = []
P_recovery_UNIFORM_df = []
P_recovery_UNIFORM_final = pd.DataFrame()

for i in range(matrix_shape[0]):
    minimum = RR_P_recovery_UNIFORM.minimum[i]
    width = RR_P_recovery_UNIFORM.width[i]

    P_recovery_UNIFORM = stats.uniform.ppf(lhs(1, samples=N_samples), loc=minimum, scale=width)
    P_recovery_UNIFORM_df = pd.DataFrame.from_records(P_recovery_UNIFORM)
    P_recovery_UNIFORM_final = pd.concat([P_recovery_UNIFORM_final, P_recovery_UNIFORM_df], axis=1)

# Nitrogen Reocvery Parameters UNIFORM Distribution
matrix_shape = RR_N_recovery_UNIFORM.shape  # [0] is number of rows and [1] is number of columns
N_recovery_UNIFORM = []
N_recovery_UNIFORM_df = []
N_recovery_UNIFORM_final = pd.DataFrame()

for i in range(matrix_shape[0]):
    minimum = RR_N_recovery_UNIFORM.minimum[i]
    width = RR_N_recovery_UNIFORM.width[i]

    N_recovery_UNIFORM = stats.uniform.ppf(lhs(1, samples=N_samples), loc=minimum, scale=width)
    N_recovery_UNIFORM_df = pd.DataFrame.from_records(N_recovery_UNIFORM)
    N_recovery_UNIFORM_final = pd.concat([N_recovery_UNIFORM_final, N_recovery_UNIFORM_df], axis=1)

# Nitrogen Recovery Parameters TRIANGLE Distribution
matrix_shape = RR_N_recovery_TRIANGLE.shape  # [0] is number of rows and [1] is number of columns
N_recovery_TRIANGLE = []
N_recovery_TRIANGLE_df = []
N_recovery_TRIANGLE_final = pd.DataFrame()

for i in range(matrix_shape[0]):
    peak = RR_N_recovery_TRIANGLE.peak_distance[i]
    minimum = RR_N_recovery_TRIANGLE.minimum[i]
    width = RR_N_recovery_TRIANGLE.width[i]

    N_recovery_TRIANGLE = stats.triang.ppf(lhs(1, samples=N_samples), peak, loc=minimum, scale=width)
    N_recovery_TRIANGLE_df = pd.DataFrame.from_records(N_recovery_TRIANGLE)
    N_recovery_TRIANGLE_final = pd.concat([N_recovery_TRIANGLE_final, N_recovery_TRIANGLE_df], axis=1)

# Potassium Recovery Parameters TRIANGLE Distribution
matrix_shape = RR_K_recovery_TRIANGLE.shape  # [0] is number of rows and [1] is number of columns
K_recovery_TRIANGLE = []
K_recovery_TRIANGLE_df = []
K_recovery_TRIANGLE_final = pd.DataFrame()

for i in range(matrix_shape[0]):
    peak = RR_K_recovery_TRIANGLE.peak_distance[i]
    minimum = RR_K_recovery_TRIANGLE.minimum[i]
    width = RR_K_recovery_TRIANGLE.width[i]

    K_recovery_TRIANGLE = stats.triang.ppf(lhs(1, samples=N_samples), peak, loc=minimum, scale=width)
    K_recovery_TRIANGLE_df = pd.DataFrame.from_records(K_recovery_TRIANGLE)
    K_recovery_TRIANGLE_final = pd.concat([K_recovery_TRIANGLE_final, K_recovery_TRIANGLE_df], axis=1)

# Output Uncertainty Ranges to Excel File
nutrient_rec_efficiency_UNIFORM_final.columns = [nutrient_rec_efficiency_UNIFORM_input.label]
transport_costs_UNIFORM_final.columns = [transport_costs_UNIFORM_input.label]
resource_recovery_TRIANGLE_final.columns = [resource_recovery_TRIANGLE_input.label]
resource_recovery_UNIFORM_final.columns = [resource_recovery_UNIFORM_input.label]
resource_recovery_nutrient_cost_final.columns = [RR_fertilizer_cost.label]
P_recovery_UNIFORM_final.columns = [RR_P_recovery_UNIFORM.label]
N_recovery_UNIFORM_final.columns = [RR_N_recovery_UNIFORM.label]
N_recovery_TRIANGLE_final.columns = [RR_N_recovery_TRIANGLE.label]
K_recovery_TRIANGLE_final.columns = [RR_K_recovery_TRIANGLE.label]

nutrient_rec_efficiency_UNIFORM_final.to_excel(writer, sheet_name='nutrient_recovery_efficiency')
transport_costs_UNIFORM_final.to_excel(writer, sheet_name='transport_costs')
resource_recovery_TRIANGLE_final.to_excel(writer, sheet_name='RR_triangle')
resource_recovery_UNIFORM_final.to_excel(writer, sheet_name='RR_uniform')
resource_recovery_nutrient_cost_final.to_excel(writer, sheet_name='fertilizer_cost')
P_recovery_UNIFORM_final.to_excel(writer, sheet_name='RR_P_recovery_uniform')
N_recovery_UNIFORM_final.to_excel(writer, sheet_name='RR_N_recovery_uniform')
N_recovery_TRIANGLE_final.to_excel(writer, sheet_name='RR_N_recovery_triangle')
K_recovery_TRIANGLE_final.to_excel(writer, sheet_name='RR_K_recovery_triangle')

# ~~~~~~~DISCOUNTED CASH FLOW ANALYSIS UNCERTAINTY RANGES~~~~~~~

# Discount Rate and Tax Rate (Triangle Distribution)
matrix_shape = DCA_parameters_TRIANGLE.shape  # [0] is number of rows and [1] is number of columns
DCA_TRIANGLE = []
DCA_TRIANGLE_df = []
DCA_TRIANGLE_final = pd.DataFrame()

for i in range(matrix_shape[0]):
    peak = DCA_parameters_TRIANGLE.peak_distance[i]
    minimum = DCA_parameters_TRIANGLE.minimum[i]
    width = DCA_parameters_TRIANGLE.width[i]

    DCA_TRIANGLE = stats.triang.ppf(lhs(1, samples=N_samples), peak, loc=minimum, scale=width)
    DCA_TRIANGLE_df = pd.DataFrame.from_records(DCA_TRIANGLE)
    DCA_TRIANGLE_final = pd.concat([DCA_TRIANGLE_final, DCA_TRIANGLE_df], axis=1)

DCA_TRIANGLE_final.columns = [DCA_parameters_TRIANGLE.label]
DCA_TRIANGLE_final.to_excel(writer, sheet_name='DCA_parameters')

writer.save()

