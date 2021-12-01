# Bwaise-fertilizers-from-sanitation
This repository contains a model designed to evaluate the resource recovery potential and economics associated with two hypothetical nutrient recovery systems under two financing scenarios (start-up with aid and self-sustaining without aid) in Bwaise, Uganda (used in [Lohman et al., 2020](https://doi.org/10.1021/acs.est.0c03764)).


The following files are contained in this repository, and all are necessary for the model to run. Run each python file in numerical order (outputs of one file are inputs for the next). Note that this code was developed using Python 2.

- `input_data_file.xlsx` - This Excel spreadsheet includes all input parameters and uncertainty distributions.
- `1_uncertainty_ranges.py` - This file computes the 1,000 values for each uncertain parameter using Latin Hypercube Sampling.
- `2_capital_cost_UDDT_pit.py` - This file calculates the capital costs associated with a pit latrine and a urine-diverting dry toilet (UDDT).
- `3_UDDT_pit_cost.py` - This file compiles all costs associated with a pit latrine and urine-diverting dry toilet (UDDT) (e.g., capital, operation, maintenance, labor).
- `4_per_capita_nutrients.py` - This file calculates the nutrients excreted per toilet user based on Uganda-specific dietary intake parameters.
- `5_resource_recovery_cost.py` - This file calculates the costs associated with resource recovery for each system.
- `6_nutrient_market_value.py` - This file calculates the Uganda fertilizer market value for comparison with potential recovered nutrient selling prices.
- `7_tanks.py` - This file calculates the quantity of tanks necessary to store urine for scenario 1 (Simple System).
- `8_break_even_scenario2_subsidized.py` - This file calculates the break-even nutrient selling price for Scenario 2 (Advanced System) under a Start-up financing scenario (subsidized with aid).
- `9_break_even_scenario2_unsubsidized.py` - This file calculates the break-even nutrient selling price for Scenario 2 (Advanced System) under a Self-Sustaining financing scenario (unsubsidized without aid).
- `10_break_even_scenario1_subsidized.py` - This file calculates the break-even nutrient selling price for Scenario 1 (Simple System) under a Start-up financing scenario (subsidized with aid).
- `11_break_even_scenario1_unsubsidized.py` - This file calculates the break-even nutrient selling price for Scenario 1 (Simple System) under a Self-Sustaining financing scenario (unsubsidized without aid).
- `12_rate_of_return_scenario2_subsidized.py` - This file calculates the rate of return for Scenario 2 (Advanced System) under a Start-up financing scenario (subsidized with aid).
- `13_rate_of_return_scenario2_unsubsidized.py` - This file calculates the rate of return for Scenario 2 (Advanced System) under a Self-Sustaining financing scenario (unsubsidized without aid).
- `14_rate_of_return_scenario1_subsidized.py` - This file calculates the rate of return for Scenario 1 (Simple System) under a Start-up financing scenario (subsidized with aid).
- `15_rate_of_return_scenario1_unsubsidized.py` - This file calculates the rate of return for Scenario 1 (Simple System) under a Self-Sustaining financing scenario (unsubsidized without aid).
