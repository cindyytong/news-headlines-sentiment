# average sentiment by year across all news sources

INCLUDED_COMPANIES = ["New York Times", "CNN", "FOX", "Washington Post", "CNBC", "The Guardian"]

def write_chunk(row):
    with open("../output/average_by_year.csv", "w") as f_out:
        f_out.writelines(row)
with open("../output/sentiment_by_year.csv", "r") as f:
    avg_row = []
    year_totals = {}
    year_stats_dict = {"total_num_articles": 0, "pct_positive_articles": 0, "pct_negative_articles": 0}
    for i in range(2007, 2023):
        year_totals[str(i)] = year_stats_dict.copy()
    for line in f:
        str_arr = line.split(",")
        year = str_arr[1]
        company = str_arr[0]
        if year in year_totals.keys() and len(str_arr) > 4 and company in INCLUDED_COMPANIES:
            year_totals[year]["pct_negative_articles"] += float(str_arr[4])
        else:
            continue

    for year in year_totals:
        pct_neg_sentiment = float(year_totals[year]['pct_negative_articles']) / 6
        avg_row.append(str(pct_neg_sentiment))

    write_chunk(avg_row)
