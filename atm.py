import pickle
import os
import time # for creating delays
import sys, traceback

# creates a tabular menu
def CreateMenu():
    print("Choose any option from 1-8")
    print("1. Withdrawal \t\t         2. check balance\n3. View transactions \t\t 4. Change pin\n5. Deposit cash \t\t 6.Prepaid recharge card")

# a simple animation to simulate loading
def proccesing():
    print("processing",end="")
    for i in range(0,5):
        print(".",end="",flush=True) #end is default to \n so changing it to "" and 
                                     #setting flush to True causes print to print to one line
        time.sleep(0.5)
    print("[DONE]")
    return


    
#function to save file
def save():
    UserFile = open(FileName, 'wb')
    pickle.dump(details,UserFile)
    UserFile.close()
    return

def deduct(amount,TransactionName):
    if amount == 0:
        while True:
            try:
                amount=int(input("How much do you want to withdraw? "))
                if amount <= 0:
                    print("Error, amount must be greater than 0")
                    raise Exception("")
                break
            except Exception as e:
                if e == ValueError:
                    print("please check what you typed")
                continue
            
    current_balance = details["balance"]
    if amount > current_balance and amount != 0:
        print("insufficient balance")

    elif amount >0:
        details["balance"] = current_balance-amount #update account balance
        save()
        #print a debit alert
        
        message="Debit alert\nTransaction: {}\nAmount withdrawn: {}\nBalance: {}".format(TransactionName,amount,details["balance"])
        
        return message  #new account balance
    

#for handling withdrwals
def Withdrawal():
    print("Choose from 1-8\n")
    while True:
        try:
            Input =int(input("1. 500 \t\t         2. 1000\n3. Urgent 2k \t\t 4. 5000\n5. 10000 \t\t 6. 15000\n7. 20000 \t\t 8. other\n"))
            MyDict={1:500, 2:1000, 3:2000, 4:5000, 5:10000, 6:15000, 7:20000, 8:0}
            # I used zero to represent 'other' since i cannot convert 'other' to an int
            if Input in range(1,8):
                 #if the user did not choose 'other'
                 proccesing()
                 message=deduct(MyDict[Input],"Withdrawal")
                 
            elif Input == 8:
                amount = int(input("How much do you want to withdraw? "))
                proccesing()
                message=deduct(amount,'Withdrawal')
                
            else:
                raise Exception("Invalid input\nPlease choose a number from 1-8")
            addTransaction(message)
            DoYouWantToPerformAnotherTransaction()
            
                 
        except Exception as e:
            if e != SystemExit:
                traceback.print_exc(file=sys.stdout)
                print("Error invalid input\nPlease choose a number from 1-8")
                continue
        break
    return
#function to save transactions to file
def addTransaction(message):
    print(message)
    details["transactions"].append(message) #stores record of transaction in a list
    save()
    return

def DoYouWantToPerformAnotherTransaction():
    while True:
        try:
            choice=int(input("Do you want to perfrom another transaction\n1. Yes \t\t 2. No\n"))
            if choice == 1:
                CheckInput()
                
            if choice == 2:
                sys.exit(0)
                         
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            if e != SystemExit:
                print("Invalid Input\nChoose either 1 or 2")
                continue #go back to the beginning of the loop 
    
     
def CheckBalance():
    proccesing()
    print("Your account balance is " + str(details["balance"]))
    DoYouWantToPerformAnotherTransaction()
    

def ViewTransactions():
    transactions=details["transactions"]
    proccesing()
    for i in range(len(transactions)):
        print(transactions[i]+"\n")
        
    DoYouWantToPerformAnotherTransaction()    
    

def ChangePin():
    while True:
        try:
            NewPin=input("Type in your new pin: ")
            if 4<len(NewPin)>4: #if len new pin is greater than 4 or less than 4
                raise Exception("pin must be a 4 digit number")
            
            details["pin"]=NewPin #update new pin
            proccesing()
            save()
            print("Your new pin is "+NewPin)
            break
            
        except Exception as e:
            print(e) #prints error message
            continue

def DepositCash():
    while True:
        try:
            amount=int(input("How much do want to deposit?: "))
            if amount<=0:
                raise Exception("Please insert a valid amount")
            proccesing()
            details["balance"]+=amount #add amount to balance
            save()
            addTransaction("Credit alert\nTransaction: Deposit\nDeposit: {}\nBalance: {}".format(amount,details["balance"]))
            DoYouWantToPerformAnotherTransaction()
            
        except Exception as e:
            print(e)
            continue
        
def PrepaidRechargeCard():
    while True:
        try:
            PhoneNumber, amount =input("Please type in your phone number and amount of recharge card you want to buy e.g +2349056149453, 1000: ").strip().split(",")
            amount=int(amount)
            proccesing()
            message=deduct(amount,'Prepaid Recharge card')
            print("\nYou have sucessfuly purchased {} naira recharge card for {}".format(amount,PhoneNumber))
            addTransaction(message)
            DoYouWantToPerformAnotherTransaction()
            
        
        except:
            
            print("error invalid input\nMake sure your input looks something like this +2349056149453, 1000")
            continue
            
            
                                                   
def CheckInput():
    CreateMenu()
    UserInput=""
    options={1:Withdrawal,2:CheckBalance,3:ViewTransactions,4:ChangePin,5:DepositCash,6:PrepaidRechargeCard}
    while True:
        try:
            UserInput=int(input("\n"))
            if UserInput < 0 or UserInput > 7:
                
                raise Exception("Invalid input\nPlease select a number from 1-7")
            
            options[UserInput]()
            break
            
        except Exception as e:
            print(e)
            continue
    return    
            
                            

            

 ######################### MAIN #################### MAIN #################### MAIN #########################
def main():
    while True:
        try:
            global FileName
            global UserFile
            global details
            
            name =input("PLease Insert your fullname: ").strip().lower()
            if not name:
                #check if name is empty
                #A tip: when you are dealing with EOF or something alike always remember that, 
                # to python, every null or empty or zero it's managed like a "false"... 
                # So you can put something like "while s:" because, 
                # if it's null or empty, will be false to python
                raise Exception("you did not type your name")
            for letter in name:
                if not letter.isspace() and not letter.isalpha():
                    raise Exception("Your name is invalid, pls check what you typed")
         
            pin=input("Pls insert your 4 digit pin: ").strip()
        
        
            if not pin.isdigit() or not len(pin) == 4: # check if pin is a digit and is =4 digits
                raise Exception("pin must a 4 digit number")
                
            FileName=name+".txt"
            
            #check if file exist
            if os.path.exists(FileName):
                #checkk if pin is correct
                #  if it is correct welcome 
                #  the user
                #import the dictionary
                UserFile = open(FileName, 'rb')
                details = pickle.load(UserFile)
                UserFile.close()

                if details['pin'] == pin:
                    break
                else:
                    print("invalid pin")
                    continue

            
             
            else:
                print("Welcome " + name)
                #welcome new user
                UserFile = open(FileName, 'wb')
            
                details={
                "balance" : 5000, "pin" : pin, "transactions" : []
                }
                pickle.dump(details,UserFile) #store file in binary form
                UserFile.close()
                break
        
            

        except Exception as e:
            print(e)
            
                
            continue
    return

 ######################### END OF MAIN #################### END OF MAIN #################### END OF MAIN #########################
  
main()
CheckInput()

