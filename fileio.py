

file = open("names.txt","r")
            
buffer = file.readlines()
print(buffer)
file.close()

names = []
grades = []

for lines in buffer: 
    line = lines.strip()
    line = line.split(",")
    names.append(line)
    line[1] = int(line[1])
    grades.append(line[1])
print(names)
print(grades)