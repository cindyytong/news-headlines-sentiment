chunk_size = 400000 # GCP Bigquery limit is 100mb
COMPANIES = [
    "New York Times",
    "CNN",
    "FOX",
    "New York Post",
    "BBC",
    "Washington Post",
    "USA Today",
    "Daily Mail",
    "CNBC",
    "The Guardian"
]

def write_chunk(part, lines):
    with open("headlines_"+ str(part) +".csv", "w") as f_out:
        f_out.write(header)
        f_out.writelines(lines)
with open("headlines.csv", "r") as f:
    count = 0
    header = f.readline()
    lines = []
    for line in f:
        count += 1
        new_line = line.replace('"', "").replace("'", "")
        # remove commas in the title
        # example: 20070101,New York Times,Rush to Hang Hussein Was  Questioned,http://www.nytimes.com/2007/01/01/world/middleeast/01iraq.html?hp&ex=1167714000&en=85dae91ed8178e3a&ei=5094&partner=homepage
        str_arr = new_line.split(",")
        if len(str_arr) < 4:
            continue

        new_str =""
        # check date
        if len(str_arr[0]) == 8:
            new_str += str_arr[0] + ","
        else:
            continue

        # check company exists
        company = str_arr[1]
        if company in COMPANIES:
            new_str += str_arr[1] + ","
        else:
            continue

        # create headline str without commas
        i = 2
        while i < len(str_arr):
            if (str_arr[i].startswith("http")):
                new_str += ","
                new_str += str_arr[i]
                continue
            else:
                new_str += str_arr[i]
                i += 1

        # write the new entry
        lines.append(new_str)
        if count % chunk_size == 0:
            write_chunk(count // chunk_size, lines)
            lines = []
    # write remainder
    if len(lines) > 0:
        write_chunk((count // chunk_size) + 1, lines)