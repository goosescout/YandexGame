def my_filter(array):
    [array.remove(elem2) for elem2 in [array.remove(elem) for elem in array if len(elem) > 4] if len(elem2) > 4]


a = ['123', '12345', '123456', '12', '1234']
my_filter(a)
print(a)
