def write_chunk(part, lines):
    with open(headlines_+ str(part) +.csv, w) as f_out:
        f_out.write(header)
        f_out.writelines(lines)


# 20210105,Washington Post,Pro-Trump forums erupt with violent threats ahead of Wednesday’s rally,https://www.washingtonpost.com/technology/2021/01/05/parler-telegram-violence-dc-protests/
with open(headlines.csv, r) as f:
    lines = []
    for line in f:
        count += 1
        lines.append(line)
        if count % chunk_size == 0:
            write_chunk(count // chunk_size, lines)
            lines = []
    # write remainder
    if len(lines) > 0:
        write_chunk((count // chunk_size) + 1, lines)

chunk_size = 400000  # GCP Bigquery limit is 100mb



with open(headlines.csv, r) as f:
    count = 0
    header = f.readline()
    lines = []
    for line in f:
        count += 1
        cleaned_line = line.replace("'", "").replace('"', "")
        lines.append(cleaned_line)
        if count % chunk_size == 0:
            write_chunk(count // chunk_size, lines)
            lines = []
    # write remainder
    if len(lines) > 0:
        write_chunk((count // chunk_size) + 1, lines)