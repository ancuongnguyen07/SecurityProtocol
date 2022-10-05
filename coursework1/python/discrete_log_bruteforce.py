# Find x in a^x = b mod q, where a,b,q are known

a = 7
b = 10
q = 11

x = 0
while a**x % q != b:
    x += 1

print(x)