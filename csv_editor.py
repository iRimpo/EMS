import pandas as pd
import re

def webctrl_csv(csv_file):
    df = pd.read_csv(csv_file)

    # selected location
    df_loc = df[['Location']]

    # to locate the index of the starting of the building number
    def find_nth_occurrence(string, char, n):
        occurrence = -1
        for i in range(n):
            occurrence = string.find(char, occurrence + 1)
            if occurrence == -1:
                return -1  # Return -1 if the character is not found enough times
        return occurrence

    df['Building'] = 'Unknown' # added building col
    # used to find the building number of the controller
    # will be added to csv file
    for index in range(0, len(df_loc)):
        row = df_loc.at[index, 'Location']  # df_loc.at[x, 'Location'] accesses the value in the 'Location' column for each row
        start = find_nth_occurrence(row, '/', 5) # index start of building number
        start += 1

        # Extract the building number including any subsequent alphabetical characters
        if start != 0:  # original is -1, but compensated due to incremented start
            match = re.match(r'(\d+[A-Z]*)', row[start:])
            if match:
                bld_num = match.group(1)
                df.at[index, 'Building'] = bld_num

    df.to_csv(csv_file, index=False)


def metasys_csv(csv_file):
    df = pd.read_csv(csv_file)

    # Define a function to extract the building number from the 'Item' column
    def extract_building_number(item):
        if "LBNL_EMS:" in item:
            return "EMS"
        elif "LBNL_FMS:" in item:
            return "FMS"
        else:
            # Extract the first sequence of 2 or more digits from the 'Item' string
            match = re.search(r'\b\d{2,}\b', item)
            if match:
                return match.group(0)
        return 'Unknown'

    # Apply the extraction function to the 'Item' column to create the 'Building' column
    df['Building'] = df['Item'].apply(extract_building_number)
    df['Vendor Name'] = 'Metasys'

    # Save the updated DataFrame back to a CSV file
    df.to_csv(csv_file, index=False)

def lutron_csv(csv_file):
    df = pd.read_csv(csv_file)
    df_loc = df[['Area Name']]
    df['Building'] = 'Unknown'

    for index in range(0, len(df_loc)):
        row = df_loc.at[index, 'Area Name']
        bld_num = row[14:16]
        df.at[index, 'Building'] = bld_num
   
    df['Vendor Name'] = 'Lutron'

    # Save the updated DataFrame back to a CSV file
    df.to_csv(csv_file, index=False)

def wattstopper_csv(csv_file):
    df = pd.read_csv(csv_file)
    df_loc = df[['No.']]
    df['Vendor Name'] = 'Wattstopper'
    df['Building'] = '74'

    df_unique = df.drop_duplicates(subset='Source')
    
    df_unique.to_csv(csv_file, index=False)

if __name__ == "__main__":
    print('\n*** Format CSV File ***\n')

wattstopper_csv('wattstopper.csv')