from pathlib import Path
from datetime import datetime

from config import (
    SYMBOL,
    TIMEFRAME,
    EMA_LENGTH,
    ALMA_LENGTH,
    MAD_LENGTH_BB,
    MAD_LENGTH_FL,
    UPPER_MULTIPLIER,
    LOWER_MULTIPLIER,
)


def create_html_report(summary, df):

    report_date = (
        df["datetime"]
        .dt.strftime("%d-%m-%Y")
        .iloc[0]
    )

    generated_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    html = f"""
<!DOCTYPE html>
<html>

<head>

<meta charset="UTF-8">

<title>MAD ENGINE v1.0-alpha</title>

<style>

body{{
    font-family:Arial,Helvetica,sans-serif;
    background:#eef2f7;
    margin:40px;
}}

.container{{
    max-width:1100px;
    margin:auto;
    background:white;
    border-radius:12px;
    padding:30px;
    box-shadow:0 0 20px rgba(0,0,0,.15);
}}

h1{{
    color:#0d47a1;
    text-align:center;
    margin-bottom:5px;
}}

h3{{
    text-align:center;
    color:#666;
    margin-top:0;
}}

table{{
    width:100%;
    border-collapse:collapse;
    margin-top:15px;
}}

th{{
    background:#0d47a1;
    color:white;
    padding:10px;
}}

td{{
    padding:10px;
    border:1px solid #dcdcdc;
}}

.section{{
    margin-top:30px;
}}

.footer{{
    text-align:center;
    margin-top:40px;
    color:#666;
    font-size:14px;
}}

</style>

</head>

<body>

<div class="container">

<h1>MAD ENGINE v1.0-alpha</h1>

<h3>Professional Backtest Report</h3>

<hr>

<h2>Report Information</h2>

<table>

<tr>
<td><b>Symbol</b></td>
<td>{SYMBOL}</td>

<td><b>Report Date</b></td>
<td>{report_date}</td>
</tr>

<tr>
<td><b>Timeframe</b></td>
<td>{TIMEFRAME}</td>

<td><b>Generated</b></td>
<td>{generated_time}</td>
</tr>

<tr>
<td><b>Strategy</b></td>
<td>MAD Engine</td>

<td><b>Version</b></td>
<td>v1.0-alpha</td>
</tr>

</table>

<div class="section">

<h2>Indicator Settings</h2>

<table>

<tr>
<td>EMA Length</td>
<td>{EMA_LENGTH}</td>

<td>ALMA Length</td>
<td>{ALMA_LENGTH}</td>
</tr>

<tr>
<td>MAD BB Length</td>
<td>{MAD_LENGTH_BB}</td>

<td>MAD FL Length</td>
<td>{MAD_LENGTH_FL}</td>
</tr>

<tr>
<td>Upper Multiplier</td>
<td>{UPPER_MULTIPLIER}</td>

<td>Lower Multiplier</td>
<td>{LOWER_MULTIPLIER}</td>
</tr>

</table>

</div>

<div class="section">

<h2>Performance Summary</h2>

<table>

<tr>
<th>Metric</th>
<th>Value</th>
</tr>

<tr>
<td>Total Trades</td>
<td>{summary["Total Trades"]}</td>
</tr>

<tr>
<td>Winning Trades</td>
<td>{summary["Wins"]}</td>
</tr>

<tr>
<td>Losing Trades</td>
<td>{summary["Losses"]}</td>
</tr>

<tr>
<td>Flat Trades</td>
<td>{summary["Flats"]}</td>
</tr>

<tr>
<td>Win Rate</td>
<td>{summary["Win Rate"]}%</td>
</tr>

<tr>
<td>Gross Profit</td>
<td>{summary["Gross Profit"]}</td>
</tr>

<tr>
<td>Gross Loss</td>
<td>{summary["Gross Loss"]}</td>
</tr>

<tr>
<td>Net Points</td>
<td><b>{summary["Net Points"]}</b></td>
</tr>

<tr>
<td>Average Win</td>
<td>{summary["Average Win"]}</td>
</tr>

<tr>
<td>Average Loss</td>
<td>{summary["Average Loss"]}</td>
</tr>

<tr>
<td>Profit Factor</td>
<td><b>{summary["Profit Factor"]}</b></td>
</tr>

</table>

</div>

<div class="footer">

<hr>

<b>Developed By</b>

<br><br>

<b>Gaurang Thakker</b>

<br><br>

MAD ENGINE v1.0-alpha

<br>

© 2026 Gaurang Thakker

</div>

</div>

</body>

</html>
"""

    Path("reports").mkdir(exist_ok=True)

    with open(
        "reports/report.html",
        "w",
        encoding="utf-8"
    ) as f:
        f.write(html)

    print("\n✅ HTML Report Created Successfully")