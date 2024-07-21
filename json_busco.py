import marimo

__generated_with = "0.6.2"
app = marimo.App()


@app.cell
def __():
    import json
    return json,


@app.cell
def __():
    import glob
    return glob,


@app.cell
def __():
    import polars as pl
    return pl,


@app.cell
def __():
    import os
    return os,


@app.cell
def __():
    list_of_files_path = "./"
    return list_of_files_path,


@app.cell
def __():
    def busco_json_convienience_function(my_data:dict):
        """
        
        This is a convienience function meant to pull the following key values out of the the json dict.

        1. "Complete percentage"
        2. "Single copy percentage"
        3. "Multi copy percentage"
        4. "Fragmented percentage"
        5. "Missing percentage"

        Inputs:
            1. Supply a busco json as a dict

            2. Name of the JSON/dict
        """

        subset_dict = dict()
        
        # The field "results" is the one that has all the percentage values
        results_field = my_data.get("results",{})

        keys_to_include = [
            "Complete percentage",
            "Single copy percentage",
            "Multi copy percentage",
            "Fragmented percentage",
            "Missing percentage"
        ]

        subset_dict = {k: results_field.get(k,"N/A") for k in keys_to_include}
        
        return(subset_dict)
    return busco_json_convienience_function,


@app.cell
def __(glob, list_of_files_path):
    list_of_files = glob.glob(list_of_files_path + "*.json")
    return list_of_files,


@app.cell
def __(busco_json_convienience_function, json, list_of_files, os):
    all_jsons = []

    for current_json in list_of_files:
        
        # Get just the basename without extension
        base_name = os.path.basename(current_json).split(".")[0]

        # Open the JSON file
        with open(current_json, 'r') as f:
            # Parse the JSON data into a Python dictionary
            data = json.load(f)
        
        base_name = busco_json_convienience_function(data)

        all_jsons.append(base_name)
    return all_jsons, base_name, current_json, data, f


@app.cell
def __(all_jsons, pl):
    percentages = pl.DataFrame(all_jsons)
    return percentages,


@app.cell
def __(list_of_files, os):
    json_names = [os.path.basename(i).split(".")[0] for i in list_of_files]
    return json_names,


@app.cell
def __(json_names, percentages, pl):
    # Add names to the percentages

    perecentages_with_names = pl.DataFrame({
        "source": json_names
    }).with_columns(percentages)
    return perecentages_with_names,


@app.cell
def __(perecentages_with_names):
    perecentages_with_names.write_csv("pecentages_with_names.tsv",separator="\t")
    return


if __name__ == "__main__":
    app.run()
