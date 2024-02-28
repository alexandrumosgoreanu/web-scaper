import csv

# Read csv file with the domain names and return the array containg the URL as strings
def read_domains(file_name):
    domains = []
    with open(file_name, mode='r', newline='') as csv_file:
        data = csv.reader(csv_file)
        line_count = 0
        for row in data:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
            else:
                # print(type("".join(row)))
                domains.append("".join(row).replace("[","").replace("]",""))
            line_count += 1
            # print(f'\t{row["domain"]}')
        print(f'Processed {line_count} lines.')
    return domains
