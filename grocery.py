file = open("grocery.txt" , "r")
buffer = file.readlines()
food = []
price = []
cart = []

for line in buffer:
   line = line.strip()
   line = line.split(",")
   food.append(line[0])
   line[1] = float(line[1])
   price.append(line[1])
total = 0
check = False
while check == False:
    print("Welcome To The Grocery Store")
    print("1. add to cart")
    print("2. remove items")
    print("3. check out")
    option = input('What is your selection: ')
    try:
        if option == 1 or option == "1":
            print(food)
            print(price)
            purchase = input("which food you would like to purchase: ").strip()
            purchase = int(purchase)
            amount = input(f'Enter the amount of {food[purchase]} you would like to purchase:')
            amount = int(amount)
            for i in range(amount):
                cart.append(food[purchase])
            total = total + amount * price[purchase]
            print("your total is " + str(total))
        
           
            
        if option == 2 or option == "2":
            print(cart)
            purchase = input("which food you would like to remove: ").strip()
            purchase = int(purchase)
            amount = input(f'Enter the amount of {food[purchase]} you would like to remove:')
            amount = int(amount)
            for i in range(amount):
                if food[purchase] in cart:
                    cart.remove(food[purchase])
                    total = total - price[purchase]
            print("your total is " + str(total))
            
            
    
         
                
        if option == 3 or option == "3":
            tax = total * 0.06
            total = total + tax
            print("your total is " + str(total))
            check = True   
                

            
      
    except ValueError:
        print ("x and y must be numbers")
    except ZeroDivisionError:
        print ("y must be nonzero")
    except Exception as e:
        print(e)
 