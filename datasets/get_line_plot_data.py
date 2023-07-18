chunk_size = 400000 # GCP Bigquery limit is 100mb
COMPANIES = {
    "nytimes": "New York Times",
    "cnn": "CNN",
    "fox": "FOX",
    "nypost": "New York Post",
    "bbc": "BBC",
    "washpost": "Washington Post",
    "usatoday": "USA Today",
    "dailymail": "Daily Mail",
    "cnbc": "CNBC",
    "guardian": "The Guardian"

}




def write_chunk(row):
    with open("data_by_company_year.csv", "w") as f_out:
        f_out.writelines(row)
with open("../output/sentiment_by_year.csv", "r") as f:

    row = ['0'] * 17
    print(row)
    i = 0
    for line in f:
        str_arr = line.split(",")
        company = str_arr[0]

        print(company)
        if company == "The Guardian" and len(str_arr) > 4:
            row[i] = str_arr[4]
            print(row)
            i += 1
        else:
            continue
    write_chunk(row)
