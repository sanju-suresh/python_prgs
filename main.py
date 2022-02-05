import pickle
import logging
from logging import Logger


class CARD:

    def checkAcc(accno):
        f = 0
        accdata = pickle.load(open("accdata.dat", "rb"))
        # in this program the account id password and account balance is being saved in a 2d array in a file named accdata.dat in first column all ids 2nd column
        # contains all the pins of the ids in the same row and the 3rd column containing the corresponding account balances
        for i in accdata:
            if i[0] == accno:
                f = 1
                break

        if f == 0:
            return False
        else:
            return True

    def checkPin(accno, pin):
        f = 0;
        accdata = pickle.load(open("accdata.dat", "rb"))
        for i in accdata:
            if i[0] == accno:
                if i[1] == pin:
                    f = 1
                break

        if f == 0:
            return False
        else:
            return True


class USER:
    def setPin(accno, pin):
        accdata = pickle.load(open("accdata.dat", "rb"))
        accdata.append([accno, pin, 0])
        pickle.dump(accdata, open("accdata.dat", "wb"))


class ACCOUNT():

    def deposit(accno, num):
        accdata = pickle.load(open("accdata.dat", "rb"))

        for i in accdata:
            if i[0] == accno:
                i[2] += int(num)
                pickle.dump(accdata, open("accdata.dat", "wb"))
                return i[2]

    def withdraw(accno, num):
        accdata = pickle.load(open("accdata.dat", "rb"))

        for i in accdata:
            if i[0] == accno:
                if int(num) > i[2]:
                    return [0, i[2]]
                else:
                    i[2] -= int(num)
                    pickle.dump(accdata, open("accdata.dat", "wb"))
                    return [1, i[2]]


class ATM:
    formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler('logdata.log')
    file_handler.setFormatter(formatter)
    stream_handler = logging.StreamHandler()
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    accdata = pickle.load(open("accdata.dat", "rb"))
    accno = input("Please insert card and enter account number:")
    if CARD.checkAcc(accno):
        pin = input("Please enter pin number :")
    else:
        pin = input("Please set pin number :")
        USER.setPin(accno, pin)

    if CARD.checkPin(accno, pin):
        print('''1 - DEPOSIT
2 - WITHDRAW
3 - VIEW BALANCE
     
ENTER CHOICE''')

        choice = input()
        if choice == "1":
            num = input("Enter amount to be deposited :")
            bal = ACCOUNT.deposit(accno, num)
            logger.info(f'''Transaction Successful from ID : {accno}
Current Balance : {bal}
{num} has been deposited in account''')


        elif choice == "2":
            num = input("Enter amount to be withdrawn :")
            p = ACCOUNT.withdraw(accno, num)

            if p[0] == 1:
                logger.info(f'''Transaction Successful from ID : {accno}
Current Balance : {p[1]}
{num} has been withdrawn from account''')
            else:
                logger.info(f'''Transaction failed. Account balance is not enough
Current Balance : {p[1]}''')
        elif choice == "3":
            for i in accdata:
                if i[0] == accno:
                    logger.info(f'''ID :{accno}
Current Balance :{i[2]}''')
        else:
            print("Invalid choice")
    else:
        logger.warning("Invalid pin")
