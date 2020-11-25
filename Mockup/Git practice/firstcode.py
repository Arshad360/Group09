print('This is a test code')

a = 5
b = 4
c = 2

# Calculate the semi-perimeter

s = (a+b+c)/2

# Area Calculation

area = (s*(s-a)*(s-b)*(s-c)) ** 0.5

print('The area of the triangle is %0.2f' %area)
