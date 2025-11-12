file = open ("buffer.txt","r")

buffer = file.readlines()
file.close()
print(buffer)
print(buffer[0])
msft = buffer[0].split(",")
amzn = buffer[1].split(",")
nvda = buffer[2].split(",")
msft.pop(0)
amzn.pop(0)
nvda.pop(0)
print(msft)
print(amzn)
print(nvda)





