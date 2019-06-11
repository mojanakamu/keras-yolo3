import pandas as pd

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

test_data_path = '../' + 'data/test01/'
test_data_img_path = test_data_path + 'img/'
correct_pixels_path = test_data_img_path + 'correct_pixels/'
estimation_pixels_path = test_data_img_path + 'estimation_pixels/'
roi_path = test_data_img_path + 'roi/'
test_data_estimation_result_path = test_data_path + 'estimation/'

df = pd.read_csv(test_data_estimation_result_path + "comparison.csv")
table = df.to_html(classes=["table", "table-bordered", "table-hover"])
html = html_template.format(table=table)

with open("test.html", "w") as f:
    f.write(html)