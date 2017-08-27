
class DictObject:
    def __init__(self, *args, **kwargs):
        l = len(args)
        i = 0
        while(i < l):
            a = args[i]
            if type(a) == type(dict()):
                self.__dict_to_attr(a)
            elif type(a) == type(list()) or type(a) == type(tuple()):
                i += 1
                if i < l:
                    ap = args[i]
                    if type(a) == type(ap):
                        self.__iter_to_attr(a, ap)
                    else:
                        raise ValueError
                else:
                    raise ValueError
            else:
                raise ValueError
            i += 1
        self.__dict_to_attr(kwargs)

    def __dict_to_attr(self, d):
        for n, v in d.items():
            setattr(self, n, v)

    def __iter_to_attr(self, names, values):
        if len(names) != len(values):
            raise ValueError
        for n, v in zip(names, values):
            setattr(self, n, v)

    def __str__(self):
        return str(self.__dict__)
        

if __name__ == '__main__':
    s = DictObject()
    print(s)

    print('Init with dicts')

    s = DictObject({'a': 1})
    print(s)

    s = DictObject({'a': 1}, {'b': 2})
    print(s)

    s = DictObject({'a': 1})
    s.b = 2
    print(s)

    try:
        s = DictObject(1)
        raise AssertionError
    except ValueError:
        pass

    try:
        s = DictObject(('a', 1))
        raise AssertionError
    except ValueError:
        pass

    print('Init with kwargs')

    s = DictObject(a=1)
    print(s)

    s = DictObject(a=1, b=2)
    print(s)

    s = DictObject()
    s.a = 1
    print(s)

    s = DictObject()
    s.a = 1
    s.b = 2
    print(s)

    s = DictObject(a=1)
    s.b = 2
    print(s)

    print('Init with tuples')
    s = DictObject((), ())
    print(s)

    s = DictObject(('a',), (1,))
    print(s)

    s = DictObject(('a', 'b'), (1, 2))
    print(s)

    try:
        s = DictObject(('a', 'b'), (1,))
        raise AssertionError
    except ValueError:
        pass

    try:
        s = DictObject(('a',), (1, 2))
        raise AssertionError
    except ValueError:
        pass

    print('Init with lists')
    s = DictObject([], [])
    print(s)

    s = DictObject(['a'], [1])
    print(s)

    s = DictObject(['a', 'b'], [1, 2])
    print(s)

    try:
        s = DictObject(['a', 'b'], [1])
        raise AssertionError
    except ValueError:
        pass

    try:
        s = DictObject(['a'], [1, 2])
        raise AssertionError
    except ValueError:
        pass

