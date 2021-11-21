from disorders import disorder


test_table_one = [
    [0, 1, 2, 3, 4, 5, 6, 7],
    ["a", "b", "c", "d", "e", "f"],
    ["aplha", "beta", "gamma", "delta", "epsilon", "zeta"],
    ["foxtrot", "uniform", "charlie", "kilo", "Yankee", "Oscar", "Uniform"],
]

def disorder_test(function, table):
    for xs in table:
        ys = function(xs)
        
        for i in range(len(xs)):
            assert(xs[i] != ys[i])
                # print("WTF&^!&!&!&!7")

            print('{:<8} -> {:>8}'.format(xs[i], ys[i]))

        # print(xs)
        # print(ys)
        print()

disorder_test(disorder, test_table_one)
