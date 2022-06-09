list1 = ['A', 'B', 'C']
for i in list1:
    globals()[i] = []

print('this is A:', A)
print('this is B:', B)

# 做了修改
list1 = ['A', 'B', 'C']
for i in list_1:
    # print(i)
    print(i, ':', get_simple_type(i));
    print(i, ':', get_type(i));