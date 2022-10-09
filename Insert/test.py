from unittest import result
from Utility import read_file
import anonymizer

# csvの読み出し
data = read_file.read_csv("Data/soturon_random_data.csv", True)

result = anonymizer.single_dim_mondrian(data, 3, 0)
print(result)

""" print(type(data[0].values()))

for value in data[0].values():
    print(type(value[0])) """

#print(type(data[0].values()))
#print(data)

book = {
    'id': 123,
    'authors': ['Author 1'],
    'title': 'Title 1'
}

#book['id'] = book.pop('id')

""" for i in book.values():
    print(i, type(i))
 """


