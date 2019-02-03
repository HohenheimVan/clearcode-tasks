# CSV report processing
The app reads a CSV file. Creates a new CSV file with a report aggregated by date and country.

Input format: CSV file with columns:
* date(MM/DD/YYYY),
* state name, 
* number of impressions and CTR percentage

Output format: UTF-8 CSV file with Unix line endings, with columns:
* date (YYYY-MM-DD),
* three letter country code (or XXX for unknown states),
* number of impressions,
* number of clicks (rounded, assuming the CTR is exact).

Rows are sorted lexicographically by date followed by the country code.
