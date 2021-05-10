from uuid import uuid1
class Customer:
    def __init__(self,ID,Name):
        self.ID = ID
        self.Name = Name

    def getID(self):
        print("hi")
        return self.ID

    def getName(self):
        return self.Name

    def get_discount(self, price):
        pass

class RetailCustomer(Customer):

    def __init__(self,ID,Name,discount_rate,Total):
        super().__init__(ID,Name)
        self.discount_rate = float(discount_rate)
        self.Total = Total

    def get_discount(self,price):
        return float( price * self.discount_rate / 100.0)

    def displayCustomer(self):
        print("customer Details")

    def setRate(self,rate):
        self.discount_rate = rate

class WholesaleCustomer(Customer):
    def __init__(self,ID,Name,discount_rate1,Total):
        super().__init__(ID,Name)
        self.discount_rate1 = float(discount_rate1)
        self.discount_rate2 = float(discount_rate1) + float(5)
        self.Total = Total

    def get_discount(self, price):
        if price > 1000:
            return (float(price)* self.discount_rate2) / 100.0
        else:
            return (float(price)* self.discount_rate1) / 100.0

    def displayCustomer(self):
        print("wholesale customer")

    def getName(self):
        return 55

    def setRate(self,rate1):
        self.discount_rate1 = rate1
        self.discount_rate2 = rate1 +float(5)

class product():
    def __init__(self,ID,Name,Price,Stock):
        self.ID = ID
        self.Name = Name
        self.Price = Price
        self.Stock = int(Stock)
    def updateStock(self,qty):
        self.Stock = self.Stock -qty
    def printproduct(self):
        print(self.ID,"v,jndjv", self.Stock)




class order():
    orders =[]

    def makeorder(self):
        while True:
            try:
                Name = str(input("Enter the Customer name"))
                temp_cust = Records.findCustomer(self,Name)
                while temp_cust is None:
                    choice = str(input("User doesnt exit\n Do you wish to create the user Y/N ?"))
                    if choice == 'Y':
                        order.usercreate(self,Name)
                        print("User Created")
                        temp_cust = "done"
                    else:
                        return
                prd_Name = str(input("Enter the Product name"))
                temp = Records.findproduct(self,prd_Name)
                while temp is None:
                    prd_Name = str(input("Product doesn't exist . Please enter the valid Product name"))
                    temp = Records.findproduct(self,prd_Name)
                if float(temp["price"]) == float(0) or temp["price"].startswith('-'):
                    print("Order cannot be placed for this product with negative/no pricing")
                    return
                qty = int(input("Enter the Qty"))
                while qty > int(temp["Stk_Qty"]):
                    print("Available Quantity  : ", temp["Stk_Qty"])
                    qty = int(input("Enter the Qty"))
            except:
                print(" Enter the correct input")
            else:
                record = Records.findCustomer(self,Name)
                pro_record = Records.findproduct(self,prd_Name)
                custinstance = Records.custinst.get(record["Cust_id"])
                prodinstance = Records.prodinst.get(pro_record["prod_id"])
                if record["type"] == 'R':
                    if int(record["total"]) > 0:
                        discount = float(custinstance.get_discount(float(qty)* float(prodinstance.Price)))
                        total_price = float(qty)* float(prodinstance.Price) - discount
                        prodinstance.updateStock(qty)
                        Records.updateStk(self,pro_record["prod_id"],qty)
                        order.printorder(self,Name,qty,prd_Name,prodinstance.Price,total_price, prodinstance.Stock)
                        break
                    else:
                        total_price = float(qty)* float(prodinstance.Price)
                        prodinstance.updateStock(qty)
                        Records.updateStk(self,pro_record["prod_id"],qty)
                        order.printorder(self,Name,qty,prd_Name,prodinstance.Price,total_price, prodinstance.Stock)
                        break
                else:
                    if int(record["total"]) > 0:
                        discount = float(custinstance.get_discount(float(qty)* float(prodinstance.Price)))
                        total_price = float(qty)* float(prodinstance.Price) - discount
                        prodinstance.updateStock(qty)
                        Records.updateStk(self,pro_record["prod_id"],qty)
                        order.printorder(self,Name,qty,prd_Name,prodinstance.Price,total_price, prodinstance.Stock)
                        break
                    else:
                        total_price = float(qty)* float(prodinstance.Price)
                        prodinstance.updateStock(qty)
                        Records.updateStk(self,pro_record["prod_id"],qty)
                        order.printorder(self,Name,qty,prd_Name,prodinstance.Price,total_price, prodinstance.Stock)
                        break

    def usercreate(self,Name):
        type = str(input("Enter the Type (R/W) :"))
        ID = str(uuid1())
        val = {"Cust_id" : ID , "Cust_name" : Name , "type" : type,
               "disc_rate" : 0, "total" : 0}
        Records.custdata.append(val)
        if val["type"] == 'R':
            temp1 = val["Cust_id"]
            temp1  = RetailCustomer(val["Cust_id"],val["Cust_name"],val["disc_rate"],val["total"])
            Records.custinst.setdefault(val["Cust_id"],temp1)
        else:
            temp2  = val["Cust_id"]
            temp2 = WholesaleCustomer(val["Cust_id"],val["Cust_name"],val["disc_rate"],val["total"])
            Records.custinst.setdefault(val["Cust_id"],temp2)

    def printorder(self,Name,qty,prd_Name,Price,total_price, Stock):
        print( Name, " purchased ", qty, " x ",prd_Name)
        print("Unit Price ", Price)
        print("Total Price ",total_price)
        print("Remaining stock : " , Stock)
        temp = {"Cust_Name" : Name, "Prd_Name" : prd_Name, "Qty" : qty}
        order.orders.append(temp)

class Records():
    proddata = []
    custdata = []
    combdata = []
    custinst = {}
    prodinst = {}
    def readcustomers(self):
        try:
            file =open("customers.txt","r")
        except:
            print("File Read Error")
            exit(1)
        else:
            lineread = file.readline()
            while lineread:
                line =lineread.strip("\n").split(",")
                val = {"Cust_id" : line[0] , "Cust_name" : line[1] , "type" : line[2],
                       "disc_rate" : line[3], "total" : line[4]}
                self.custdata.append(val)
                lineread = file.readline()
            file.close()
            for data in self.custdata:
                if data["type"] == 'R':
                    temp = data["Cust_id"]
                    temp  = RetailCustomer(data["Cust_id"],data["Cust_name"],data["disc_rate"],data["total"])
                    self.custinst.setdefault(data["Cust_id"],temp)
                else:
                    temp  = data["Cust_id"]
                    temp = WholesaleCustomer(data["Cust_id"],data["Cust_name"],data["disc_rate"],data["total"])
                    self.custinst.setdefault(data["Cust_id"],temp)


    def updateStk(self,prd_id,qty):
        for data in Records.proddata:
            if prd_id == data["prod_id"]:
                data["Stk_Qty"] = str(int(data["Stk_Qty"]) - int(qty))
        for data in Records.combdata:
            if prd_id == data["comb_id"]:
                data["Stk_Qty"] = data["Stk_Qty"] - qty


    def readproducts(self):
        try:
            file =open("products.txt","r")
        except:
            print("File Read Error")
            exit(1)
        else:
            lineread = file.readline()
            while lineread:
                line =lineread.strip("\n").split(",")
                if line[0].startswith('P'):
                    val = {"prod_id" : line[0] , "prod_name" : line[1] , "price" : line[2],
                           "Stk_Qty" : line[3]}
                    self.proddata.append(val)
                    lineread = file.readline()
                else:
                    temp = []
                    i = 0
                    for data in line:
                        if i == 0 or i == 1 or i == line.__len__() - 1:
                            i = i+1
                            continue
                        else:
                            i = i+1
                            temp.append(data)
                    val = {"comb_id" : line[0] , "combo_name" : line[1] , "prd_list" : temp,
                           "Stk_Qty" : line[line.__len__() - 1]}
                    self.combdata.append(val)
                    lineread = file.readline()
            file.close()

            for data in Records.combdata:
                temp = data["comb_id"]
                temp = combo(data["comb_id"],data["combo_name"],data["prd_list"],data["Stk_Qty"])
                self.prodinst.setdefault(data["comb_id"], temp)
            for data in self.proddata:
                temp = data["prod_id"]
                temp = product(data["prod_id"],data["prod_name"],data["price"],data["Stk_Qty"])
                self.prodinst.setdefault(data["prod_id"],temp)


    def findCustomer(self,Value):
        for record in Records.custdata:
            if record["Cust_id"] == Value or record["Cust_name"] == Value:
                return record
        return None

    def findproduct(self,Value):
        for record in Records.proddata:
            if record["prod_id"] == Value or record["prod_name"] == Value:
                return record
        return None

    def listCustomers(self):
        for record in Records.custdata:
            print(list(record.values()))

    def listProducts(self):
        for record in Records.proddata:
            print(list(record.values()))

class combo():
    def __init__(self,Id,Name,pr_list,Stk):
        self.combo_id = Id
        self.Combo_Name = Name
        self.Prd_list = pr_list
        self.Stk_Qty = Stk

    def getprice(self):
        prices = []
        for prd in self.Prd_list:
            pro_record = Records.findproduct(self,prd)
            prodinstance = Records.prodinst.get(pro_record["prod_id"])
            prices.append(prodinstance.Price)
        Total = float(0)
        for price in prices:
            Total = Total + price
        return Total * float(0.9)

Records.readcustomers(self=Records)
Records.readproducts(self=Records)
while True:
    print("Menu\n1.List the Customer\n2.List the Product\n"
          "3..Make an order\n4.Append a Product to the product list\n5.Set prices for the products"
          "\n6.Make a purchase\n7.Replenish\n8.Valuable Customer\n9.Exit")
    try:
        choice = int(input("Enter the Choice :"))
    except:
        print("\nError, Please enter the correct option")
    else:
        if choice == 1:
            Records.listCustomers(self=Records)
        elif choice ==2:
            Records.listProducts(self=Records)
        elif choice ==3:
            order.makeorder(self=order)
        elif choice ==4:
            break