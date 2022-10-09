from unittest import result
from Utility import read_file
import anonymizer

# csvの読み出し
data = read_file.read_csv("Data/soturon_random_data.csv", True)

result = anonymizer.single_dim_mondrian(data, 3, 0)
print(result)


