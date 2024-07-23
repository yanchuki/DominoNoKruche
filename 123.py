def power_count(a):
    abs = []
    for i in range(1, a + 1):
        if a % i == 0:
            abs.append(i)
    return sum(abs)

# print(power_count(10))

def recursion_power_count(a):
    if a == 1:
       return a
    return a + recursion_power_count(a - 1)

print(recursion_power_count(10))