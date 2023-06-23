#!/usr/bin/python


"""
#!/usr/bin/env python
module to test equality, small interger caching in Python
"""

a = 1
b = 1

print(f'{a == b} \
       {a is b}')


d = 300
f = 300

print(f'{d == f} \
       {d is f}')

g = 'what the fuck'
h = 'what the fuck'

print(f'{g == h} \
       {g is h}')

aa = 250
bb = 250

print(aa == bb)
print(aa is bb)

ab = 258
ba = 258

print(ab == ba)
print(ab is ba)
