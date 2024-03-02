import csv

# Read csv file with the domain names and return the array containg the URL as strings
def read_domains(file_name):
    domains = []
    with open(file_name, mode='r', newline='') as csv_file:
        data = csv.reader(csv_file)
        print(f'Column headers are {next(data)}')
        
        row_count = 0
        for row in data:
            domains.append("".join(row).replace("[","").replace("]",""))
            row_count += 1

        print(f'Read {row_count} domains')

    return domains

def read_company_data(file_name):
    company_data = []
    with open(file_name, mode='r', newline='') as csv_file:
        data = csv.DictReader(csv_file)
        column_headers = data.fieldnames    # reading the column headers from the first row
        print(f'Column headers are: {data.fieldnames}')

        row_count = 0
        for row in data: 
            row[column_headers[3]] = row[column_headers[3]].split(" | ")    # converting from string to list based on delimiter
            company_data.append(row)
            row_count += 1

        print(f'Read {row_count} company names')
        
    return company_data

def read_api_data(file_name):
    api_data = []
    with open(file_name, mode='r', newline='') as csv_file:
        data = csv.DictReader(csv_file)
        column_headers = data.fieldnames    # reading the column headers from the first row
        print(f'Column headers are: {column_headers}')

        row_count = 0
        for row in data:
            row[column_headers[1]] = row[column_headers[1]].replace('(', '').replace(')', '').replace('-', ' ').replace('.', ' ')   # removing ()-. from phone number
            api_data.append(row)
            row_count += 1

        print(f'Read {row_count} API data')
    
    return api_data