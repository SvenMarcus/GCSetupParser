import sys
import pandas as pd

from lua_utils import LuaTable, FunctionCall

if len(sys.argv) < 3:
    print("Error. Not enough input arguments")
    print("Usage: gc_setup_parser.py input.csv output.lua")
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]

gc_data = pd.read_csv(input_file, sep=None, engine="python")

gc_main_table = LuaTable()

current_planet = None
current_planet_table = None
current_era = 0
current_era_table = None

starting_forces_table = None

for index, row in gc_data.iterrows():
    if row["Planet"] != current_planet:
        current_planet = row["Planet"]
        current_planet_table = LuaTable()
        gc_main_table.add(current_planet, current_planet_table)
    
    if row["Era"] != current_era:
        current_era = row["Era"]
        if not pd.isna(row["ReuseEra"]):
            current_era_table = gc_main_table.get(current_planet).get(int(row["ReuseEra"]))
            current_planet_table.add(value=current_era_table)
            continue
    
        current_era_table = LuaTable()
        current_planet_table.add(value=current_era_table)

        starting_forces_table = LuaTable()
        current_era_table.add("Owner", row["Owner"])
        current_era_table.add("StartingForces", starting_forces_table)

    if starting_forces_table:
        object_type = row["ObjectType"]
        amount = int(row["Amount"])

        if amount > 1:
            starting_forces_table.add(value=FunctionCall("listOf", amount, object_type))
        elif amount == 1:
            starting_forces_table.add(value=object_type)
        else:
            pass

output = "return " + str(gc_main_table)

file = open(output_file, "w+")
file.write(output)
file.close()

sys.exit(0)