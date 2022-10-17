from Utility import read_file
import anonymizer_original


data = read_file.read_csv("Data/random_data.csv", True)

result = anonymizer_original.simple_k_anonymizer(data)
print(result)
