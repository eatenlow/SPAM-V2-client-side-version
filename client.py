import openpyxl
import datetime
from os import path, system, name
import shutil
import socket
from loginV2 import login, b


clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host='localhost'
clientsocket.connect((host, 8089))

class logins(login):
    def send_user(self):
        while self.done != True:
            self.UI()
        user = self.username
        clientsocket.send(user.encode())
        
class UiDesign:
    def clear(self): #to clear the screen so the UI looks cleaner and less messy/ cluttered
        if name == "nt":
            _ = system("cls")
        else:
            _ = system('clear')
    def printBanner(self, name, symbol): #to add a banner the width of the window (only works when running the program in command prompt, python shell won't clear)
        cols,rows = shutil.get_terminal_size()
        blue = "\033[33m"
        reset = '\033[m'
        print(blue + cols * symbol)
        print(blue + "{0:^{1}}".format(name,cols)) #to print name of page in center of the window
        print(blue + cols * symbol , reset)
        print("")
        
class SPAM:
    def __init__(self):
        self.cart = {}
        self.preordercart = {}
        self.menu = {}
        self.codeUsed = False
        self.total = 0
        self.preordered = {}

    def startup(self):
        self.discount = float(clientsocket.recv(5).decode())
        self.todaydate = clientsocket.recv(128).decode()
        self.receiver()
        while self.messageReceived != 'complete':
            self.receiver()
            temp = self.messageReceived.split(':')
            self.cart[temp[0]] = temp[1]

    def menuDecipher(self,menuString):
        self.menu = dict(p.split(':') for p in menuString.split(','))   #to split the long string of menu items into a dictionary
        
    def displayMenu(self,check):
        counter = 0
        if check == 1:
            tempcart = self.cart
        elif check == 2:
            tempcart = self.preordercart
        for food,price in self.menu.items():
            counter += 1
            print("{0:<1}. {1:20s}{3:6s}${2:.2f}".format(counter,food,float(price),":"))    #formatting printing of menu
        add2cart = 1
        while add2cart != '0':                
            add2cart = input(f"\nEnter the dish number that you would like to order, or 0 to stop: ")
            if ((add2cart.isnumeric() == False) or (int(add2cart) > counter) or (int(add2cart) < 0)):
                print("\nPlease enter a valid option!")
            elif add2cart == '0':
                break
            else:
                validQ = False
                while validQ == False:
                    quantity = (input("How many would like to order? "))
                    if quantity.isnumeric() == False:
                        print("Please enter a number between 1-100")
                    elif int(quantity) > 100 or int(quantity) < 1:
                        print("Please enter a number between 1-100")
                    else:
                        if list(self.menu)[int(add2cart)-1] not in tempcart:    #check if added item is already in cart
                            tempcart[list(self.menu)[int(add2cart)-1]] = int(quantity)
                            validQ = True
                        elif (tempcart[list(self.menu)[int(add2cart)-1]] + int(quantity)) > 100:    #limit amount user can order at once to 100 units
                            print("You may not order more than 100 portions of each dish")
                            validQ = True
                        else:
                            tempcart[list(self.menu)[int(add2cart)-1]] += int(quantity) #update cart if user's input is valid after above checks
                            validQ = True
        if check == 2:
            for key,value in list(tempcart.items()):
                self.preordercart[key] = str(value) + str((datetime.datetime.strptime(self.date, "%Y-%m-%d")).weekday())
            if len(self.preordercart) > 0:
                for key,value in self.preordercart.items():
                    if type(value) == int:
                        print('Your pre order cart currrently consists of:',key+" x",value)
                self.preordered[self.date] = self.menu
            else:
                print('Your pre order cart is currently empty')
        elif check == 1:
            self.cart.update(tempcart)
            if len(self.cart) > 0:
                for key,value in self.cart.items():
                    print ('Your cart currrently consists of:',key+" x",value)
            else:
                print('Your cart is currently empty')

        self.userInterface()

    def searchMenu(self):
        c.clear()
        found = False
        add2cart = 1
        c.printBanner("Item Search","*")
        while found == False:
            results = []
            counter = 0
            search = input("Please input food to search: ")
            print('')
            for food,price in self.menu.items(): #to search through dictionary storing menu items
                if search.lower() in food.lower():
                    counter += 1
                    found = True
                    results.append(food)
                    print("{0:<1}. {1:20s}{3:6s}${2:.2f}".format(counter,food,float(price),":"))
            if len(results) == 0:
                print("No results found")
                found = False
        while add2cart != '0':                
            add2cart = input(f"\nEnter the dish number that you would like to order, or 0 to stop: ")
            if ((add2cart.isnumeric() == False) or (int(add2cart) > counter) or (int(add2cart) < 0)):
                print("Please enter a valid option!")
            elif add2cart == '0':
                break
            else:  
                validQ = False
                while validQ == False:
                    quantity = (input("How many would like to order? "))
                    if quantity.isnumeric() == False:               #ensure user only enters numbers and no letters
                        print("Please enter a number between 1-100")
                    elif int(quantity) > 100 or int(quantity) < 1:  #ensure user enters a valid number
                        print("Please enter a number between 1-100")
                    else:
                        if results[int(add2cart)-1] not in self.cart:
                            self.cart[results[int(add2cart)-1]] = int(quantity)
                            validQ = True
                        elif self.cart[results[int(add2cart)-1]] + int(quantity) > 100:
                            print("You may not order more than 100 portions of each dish")
                        else:
                            self.cart[results[int(add2cart)-1]] += int(quantity)
                            validQ = True
        if len(self.cart) > 0:
            for key,value in self.cart.items():
                print ('Your cart currrently consists of:',key," x",value)
        else:
            print('Your cart is currently empty')
        self.userInterface()
        
    def displayCart(self,cart,check):
        valid = False
        if len(cart) > 0:
            if check == 2:
                for key,value in enumerate(cart,1):
                    for i in self.preordered.values():
                        self.menu = i
                        date = self.preordered[i]
                        if value in self.menu:
                            total = (float(self.menu[value]) * int(cart[value]))
                            print(f"{date}: {key}. {value}",(20 - len(value))*" ",f"x {cart[value]} ",(((25 - len(str(cart[value]))) - len("{value}"))*".")," ${0:.2f}".format(float(total))) #print cart item, quantity and price
                            
                input("Press any key to return to main menu")
                self.userInterface()
            else:
                for key,value in enumerate(cart,1):
                    total = (float(self.menu[value]) * int(cart[value]))
                    print(f"{key}. {value}",(20 - len(value))*" ",f"x {cart[value]} ",(((25 - len(str(cart[value]))) - len("{value}"))*".")," ${0:.2f}".format(float(total))) #print cart item, quantity and price
        else:
            print("Your cart is currently empty")
        while valid == False and check != 2:
            edit = input("Do you wish to edit your cart? (Y/N) ")
            if edit == "Y" or edit == 'y':
                valid = True
                if len(list(cart)) > 0 and check == 1: #check if cart is empty
                    self.editCart(cart,1)
                else:
                    print("Your cart is currently empty")
                    self.userInterface()
            elif edit == "N" or edit == 'n':    #return to main menu if user enters N or n
                valid = True
                self.userInterface()
            else:
                valid = False
                print("Invalid input!")
        
    def checkOut(self):
        self.total = 0
        self.noDistotal = 0 #to store undiscounted total to prevent errors in applying discount multiple times
        c.clear()
        c.printBanner("Your Bill","-")
        counter = 0
        if self.discount != 1:                              #to check if admin promo code was applied
            for key,value in enumerate(self.cart,1):        #formatting printing of cart
                print(f"{key}. {value}",(20 - len(value))*" ",f"x {self.cart[value]} ",(((25 - len(str(self.cart[value]))) - len("{value}"))*".")," ${0:.2f}".format(float(self.menu[value])*float(self.discount)*self.cart[value]))
                self.total += (float(self.menu[value]) * self.cart[value] * self.discount)
                self.noDistotal += (float(self.menu[value]) * self.cart[value])
            print("\nDiscount: ${0:.2f}".format(self.noDistotal - (self.discount * self.noDistotal)))        
            print("Your Total is: $" + "{0:.2f}".format(self.total))
            edit = input("Would you like to make changes to your cart? (Y/N) ")
            if edit == 'Y' or edit == 'y':
                self.editCart()
            else:
                proceed = input("Would you like to proceed to payment? checkout0 (Y/N): ")
            validP = False
            while validP == False:
                if proceed == "Y" or proceed == 'y':
                    self.payment()
                    validP = True
                elif proceed == "N" or proceed == 'n':
                    self.userInterface()
                    validP = True
                else:
                    print("Invalid input!")
                    proceed = input("Would you like to proceed to payment? checkout1(Y/N): ")   
        else:
            for key,value in enumerate(self.cart,1):
                    print(f"{key}. {value}",(20 - len(value))*" ",f"x {self.cart[value]} ",(((25 - len(str(self.cart[value]))) - len("{value}"))*".")," ${0:.2f}".format(float(self.menu[value])*self.cart[value]))
                    self.noDistotal += float(self.menu[value]) * self.cart[value]

            
    def editCart(self,cart,check):
        valid = False
        while valid == False: #to allow the user to choose whether to remove, increase or decrease quantity of in cart items
            c.clear()
            c.printBanner("Cart Editor","*")
            for key,value in enumerate(cart,1):
                total = (float(self.menu[value]) * int(cart[value]))
                print(f"{key}. {value}",(20 - len(value))*" ",f"x {cart[value]} ",(((25 - len(str(cart[value]))) - len("{value}"))*".")," ${0:.2f}".format(float(total))) #print cart item, quantity and price
            editor = eval(input("""
Please enter
(1) to add to cart,
(2) to decrease number of portions,
(0) to exit: """))

            if editor == 2:
                validE = False
                while validE == False:
                    edit = input("Please enter the number of item you wish to remove: ")
                    if(edit.isnumeric() == False or edit == ''):
                        print("Invalid Input")
                        validE = False
                    elif int(edit) < 1 or int(edit) > len(list(cart)):
                        print("Invalid Input")
                        validE = False
                    else:
                        validE = True
                portions = cart[list(cart)[int(edit)-1]]
                c.clear()
                c.printBanner("Cart Editor","*")
                remove = input("How many would you like to remove: ")
                while remove.isnumeric == False or int(remove) < 0:
                    remove = input("How many would you like to remove: ") #input validation
                if portions - int(remove) >= 0:
                    cart[list(cart)[int(edit)-1]] -= int(remove)
                    print(f"{list(cart)[int(edit)-1]} x {cart[list(cart)[int(edit)-1]]}")
                elif portions == 0:
                    print("You no longer have that item in the cart")
                    del cart[list(cart)[int(edit)-1]]
                elif portions - int(remove) < 0:
                    print("You can't remove more than you have added into your cart.") #input validation
            elif editor == 0:
                self.userInterface()
                valid = True
            elif editor == 1:
                self.menuDecipher(self.todaymenu)       #to obtain today menu in a printable form
                self.displayMenu(1)
                self.editCart(cart)
            else:
                print("Invalid Input!")

                
    def payment(self):
        if self.discount != 1:
            print("Thank you for using SPAM, Please pay ${0:.2f}".format(self.total))
        else:
            print("Thank you for using SPAM, Please pay ${0:.2f}".format(self.noDistotal))

        if len(self.preordercart) > 0:
            self.reply("preorder")
            preorders = ''
            for key,value in (self.preordercart.items()):       #to send any pre ordered items to server
                preorders += (str(key)+":"+str(value)+",")
            self.reply(preorders[0:len(preorders)-1])
        else:
            self.reply('bill')
            logs = ''
            for key,value in enumerate(self.cart,1):            #to send ordered items to server
                logs += (f"{value}:{self.cart[value]},")
            self.reply(logs[0:len(logs)-1])
        self.cart.clear                                         #clear cart for next order
        
    def reply(self,msg):
        sent = str(msg).encode()
        clientsocket.send(sent)

    def receiver(self):
        reply = clientsocket.recv(1024)
        self.messageReceived = reply.decode()

    def preorder(self):
        validnum = False
        while validnum == False:
            displayDay = input(f"""
1. Monday
2. Tuesday
3. Wednesday
4. Thursday
5. Friday
6. Saturday
7. Sunday

Please input your choice of day (0 to exit): """)
            if displayDay.isnumeric()==False or int(displayDay)>7 or int(displayDay)<0:
                validnum = False
            elif displayDay == '0':
                self.userInterface()
                validnum = True
            else:
                c.clear()
                self.reply(displayDay)
                self.receiver()
                self.date = self.messageReceived
                c.printBanner(f"Menu for {self.date}","=")
                self.receiver()
                self.menuDecipher(self.messageReceived)
                self.displayMenu(2)
                validnum = True
                
    def userInterface(self):
        c.clear()
        valid = False
        while valid != True:
            c.printBanner("Welcome to SPAM","*")
            choice = input("""1. Display Today's Menu
2. Search Menu
3. Display Cart
4. Check Out
5. Preorder
6. Display Preorder Cart
7. Shutdown server
    
Please input your choice of action (ENTER to exit): """) 
            if choice.isnumeric() == True and (int(choice) > 0 and int(choice) < 8): #check for which option the user had chosen
                  if int(choice) == 1:
                      self.reply("1")
                      self.receiver()
                      self.todaymenu = self.messageReceived     #client receives date from server
                      self.menuDecipher(self.todaymenu)
                      valid = True
                      c.clear()
                      c.printBanner(f"Menu","=")
                      self.displayMenu(1)
                  elif int(choice) == 2:
                      self.reply("2")
                      self.receiver()
                      self.menuDecipher(self.messageReceived)
                      self.menuDecipher(self.todaymenu)     #to ensure menu variable is containing today's menu and not the other days' menu
                      valid = True
                      self.searchMenu()
                  elif int(choice) == 3:
                      self.reply('3')
                      valid = True
                      c.clear()
                      c.printBanner("Your Cart","-")
                      self.menuDecipher(self.todaymenu)
                      self.displayCart(self.cart,1)
                  elif int(choice) == 4:
                      self.reply('Checkout')
                      self.receiver()
                      self.todaymenu = self.messageReceived
                      valid = True
                      self.menuDecipher(self.todaymenu)
                      print(self.todaymenu)
                      self.checkOut()
                      self.payment()
                  elif int(choice) == 5:
                      self.reply('5')
                      self.preorder()
                      valid = True
                  elif int(choice) == 6:
                      self.reply('6')
                      c.clear()
                      c.printBanner("Your Preorder Cart","-")
                      a={}
                      for key,value in self.preordercart.items():
                          a[key] = value
                      self.displayCart(a,2)
                      
                  elif int(choice) == 7:
                      self.reply("shutdown")
                      valid = True
                      print("disconnecting...")
                      clientsocket.close()
            elif choice == '':
                orderAgain = False
                print("Invalid Input!")
                break
            else:
                print("Invalid Input!")
                valid = False


d = logins()
d.send_user()
orderAgain = True
c = UiDesign()
a = SPAM()
a.startup()
while orderAgain == True:
    a.userInterface()
    checkAgain = input("\nWould you like to make a new order? (Y/N): ")
    if checkAgain == "y" or checkAgain == "Y":
        orderAgain = True
    elif checkAgain == 'n' or checkAgain == "N" or checkAgain == '':
        orderAgain = False
        a.reply("DC")
print("Goodbye, See you again!")

