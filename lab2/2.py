def f1(a):
    return 1


def f2(a):
    return 2


def f3(a):
    return 3


def composed(*functions):
    def func(s):
        a = list(functions)
        res = []
        for i in range(len(a) - 1, -1, -1):
            a[i](s)
            res += [a[i](s)]
        return res

    return func


print(composed(f1, f2, f3)(1))
