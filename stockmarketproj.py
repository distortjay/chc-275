file = open "buffer.txt","r"

buffer.file = file.readlines()
file.close()
print(buffer)
print(buffer[0])
msft = buffer[0]