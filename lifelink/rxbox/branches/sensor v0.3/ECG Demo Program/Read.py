data = open("data")
string = ''
temp = 'a'
while temp:
    temp = data.read()
    string += temp
    
print list(string)
