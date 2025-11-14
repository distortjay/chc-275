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



for i in range  (len(msft)):
    
    msft[i]= int (msft[i])
    amzn[i] = int (amzn[i])
    nvda[i] = int (nvda[i])
m1 = sum(msft) / len(msft) 
a1 = sum(amzn) / len(amzn)
n1 = sum(nvda) / len(nvda)

file = open ("buffer2.txt","r")

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



for i in range  (len(msft)):
    
    msft[i]= int (msft[i])
    amzn[i] = int (amzn[i])
    nvda[i] = int (nvda[i])
m2 = sum(msft) / len(msft) 
a2 = sum(amzn) / len(amzn)
n2 = sum(nvda) / len(nvda)

buys = []
print(m1,m2)
print(a1,a2)
print(n1,n2)

if m2 > m1:
    buys.append("msft")
    print(1)
if a2 > a1:
    buys.append("amzn")
    print(2)
if n2 > n1:
    print(3)
    buys.append("nvda")


print(buys)

line0 = f"msft {m1} {m2} \n"
line1 = f"amzn {a1} {a2} \n"
line2 = f"nvda {n1} {n2} \n"
line3 = f'buys {buys}'
buffer = [line0, line1, line2, line3]
file = open("report.txt" , "w") 
file.writelines(buffer)
file.close()