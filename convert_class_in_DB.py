


import pandas as pd



###########################################################
#  Convert CLASS column in DB from Greek to English codes #
#  for example "Α" -> "ae", "Β" -> "be" etc.              #
###########################################################

def convert_class_in_DB():
    my_db_file = "M:/ANALYSIS DB_v1.xlsx"
    
    # Load Excel file
    df = pd.read_excel(my_db_file)

    # Define your mapping rules
    class_mapping = {
        "Α": "ae",
        "Β": "be",
        "Γ": "ge",
        "Δ": "de",
        "Ε": "ee",
        "ΣΤ": "ste",
        "Α ΓΥΜΝ": "ag",
        "Β ΓΥΜΝ": "bg",
        "Γ ΓΥΜΝ": "gg"
    }

    # Apply the mapping
    df["RADAR CLASS"] = df["RADAR CLASS"].replace(class_mapping)

    # Save back to Excel
    df.to_excel("M:/ANALYSIS DB_v2.xlsx", index=False)
