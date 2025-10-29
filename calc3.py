
check = False 
while check  == False:

   
    


    print("welcome to calculator!")
    print("1. addition")
    print("2. subtraction")
    print("3. multipliction")
    print("4. division")
    
   try:
        option = input("Enter your option addition subtraction division or multiplication. Type quit to exit: ")
        

    if option == "addition":
        x = input("add value for x:")
        x = int(x)
        y = input('add value for y:')
        y=int(y)
        z = x + y
        print(f'the sum of {x} and {y} is {z}')
    elif option == "subtraction":
        r = input("add value for r:")
        r = int(r)
        p = input('add value for p:')
        p =int(p)
        k = r - p
        print(f'the difference of {r} and {p} is {k}')
    elif option == "division":
        t= input("add value for t:")
        t = int(t)
        s = input('add value for s:')
        s =int(s)
        g = t / s
        print(f'the quotient {t} and {s} is {g}')
    elif option == "multipliction":
        b = input("add value for b:")
        b = int(b)
        c = input('add value for c:')
        c=int(c)
        m = b * c
        print(f'the product of {b} and {c} is {m}')
    elif option == "quit":
        check = True    
   except ValueError:
       print("you must enter a number")
   except ZeroDivisionError: 
       print("number 2 must not bbe zero 
    
 