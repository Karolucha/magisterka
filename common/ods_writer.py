from collections import OrderedDict

from pyexcel_ods import save_data

data = OrderedDict()

data.update({"Sheet 1": [[1, 2, 3], [4, 5, 6]]})
data.update({"Sheet 2": [["row 1", "row 2", "row 3"]]})
save_data("your_file.ods", data)