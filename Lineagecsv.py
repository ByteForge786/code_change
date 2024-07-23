import csv

def add_table_columns(input_file, output_file, source_table, target_table):
    # Read the input file and count total rows
    with open(input_file, 'r', newline='') as infile:
        reader = csv.reader(infile)
        header = next(reader)  # Read and store the header
        rows = list(reader)    # Read all rows into a list
    
    total_rows = len(rows)
    
    # Count the number of unique source attributes
    unique_sources = len(set(row[0] for row in rows))
    
    # Calculate how many times to repeat each table name
    repeat_count = total_rows // unique_sources

    # Write the output file with new columns
    with open(output_file, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        
        # Write the new header
        writer.writerow(['Source Table', 'Target Table'] + header)

        source_count = 0
        for row in rows:
            if source_count < repeat_count:
                source_entry = source_table
            else:
                source_entry = ''
            
            new_row = [source_entry, target_table] + row
            writer.writerow(new_row)

            source_count = (source_count + 1) % repeat_count

# Example usage
input_file = 'input.csv'
output_file = 'output.csv'
source_table = 'SourceTableName'
target_table = 'TargetTableName'

add_table_columns(input_file, output_file, source_table, target_table)
