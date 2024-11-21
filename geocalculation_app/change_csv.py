# Input CSV file name
input_file = "bihar.csv"

# Output CSV file name
output_file = "change.csv"

# Read data from CSV file
data_sets = []
with open(input_file, "r") as csvfile:
    # Read each line from the input file
    lines = csvfile.readlines()
    data_set = []
    for line in lines:
        if line.strip():  # Check if the line is not empty
            # Remove leading and trailing spaces and replace multiple spaces with single space
            formatted_row = " ".join(line.strip().split())
            data_set.append(formatted_row)
        else:
            # Append the current data set to the list of data sets
            if data_set:
                data_sets.append(data_set)
                data_set = []

    # Append the last data set if it's not empty
    if data_set:
        data_sets.append(data_set)

# Write formatted data to CSV file with whitespace as delimiter
with open(output_file, "w") as csvfile:
    for data_set in data_sets:
        # Write each row to the output file
        csvfile.write(" ".join(data_set) + "\n")

print("Data has been successfully reformatted and written to", output_file)

