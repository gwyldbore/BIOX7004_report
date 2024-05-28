import pandas as pd
import distinctipy
import os
import itol_text

def get_info_list(df, col, id_field):
    info_list = [(df.at[i, id_field], df.at[i, col]) if pd.notna(df.at[i, col]) else (df.at[i, id_field], "None") for i in df.index]
    return info_list

def get_colour_dict(df, col):
    df = df.fillna("None")
    unique_values = df[col].unique()
    colour_set = [distinctipy.get_hex(x) for x in distinctipy.get_colors(len(unique_values))]
    colour_dict = {value: colour_set[i % len(colour_set)] for i, value in enumerate(unique_values)}
    if "None" in colour_dict:
        colour_dict["None"] = "#FFFFFF"     
    return colour_dict

def generate_itol_colorstrip(col, colour_dict, info_list, output_filename):
    with open(output_filename, "w") as f:
        f.write(itol_text.dataset_colorstrip_text.replace("<custom_dataset_label>", col))
        for info, label in info_list:
            f.write(f"{info},{colour_dict[label]},{label} \n")
    print(f"File '{output_filename}' has been created.\n")

def generate_itol_ranges(col, colour_dict, info_list, output_filename):
    with open(output_filename, "w") as f:
        f.write(itol_text.dataset_ranges_text.replace("<custom_dataset_label>", col))
        for info, label in info_list:
            f.write(f"{info},{info},{colour_dict[label]},{colour_dict[label]},{colour_dict[label]},dashed,2,{label},black,italic\n")
    print(f"File '{output_filename}' has been created.\n")

def generate_itol_text(col, info_list, output_filename):
    with open(output_filename, "w") as f:
        f.write(itol_text.dataset_text_text.replace("<custom_dataset_label>", col))
        for info, label in info_list:
            if label != "None":
                position = 1 if info[0] == "N" and info[1:].isdigit() else -1
                f.write(f"{info},{label},{position},#0000ff,bold-italic,1,0 \n")
    print(f"File '{output_filename}' has been created.\n")

def main():
    df = pd.read_csv("../example_data/kari_example.csv") # Dataframe with annotations
    annotation_cols = [x for x in df.columns] # Columns you want to generate itol annotations for
    outpath = "../itol_output" # Folder to write out itol annotations
    id_field = 'truncated_info' # ID field (will be skipped when making annotations)

    if not os.path.exists(outpath):
        os.makedirs(outpath)

    for col in annotation_cols:
        # Skip the info column, which won't be informative
        if col != id_field and col in df:
            colour_dict = get_colour_dict(df, col)
            info_list = get_info_list(df, col, id_field)
            generate_itol_colorstrip(col, colour_dict, info_list, f"{outpath}/{col}_itol_colorstrip.txt")
            generate_itol_ranges(col, colour_dict, info_list, f"{outpath}/{col}_itol_ranges.txt")

    text_cols = ['value']
    for text_col in text_cols:
        info_list = get_info_list(df, text_col, id_field)
        generate_itol_text(text_col, info_list, f"{outpath}/{text_col}_itol_text.txt")

if __name__ == "__main__":
    main()
