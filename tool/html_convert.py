import pandas as pd
import os
import sys

html_template = """
<!doctype html>
<html lang="ja">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css">
  </head>
  <body>
    <script src="https://code.jquery.com/jquery-3.2.1.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>
    <div class="container">
        {table}
    </div>
  </body>
</html>
"""

args = sys.argv

if len(args) ==2:
    print("第1引数：" + args[1])
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root_path = os.path.dirname(current_dir)
    test_data_parent_path = os.path.join(project_root_path, "data", args[1])
    print(test_data_parent_path)
    estimation_result_path = os.path.join(test_data_parent_path, "estimation")
    if os.path.exists(os.path.join(estimation_result_path, "comparison.csv")):
        print('比較用csvデータあり')
    else:
        print('比較用csvデータなし')
        quit()
else:
    print('以下形式でテスト対象フォルダを指定してください')
    print('$ python html_convert.py  <folder> ')
    quit()

pd.set_option("display.max_colwidth", 120)
df = pd.read_csv(os.path.join(estimation_result_path, "comparison.csv"))

# imgタグの文字列へ変換
df["img_path"] = df["img_path"].map(lambda s: "<img src='{}' width='200' />".format(s))
df["estimation_pixels"] = df["estimation_pixels"].map(lambda s: "<img src='{}' width='200' />".format(s))
df["correct_pixels"] = df["correct_pixels"].map(lambda s: "<img src='{}' width='200' />".format(s))
df["roi"] = df["roi"].map(lambda s: "<img src='{}' width='200' />".format(s))
table = df.to_html(classes=["table", "table-bordered", "table-hover"], escape=False)
html = html_template.format(table=table)

with open("test.html", "w") as f:
    f.write(html)