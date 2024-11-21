# input_file = "change.csv"

# # Output CSV file name
# output_file = "revarse.csv"

# # Read data from CSV file
# with open(input_file, "r") as infile, open(output_file, "w") as outfile:
#     # Read all lines from the input file
#     lines = infile.readlines()
    
#     # Reverse the order of lines
#     lines.reverse()

#     # Write all lines to the output file
#     outfile.writelines(lines)

# print("Data has been successfully reordered, and written to", output_file)


# Input CSV file name
input_file = "up_data.csv"

# Output CSV file name
output_file = "haryana.csv"

# Read data from CSV file and reformat it
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

# Reverse the order of the formatted data sets
reversed_data_sets = list(reversed(data_sets))

# Write the reversed data to the output CSV file with whitespace as delimiter
with open(output_file, "w") as csvfile:
    for data_set in reversed_data_sets:
        # Write each row to the output file
        csvfile.write(" ".join(data_set) + "\n")

print("Data has been successfully reformatted, reversed, and written to", output_file)
