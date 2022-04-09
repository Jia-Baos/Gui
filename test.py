def add(**kwargs):
    print(type(kwargs))
    print(kwargs)
    return kwargs


if __name__ == '__main__':
    my_dict = {'name': 10, 'age': 12}
    new_dict = add(temperate=10)
    print(type(new_dict))
    print(new_dict)
    my_dict.update(new_dict)
    print(type(my_dict))
    print(my_dict)

    a = 10
    b =11
    print('='.join([str(a),str(b)]))



