import requests
import json
import base64
from addresses import DC01_address, DC11_address

X_Zsc_Authorization = 'suzuki:0000'
X_Zsc_Authorization = bytearray(X_Zsc_Authorization, 'utf-8')
X_Zsc_Authorization = base64.b64encode(X_Zsc_Authorization)
X_Zsc_Authorization = X_Zsc_Authorization.decode("UTF-8")
X_Zsc_Authorization

# #New_TEST inventory. takes so long to download
# #Login and obtain a token
# url_login = 'https://zaikos.azure-api.net/zsc/beautygarage/login'
# header_login = { 'Ocp-Apim-Subscription-Key' : '253ae2b9815f44f8952a42e781ca362a','X-Zsc-Subscription' : 'beautygarage2','Cache-Control' : 'no-cache','X-Zsc-Authorization' : 'MDA3MTowMDcx' }
# r = requests.post(url_login , headers= header_login)
# r.encoding = 'utf-8-sig' #server encoding is not UTF-8 (probably). if this is removed some strange characters show up in Token.
# jToken = json.loads(r.text)

# #Obtain the inventory data
# url_inv = "https://zaikos.azure-api.net/zsc/beautygarage/stocks_summary"
# SubKey_Token = { "Ocp-Apim-Subscription-Key" : "253ae2b9815f44f8952a42e781ca362a",'X-Zsc-Subscription' : 'beautygarage2',"X-Zsc-Token" : jToken['token'] }


#faster inventory
#Login and obtain a token
url_login = 'https://zaikos.azure-api.net/zsc/beautygarage/login'
header_login = { 'Ocp-Apim-Subscription-Key' : '253ae2b9815f44f8952a42e781ca362a','Cache-Control' : 'no-cache','X-Zsc-Authorization' : 'MjAzMjoyMDMy' }
r = requests.post(url_login , headers= header_login)
r.encoding = 'utf-8-sig' #server encoding is not UTF-8 (probably). if this is removed some strange characters show up in Token.
jToken = json.loads(r.text)

#Obtain the inventory data
url_inv = "https://zaikos.azure-api.net/zsc/beautygarage/stocks_summary"
SubKey_Token = { "Ocp-Apim-Subscription-Key" : "253ae2b9815f44f8952a42e781ca362a", "X-Zsc-Token" : jToken['token'] }


#DC01
query = {'warehouseCode': '01' , 'keycode' : ''}
r_inv = requests.get(url_inv , headers=SubKey_Token , params=query)
f = open(DC01_address, "w")
f.write(r_inv.text.lstrip('\ufeff'))
f.close()

#DC11
query = {'warehouseCode': '11' , 'keycode' : ''}
r_inv = requests.get(url_inv , headers=SubKey_Token , params=query)
f = open(DC11_address, "w")
f.write(r_inv.text.lstrip('\ufeff'))
f.close()

#Logout
url_out = 'https://zaikos.azure-api.net/zsc/beautygarage/logout'
r = requests.post(url_out , headers=SubKey_Token)
sLogout = "Logout " + r.text
print(sLogout)


####################################################SORTING ORDERS##########################################################
import pandas as pd
import csv
import sys
from addresses import DC01_address, DC11_address, Order_address, Order_address_source, PostCode_address, Output_DCx1_address, Output_DCx1_address_west


#This is the header for the East inventory
header= ["DC_Code","DC_Name","barcode","stock_no","description_1","description_2","category","category_name","total_inventory","shipping_qty","allocate_qty","blocked_qty","available_qty","arrival_qty","expected_inventory","order_point","unit","uodate_date"]

#The following adds the header above to the first line of the file.
with open(DC01_address, newline='', encoding="shift_jis_2004") as f:
    r = csv.reader(f)
    data = [line for line in r]
with open(DC01_address,'w',newline='', encoding="shift_jis_2004") as f:
    w = csv.writer(f)
    w.writerow(header)
    w.writerows(data)  
 

#The following adds the header above to the first line of the file.
with open(DC11_address,newline='', encoding="shift_jis_2004") as f:
    r = csv.reader(f)
    data = [line for line in r]
with open(DC11_address,'w',newline='', encoding="shift_jis_2004") as f:
    w = csv.writer(f)
    w.writerow(header)
    w.writerows(data)  

df_inv_east = pd.read_csv(DC01_address, usecols=["DC_Name","stock_no","available_qty"])
df_inv_east.columns=["InverntoryName",  "Item code", "NumItemsAvailable"] #renames the columns
#convert negative numbers to zero in NumItemsAvailable
df_inv_east.NumItemsAvailable = df_inv_east.NumItemsAvailable.mask(df_inv_east.NumItemsAvailable.lt(0),0)

df_inv_west = pd.read_csv(DC11_address, usecols=["DC_Name","stock_no","available_qty"])
df_inv_west.columns=["InverntoryName",  "Item code", "NumItemsAvailable"] #renames the columns
#convert negative numbers to zero in NumItemsAvailable
df_inv_west.NumItemsAvailable = df_inv_west.NumItemsAvailable.mask(df_inv_west.NumItemsAvailable.lt(0),0)

#This is the header for the Shipping order file
header_order = ["Shipping_Order_No","Voucher_Class","Order_Date","Delivery_Date","Planed_Ship_Date","DC_Code","DC_Name","Customer_Code","Customer_Name1","Customer_Name2","Data_11","Data_12","Data_13","Data_14","Customer_Zip_Code","Customer_address1","Customer_address2","Customer_TEL","Customer_FAX","Order_No","Transport_Company","Receiver_Code","Receiver_Name1","Receiver_Name2","Data_25","Data_26","Data_27","Data_28","Receiver_Zip_Code","Receiver_address1","Receiver_address2","Receiver_TEL","Receiver_FAX","Consumption_TAX","Data_35","Data_36","Mail_address","Point","Data_39","SAP_Shipping_No","Data_41","Working_Condition","Balance","Data_44","Data_45","Data_46","Data_47","Update_date","Detail_No","Data_50","Stock_No","BarCode","Location","Description1","Description2","Pcs_Per_case","Case_No","Quantity","Units","Lot1","Lot2","Status_Code","Status","Data_64","Data_65","Data_66","Warranty","Data_68","Data_69","Detail_Update_date"]

#The following adds the header above to the first line of the file.
with open(Order_address_source,newline='', encoding="shift_jis_2004") as f:
    r = csv.reader(f)
    data = [line for line in r]
with open(Order_address,'w',newline='',encoding="shift_jis_2004") as f:
    w = csv.writer(f)
    w.writerow(header_order)
    w.writerows(data)

df_order = pd.read_csv(Order_address, encoding="shift_jis_2004",converters={'Receiver_Zip_Code': lambda x: x.strip('”'),'Shipping_Order_No': lambda x: x.strip('”'),'Stock_No': lambda x: x.strip('”'),'Quantity': lambda x: int(x.strip('”')), 'Receiver_TEL': lambda x: str(x) })
df_order = df_order.rename(columns={'Stock_No': 'item code', 'Quantity' : 'NumItemsNeeded'}) #I will just rename these columns since at earler versions of the code these names were used and changing them in the code now, might alter the dynamics.

df_postal = pd.read_csv(PostCode_address, converters={'Zip_Code 3degit': lambda x: str(x)}, usecols= ["Zip_Code 3degit", "East/West"]) #Reading the Post code file
df_postal.columns=["PostCode", "East_West"] #renames the columns
df_postal = df_postal.drop_duplicates(keep='first')#probably not needed


#Let's import these data into a class for better access
class order:
    def __init__(self, order_num, zipcode, items): 
        self.order_num = order_num        
        self.zipcode = zipcode
        self.items = items #items is gonna be a list of class item

OrderNumbers = df_order["Shipping_Order_No"].unique().tolist() #A list with all the order numbers inside it (unique)
zipcodes = df_order["Receiver_Zip_Code"].unique().tolist() #A list with all the Zipcodes inside it (unique) not necessarily the same size as OrderNumbers

List_of_index_orders = [] #This list will contain the indexes (i.e. rows) for each shipping number. 
for i in OrderNumbers:
    List_of_index_orders.append(df_order.index[df_order["Shipping_Order_No"] == i].tolist())

#This function create the list_items
def get_items(List_of_index_orders):    
    availibility = False #default values of availibility
    inv_loc = "unknown" #default values of location
    
    list_items = list()
    temp = list()
    for i in range(len(List_of_index_orders)):
        for j in  List_of_index_orders[i]:
            temp.append([df_order.at[j,'item code'],df_order.at[j,'NumItemsNeeded'],availibility,inv_loc,\
                        [df_order.at[j,'Voucher_Class'],df_order.at[j,'Order_Date'],df_order.at[j,'Delivery_Date'],df_order.at[j,'Planed_Ship_Date'],\
                        df_order.at[j,'DC_Code'],df_order.at[j,'DC_Name'],df_order.at[j,'Customer_Code'],df_order.at[j,'Customer_Name1'],\
                        df_order.at[j,'Customer_Name2'],df_order.at[j,'Data_11'],df_order.at[j,'Data_12'],df_order.at[j,'Data_13'],\
                        df_order.at[j,'Data_14'],df_order.at[j,'Customer_Zip_Code'],df_order.at[j,'Customer_address1'],df_order.at[j,'Customer_address2'],\
                        df_order.at[j,'Customer_TEL'],df_order.at[j,'Customer_FAX'],df_order.at[j,'Order_No'],df_order.at[j,'Transport_Company'],\
                        df_order.at[j,'Receiver_Code'],df_order.at[j,'Receiver_Name1'],df_order.at[j,'Receiver_Name2'],df_order.at[j,'Data_25'],\
                        df_order.at[j,'Data_26'],df_order.at[j,'Data_27'],df_order.at[j,'Data_28'],\
                        df_order.at[j,'Receiver_address1'],df_order.at[j,'Receiver_address2'],df_order.at[j,'Receiver_TEL'],df_order.at[j,'Receiver_FAX'],\
                        df_order.at[j,'Consumption_TAX'],df_order.at[j,'Data_35'],df_order.at[j,'Data_36'],df_order.at[j,'Mail_address'],\
                        df_order.at[j,'Point'],df_order.at[j,'Data_39'],df_order.at[j,'SAP_Shipping_No'],df_order.at[j,'Data_41'],\
                        df_order.at[j,'Working_Condition'],df_order.at[j,'Balance'],df_order.at[j,'Data_44'],df_order.at[j,'Data_45'],\
                        df_order.at[j,'Data_46'],df_order.at[j,'Data_47'],df_order.at[j,'Update_date'],df_order.at[j,'Detail_No'],\
                        df_order.at[j,'Data_50'],df_order.at[j,'BarCode'],df_order.at[j,'Location'],\
                        df_order.at[j,'Description1'],df_order.at[j,'Description2'],df_order.at[j,'Pcs_Per_case'],df_order.at[j,'Case_No'],\
                        df_order.at[j,'Units'],df_order.at[j,'Lot1'],df_order.at[j,'Lot2'],\
                        df_order.at[j,'Status_Code'],df_order.at[j,'Status'],df_order.at[j,'Data_64'],df_order.at[j,'Data_65'],\
                        df_order.at[j,'Data_66'],df_order.at[j,'Warranty'],df_order.at[j,'Data_68'],df_order.at[j,'Data_69'],\
                        df_order.at[j,'Detail_Update_date']]   ]) #these other information has to be in a list because I have to write down an _ later on
                        #update,v111: data 35 now will named EW to indicate that an order has been split or not
        list_items.append(temp.copy())
        temp.clear()
    return list_items     


list_items = get_items(List_of_index_orders)

#Creating the classes now
orders = list()

# Better to put an if loop here to make sure len(List_of_index_orders) = len(list_items)
for i in range(len(List_of_index_orders)):
    OrderNumber = OrderNumbers[i]
    Zipcode = df_order.at[List_of_index_orders[i][0],"Receiver_Zip_Code"]
    Items = list_items[i]
    orders.append(order(OrderNumber,Zipcode,Items))


#------------------Importing done! let's define the functions we need.----------------------
def remove_duplicates(order): #Check for any duplicates of items of an order
    duplicates = list()
    for i in range(len(order.items)):
        for j in range(i+1,len(order.items)):
            if(order.items[i][0] == order.items[j][0]):
                if(order.items[j] not in duplicates):
                    order.items[i][1] = order.items[i][1] + order.items[j][1]
                    duplicates.append(order.items[j])
    for item in duplicates:
        #print("removing", item)
        order.items.remove(item)

def EastOrWest(order):
    FirstThreeDigit = str(order.zipcode)[:3] #gets the first three digits of input ZipCode
    if(df_postal["PostCode"].tolist().count(FirstThreeDigit)>0):
        #print("Code exists in the list.")
        index_postalCode = df_postal.index[df_postal['PostCode'] == FirstThreeDigit].tolist()[0]    
        if(df_postal.at[index_postalCode,'East_West'].strip()=="East"): #strip() removes the spaces at the begining and the end
            #print("Zipcode is for East.")
            return 1 # returns 1 for East and 0 for West
        elif(df_postal.at[index_postalCode,'East_West'].strip()=="West"):
            #print("Zipcode is for West.")
            return 0 # returns 1 for East and 0 for West
    else:
        #raise NameError('First three digits', str(FirstThreeDigit), 'was not found in postal code list.')
        #print('First three digits', str(FirstThreeDigit), 'was not found in postal code list. \nSending order number ',order.order_num,'to east.')
        return 1

def update_inv(order): #this function will updates inventory 
    for item in order.items:
        if(item[3] == 'East'): #item[3] is the location  variable
            Index_item_inv_east = df_inv_east.index[df_inv_east['Item code'] == item[0]].tolist()[0] #index of the item in inventory list 
            df_inv_east.at[Index_item_inv_east , 'NumItemsAvailable'] = df_inv_east.at[Index_item_inv_east , 'NumItemsAvailable'] - item[1]
        
        elif(item[3] == 'West'): #item[3] is the location  variable
            Index_item_inv_west = df_inv_west.index[df_inv_west['Item code'] == item[0]].tolist()[0] #index of the item in inventory list 
            df_inv_west.at[Index_item_inv_west , 'NumItemsAvailable'] = df_inv_west.at[Index_item_inv_west , 'NumItemsAvailable'] - item[1]
        else:
            raise NameError("something is wrong with updating inv for order:", order.order_num)
           
def Item_available_east(Item_code, Num_items_ordered):
    List_of_items_inventory = df_inv_east['Item code'].tolist()
    if(Item_code in List_of_items_inventory):
        Inv_index_item = df_inv_east.index[df_inv_east['Item code'] == Item_code].tolist()[0] #index of the item in inventory list 
        #print("Index of item ", Item_code, " is ",Inv_index_item,"in inventory list.")
        Num_avil_item = df_inv_east.at[Inv_index_item,'NumItemsAvailable'] #number of available items in inventory
        #print("There are ", Num_avil_item, " items available and", Num_items_ordered  ,"needed for item", Item_code)
        
        if(Num_avil_item - Num_items_ordered >= 0): #checks if there are enough items in the inventory.
            #print("Enough items are available for item ", Item_code,". \nNow there are ", Num_avil_item - Num_items_ordered, "left in inventory." )
            return 1
        else:
            #print("There is not enough items in East inventory",Item_code,".\nMissing number =", Num_avil_item - Num_items_ordered)
            return 0
        
    else:
        Items_not_in_inv_east.append(Item_code)
        #print('One items', Item_code, 'was not found in east inventory.')
        
def check_inv_east(order):
    for item in order.items:
        if(item[2] == False):
            if(Item_available_east(item[0],item[1])): #item[0] = Code, item[1] = Num_items_ordered
                item[2] = True #availability
                item[3] = "East" #Location
    if(all( availability == 1 for (_, _, availability,_,_) in order.items)):
        return 1 #Some or all items are avaible in East_inv 
    else:
        return 0

def Item_available_west(Item_code, Num_items_ordered):
    List_of_items_inventory = df_inv_west['Item code'].tolist()
    if(Item_code in List_of_items_inventory):
        Inv_index_item = df_inv_west.index[df_inv_west['Item code'] == Item_code].tolist()[0] #index of the item in inventory list 
        #print("Index of item ", Item_code, " is ",Inv_index_item,"in inventory list.")
        Num_avil_item = df_inv_west.at[Inv_index_item,'NumItemsAvailable'] #number of available items in inventory
        #print("There are ", Num_avil_item, " items available and", Num_items_ordered  ,"needed for item", Item_code)
        
        if(Num_avil_item - Num_items_ordered >= 0): #checks if there are enough items in the inventory.
            #print("Enough items are available for item ", Item_code,". \nNow there are ", Num_avil_item - Num_items_ordered, "left in inventory." )
            return 1
        else:
            #print("There is not enough items in West inventory",Item_code,".\nMissing number =", Num_avil_item - Num_items_ordered)
            return 0
        
    else:       
        Items_not_in_inv_east.append(Item_code)
        #print('One items', Item_code, 'was not found in west inventory.')

def check_inv_west(order):
    for item in order.items:
        if(item[2] == False):
            if(Item_available_west(item[0],item[1])): #item[0] = Code, item[1] = Num_items_ordered
                item[2] = True #availability
                item[3] = "West" #Location
    if(all( availability == 1 for (_, _, availability,_,_) in order.items)):
        return 1 #Some or all items are avaible in East_inv 
    else:
        return 0

def split_order(order):
    original_item2be_split = list()
    for item in order.items: #sends the items one by one
        if(item[2] == False): # only items that were not avaiable in East will go through 
            if(item[0] in df_inv_east['Item code'].tolist()): #checks if the itemcode exists in inv
                Index_item_inv_east = df_inv_east.index[df_inv_east['Item code'] == item[0]].tolist()[0] #index of the item in east inventory 
                if(df_inv_east.at[Index_item_inv_east , 'NumItemsAvailable'] == 0): #checks if the order needs to be split
                    #No need to split, no items in east inv.
                    if(Item_available_west(item[0],item[1])): #item[0] = Code, item[1] = Num_items_ordered
                        item[2] = True #availability
                        item[3] = "West" #Location
                    #else:
                        #print("Not enough items in both inventory for item",item,"in order",order.order_num)
                #elif(item[0] not in df_inv_west['Item code'].tolist()):
                    #print("item does not exist in west inv")

                else:
                    if(item[0] in df_inv_west['Item code'].tolist()): #checks if item exists in west inv
                        Index_item_inv_west = df_inv_west.index[df_inv_west['Item code'] == item[0]].tolist()[0] #index of the item in west inventory 
                        if(df_inv_east.at[Index_item_inv_east , 'NumItemsAvailable'] + df_inv_west.at[Index_item_inv_west , 'NumItemsAvailable'] >= item[1]):
                            #if item in East_inv + West_inv greater than quantity needed; 

                            #there are enough items in both inventories
                            new_item_east = [item[0], df_inv_east.at[Index_item_inv_east , 'NumItemsAvailable'], True, "East", item[4]]
                            new_item_west = [item[0], item[1]-df_inv_east.at[Index_item_inv_east , 'NumItemsAvailable'], True, "West", item[4]]
                            #print("removing the parent order and replacing it with split order for order number:", order.order_num, item[0])
                            original_item2be_split.append(item)
                            order.items.append(new_item_east)
                            order.items.append(new_item_west)

                    #else:
                        #print("item",item[0],"doesnot exist in west(split order). CANNOT BE SPLIT")
                            
            else: #does not exist in East inv
                #print("item",item[0],"doesnot exist in east in split order.")
                if(item[0] in df_inv_west['Item code'].tolist()): #checks if item exists in west inv
                    Index_item_inv_west = df_inv_west.index[df_inv_west['Item code'] == item[0]].tolist()[0] #index of the item in west inventory
                    if(Item_available_west(item[0],item[1])):
                        item[2] = True #availability
                        item[3] = "West" #Location
                
    for item in original_item2be_split:
        order.items.remove(item)
                    
    return order

#______________________________________Main___________________________________________
Complete_orders = list()
Incomplete_orders = list()
Splited_orders = list()

Items_not_in_inv_east = list()
Items_not_in_inv_west = list()

for order in orders:
    remove_duplicates(order) #merges duplicated items in an order
    if(EastOrWest(order)):
        #East
        if(check_inv_east(order)):
            #print("All items for order",order.order_num," are avaible. All in East.")
            Complete_orders.append(order)
            update_inv(order)
        else:            
            if(all( availability == 1 for (_, _, availability,_,_) in split_order(order).items)):
                Complete_orders.append(order)
                update_inv(order)
            else:
                Incomplete_orders.append(order)
                
    else:
        #West
        if(check_inv_west(order)):
            #print("All items for order",order.order_num," are avaible. All in West.")
            Complete_orders.append(order)
            update_inv(order)
        else:
            #Not all items are available in west inventory; setting all availibility to zero
            for item in order.items:
                item[2] = False
                #print("setting all availbility to zero.")
            if(check_inv_east(order)):
                #print("All items for order",order.order_num," are avaible. All in East.")
                Complete_orders.append(order)
                update_inv(order)
            else:            
                if(all( availability == 1 for (_, _, availability,_,_) in split_order(order).items)):
                    Complete_orders.append(order)
                    update_inv(order)
                else:
                    Incomplete_orders.append(order)
#-----------------------------------------------Result-----------------------------------------------------------


lComplete_orders = list()
temp = list()
for order in Complete_orders:
    for i in range(len(order.items)):
        temp = [order.order_num, \
                order.items[i][4][0],order.items[i][4][1],order.items[i][4][2],order.items[i][4][3],\
                order.items[i][4][4],order.items[i][4][5],order.items[i][4][6],order.items[i][4][7],\
                order.items[i][4][8],order.items[i][4][9],order.items[i][4][10],order.items[i][4][11],\
                order.items[i][4][12],order.items[i][4][13],order.items[i][4][14],order.items[i][4][15],\
                order.items[i][4][16],order.items[i][4][17],order.items[i][4][18],order.items[i][4][19],\
                order.items[i][4][20],order.items[i][4][21],order.items[i][4][22],order.items[i][4][23],\
                order.items[i][4][24],order.items[i][4][25],order.items[i][4][26],order.zipcode,\
                order.items[i][4][27],order.items[i][4][28],order.items[i][4][29],order.items[i][4][30],\
                order.items[i][4][31],order.items[i][4][32],order.items[i][4][33],order.items[i][4][34],\
                order.items[i][4][35],order.items[i][4][36],order.items[i][4][37],order.items[i][4][38],\
                order.items[i][4][39],order.items[i][4][40],order.items[i][4][41],order.items[i][4][42],\
                order.items[i][4][43],order.items[i][4][44],order.items[i][4][45],order.items[i][4][46],\
                order.items[i][4][47],order.items[i][0],order.items[i][4][48],order.items[i][4][49],\
                order.items[i][4][50],order.items[i][4][51],order.items[i][4][52],order.items[i][4][53],\
                order.items[i][1],order.items[i][4][54],order.items[i][4][55],order.items[i][4][56],\
                order.items[i][4][57],order.items[i][4][58],order.items[i][4][59],order.items[i][4][60],\
                order.items[i][4][61],order.items[i][4][62],order.items[i][4][63],order.items[i][4][64],\
                order.items[i][4][65],order.items[i][2], order.items[i][3]]
        lComplete_orders.append(temp)



lIncomplete_orders = list()
for order in Incomplete_orders:
    for i in range(len(order.items)):
        temp = [order.order_num, \
                order.items[i][4][0],order.items[i][4][1],order.items[i][4][2],order.items[i][4][3],\
                order.items[i][4][4],order.items[i][4][5],order.items[i][4][6],order.items[i][4][7],\
                order.items[i][4][8],order.items[i][4][9],order.items[i][4][10],order.items[i][4][11],\
                order.items[i][4][12],order.items[i][4][13],order.items[i][4][14],order.items[i][4][15],\
                order.items[i][4][16],order.items[i][4][17],order.items[i][4][18],order.items[i][4][19],\
                order.items[i][4][20],order.items[i][4][21],order.items[i][4][22],order.items[i][4][23],\
                order.items[i][4][24],order.items[i][4][25],order.items[i][4][26],order.zipcode,\
                order.items[i][4][27],order.items[i][4][28],order.items[i][4][29],order.items[i][4][30],\
                order.items[i][4][31],order.items[i][4][32],order.items[i][4][33],order.items[i][4][34],\
                order.items[i][4][35],order.items[i][4][36],order.items[i][4][37],order.items[i][4][38],\
                order.items[i][4][39],order.items[i][4][40],order.items[i][4][41],order.items[i][4][42],\
                order.items[i][4][43],order.items[i][4][44],order.items[i][4][45],order.items[i][4][46],\
                order.items[i][4][47],order.items[i][0],order.items[i][4][48],order.items[i][4][49],\
                order.items[i][4][50],order.items[i][4][51],order.items[i][4][52],order.items[i][4][53],\
                order.items[i][1],order.items[i][4][54],order.items[i][4][55],order.items[i][4][56],\
                order.items[i][4][57],order.items[i][4][58],order.items[i][4][59],order.items[i][4][60],\
                order.items[i][4][61],order.items[i][4][62],order.items[i][4][63],order.items[i][4][64],\
                order.items[i][4][65],order.items[i][2], order.items[i][3]]
        lIncomplete_orders.append(temp)


field = ["Shipping_Order_No","Voucher_Class","Order_Date","Delivery_Date","Planed_Ship_Date","DC_Code","DC_Name","Customer_Code","Customer_Name1","Customer_Name2","Data_11","Data_12","Data_13","Data_14","Customer_Zip_Code","Customer_address1","Customer_address2","Customer_TEL","Customer_FAX","Order_No","Transport_Company","Receiver_Code","Receiver_Name1","Receiver_Name2","Data_25","Data_26","Data_27","Data_28","Receiver_Zip_Code","Receiver_address1","Receiver_address2","Receiver_TEL","Receiver_FAX","Consumption_TAX","Data_35","Data_36","Mail_address","Point","Data_39","SAP_Shipping_No","Data_41","Working_Condition","Balance","Data_44","Data_45","Data_46","Data_47","Update_date","Detail_No","Data_50","Stock_No","BarCode","Location","Description1","Description2","Pcs_Per_case","Case_No","Quantity","Units","Lot1","Lot2","Status_Code","Status","Data_64","Data_65","Data_66","Warranty","Data_68","Data_69","Detail_Update_date","Availability","EasrOrWest"]

df_complete_orders = pd.DataFrame(lComplete_orders, columns = field)

#Creating  East and West order DataFrames
df_East = df_complete_orders.loc[df_complete_orders["EasrOrWest"] == "East"]
df_East = df_East.reset_index().drop(columns=['index'])
df_West = df_complete_orders.loc[df_complete_orders['EasrOrWest'] == 'West']
df_West = df_West.reset_index().drop(columns=['index'])

#Creating incomplete order DataFrames
df_incomplete_orders = pd.DataFrame(lIncomplete_orders, columns = field)


#------------------------------------------------Output-------------------------------------------------------------
import datetime
dateTimeObj = datetime.datetime.now()
timestampStr = dateTimeObj.strftime("%Y%b%d-%H%M%S")#YYYYMMDD-HHMMSS.csv

name_east_file = Output_DCx1_address + 'East_orders' + timestampStr +'.csv'
name_west_file = Output_DCx1_address_west + 'West_orders' + timestampStr +'.csv'
name_incom_file = Output_DCx1_address + 'Incomplete_orders' + timestampStr +'.csv' 


df_East = df_East.drop(columns =['Availability', 'EasrOrWest']) 
df_West = df_West.drop(columns =['Availability', 'EasrOrWest']) 
df_incomplete_orders = df_incomplete_orders.drop(columns =['Availability', 'EasrOrWest']) 

#When there is a NaN value in the columb, other values also turn into a float. hence to change 1.0 values to 1, the following is needed.
df_East["Data_35"] = df_East["Data_35"].fillna(0).astype(int)
df_West["Data_35"] = df_West["Data_35"].fillna(0).astype(int)

############################################Split order flag and COD Tags#################################################
order_nums_east = df_East["Shipping_Order_No"].unique().tolist()
order_nums_west = df_West["Shipping_Order_No"].unique().tolist()


def rise_split_flag(order_num):
    df_East.loc[df_East["Shipping_Order_No"] == Order_Num, "Data_35"] = 1
    df_West.loc[df_West["Shipping_Order_No"] == Order_Num, "Data_35"] = 1

def remove_COD_tag_str(CODtag):
    new_data25_string = CODtag.split("/")
    CODtag = new_data25_string[0] + "/" + new_data25_string[1] + "/" + "/" + new_data25_string[3] + "/" + new_data25_string[4] #removes the COD tag
    return CODtag

def remove_ConTax(order_num):
    df_West.loc[df_West["Shipping_Order_No"] == Order_Num, "Consumption_TAX"] = float("NAN")




for Order_Num in order_nums_east:
    if Order_Num in order_nums_west:
        rise_split_flag(Order_Num)  #rises the split flag
        df_West["Data_25"] = df_West[["Shipping_Order_No","Data_25"]].apply(lambda x: remove_COD_tag_str(x["Data_25"]) if x["Shipping_Order_No"] == Order_Num else x["Data_25"],axis=1)
        remove_ConTax(Order_Num) #sets consumption TAX to zero


##########################################################################################################################
df_East.to_csv(name_east_file, index=False, header=None, encoding="shift_jis_2004", quoting=csv.QUOTE_ALL)
df_West.to_csv(name_west_file, index=False, header=None, encoding="shift_jis_2004", quoting=csv.QUOTE_ALL)
df_incomplete_orders.to_csv(name_incom_file, index=False, header=None, encoding="shift_jis_2004", quoting=csv.QUOTE_ALL)




