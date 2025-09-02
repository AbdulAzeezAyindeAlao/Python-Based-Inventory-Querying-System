import datetime  # Import the datetime module to work with dates and times
def ReadTheFile(filename): #Function to read the input files
    """Reads a file and returns its content as a list of lists."""
    file = open(filename, 'r') #Opens the file name and gives it read permissions 
    lines = file.readlines() #Read each line of the file
    file.close() #Close the file
    data = [] #Creates a list called data
    for line in lines: #For each line in lines (a list)
        data.append(line.strip().split(',')) #Then, strip each line then split it wherever there is a comma, then append it to the data list
    return data #Return data



def ProcessTheInventory(ManufacturerList, PriceList, ServiceDatesList): #Function for processing the input files
    """Processes the input lists into a structured dictionary."""
    Inventory = {} #Create an empty dictionary to store inventory data
    
    for item in ManufacturerList: #For loop that creates variables for Item ID, Manufacturer, Item Type, Damage Status
        ItemId = item[0].strip() #First Index is equal to the Item ID
        Manufacturer = item[1].strip() #Second Index is equal to the Manufacturer
        ItemType = item[2].strip() #Third Index is equal to the Item Type
        Damaged = item[3].strip() if len(item) > 3 else "" #Fourth Index is equal to the Damage Status
        Inventory[ItemId] = {
            'Manufacturer': Manufacturer,
            'ItemType': ItemType,
            'Damaged': Damaged
        } #Assigns keys to their values
    
    for item in PriceList: #For loop that iterates over each item in the PriceList and updates the Inventory dictionary with the corresponding prices.
        ItemId = item[0].strip()
        price = int(item[1].strip())
        if ItemId in Inventory:
            Inventory[ItemId]['Price'] = price
    
    for item in ServiceDatesList: # For loop that iterates over each item in the ServiceDatesList and then updates the Inventory dictionary
        ItemID = item[0].strip()  # Extract and strip the Item ID from the first element of the item list
        ServiceDateString = item[1].strip()  # Extract and strip the service date string from the second element of the item list
        ServiceDate = datetime.datetime.strptime(ServiceDateString, "%m/%d/%Y") if ServiceDateString else None  # Convert the service date string to a datetime object if it exists
        if ItemID in Inventory:  # Check if the Item ID exists in the Inventory dictionary
            Inventory[ItemID]['ServiceDate'] = ServiceDate #Update the ServiceDate field/key with a new value
    
    return Inventory #Returns data added to the Inventory Dictionary
def SortByTheManufacturer(Inventory): #Function that sorts each item by its manufacturer
    """Returns a list of item IDs sorted alphabetically by manufacturer."""
    ItemIds = list(Inventory.keys())                                    # Get a list of all item IDs from the inventory
    for i in range(len(ItemIds)):                                       # Outer loop to iterate over each item ID
        for j in range(i + 1, len(ItemIds)):                            # Inner loop to compare the current item ID with the rest
            if Inventory[ItemIds[i]]['Manufacturer'] > Inventory[ItemIds[j]]['Manufacturer']: # Compare manufacturers
                    ItemIds[i], ItemIds[j] = ItemIds[j], ItemIds[i]                            # Swap if the current manufacturer is greater
    return ItemIds #Return the sorted list of item IDs

def SortByItemID(items):
    """Sorts items by item ID."""
    for i in range(len(items)):  # Outer loop to iterate over each item
        for j in range(i + 1, len(items)):  # Inner loop to compare the current item with the rest
            if items[i][0] > items[j][0]:  # Compare item IDs
                items[i], items[j] = items[j], items[i]  # Swap if the current item ID is greater
    return items  # Return the sorted list of items

def SortByTheServiceDate(items): # Define a function to sort items by service date
    """Sorts items by service date from oldest to most recent."""  
    for i in range(len(items)): # Outer loop to iterate over each item
        for j in range(i + 1, len(items)): # Inner loop to compare the current item with the rest
            if items[i][1]['ServiceDate'] > items[j][1]['ServiceDate']: # Compare service dates
                items[i], items[j] = items[j], items[i] # Swap if the current service date is later
    return items # Return the sorted list of items

def FullInventory(Inventory):  # Define a function to write the full inventory to a file
    """Writes FullInventory.txt sorted alphabetically by manufacturer."""
    sorted_items = SortByTheManufacturer(Inventory)  # Sort the inventory items by manufacturer
    file = open("FullInventory.txt", 'w')  # Open a file named "FullInventory.txt" in write mode
    for ItemId in sorted_items:  # Iterate over each sorted item ID
        item = Inventory[ItemId]  # Get the item details from the inventory
        ServiceDateString = item.get('ServiceDate', 'N/A')  # Get the service date or 'N/A' if not available
        if ServiceDateString != 'N/A':  # If the service date is available
            ServiceDateString = item['ServiceDate'].strftime('%m/%d/%Y')  # Format the service date as a string
        file.write(f"{ItemId}, {item['Manufacturer']}, {item.get('Price', 'N/A')}, {ServiceDateString}" + (f", {item['Damaged']}" if item['Damaged'] else "") + "\n")  # Write the item details to the file
    file.close()  # Close the file

def ItemTypeInventory(Inventory):
    """Writes separate inventory files per item type, sorted by item ID."""
    ItemTypes = {}  # Create an empty dictionary to store items by their type
    for ItemId in Inventory:  # Iterate over each item in the inventory
        item = Inventory[ItemId]  # Get the item details from the inventory
        ItemType = item['ItemType']  # Get the item type
        if ItemType not in ItemTypes:  # If the item type is not already in the dictionary
            ItemTypes[ItemType] = []  # Create a new list for this item type
        ItemTypes[ItemType].append((ItemId, item))  # Append the item ID and details to the list for this item type
    
    for ItemType in ItemTypes:  # Iterate over each item type in the dictionary
        sorted_items = SortByItemID(ItemTypes[ItemType])  # Sort the items by item ID
        file = open(f"{ItemType.capitalize()}Inventory.txt", 'w')  # Open a file named after the item type in write mode
        for ItemId, item in sorted_items:  # Iterate over each sorted item
            ServiceDateString = item.get('ServiceDate', 'N/A')  # Get the service date or 'N/A' if not available
            if ServiceDateString != 'N/A':  # If the service date is available
                ServiceDateString = item['ServiceDate'].strftime('%m/%d/%Y')  # Format the service date as a string
            file.write(f"{ItemId}, {item['Manufacturer']}, {item.get('Price', 'N/A')}, {ServiceDateString}" + (f", {item['Damaged']}" if item['Damaged'] else "") + "\n")  # Write the item details to the file with a blank line after each item
        file.close()  # Close the file

def PastServiceDateInventory(inventory):  # Define a function to write past service date inventory to a file
    """Writes PastServiceDateInventory.txt sorted by oldest service date."""
    past_service_items = []  # Create an empty list to store items with past service dates
    for ItemId in inventory:  # Iterate over each item in the inventory
        item = inventory[ItemId]  # Get the item details from the inventory
        if 'ServiceDate' in item:  # Check if the item has a service date
            past_service_items.append((ItemId, item))  # Append the item ID and details to the list
    
    sorted_items = SortByTheServiceDate(past_service_items)  # Sort the items by service date
    file = open("PastServiceDateInventory.txt", 'w')  # Open a file named "PastServiceDateInventory.txt" in write mode
    today = datetime.datetime.now()  # Get the current date and time
    for ItemId, item in sorted_items:  # Iterate over each sorted item
        ServiceDateString = item['ServiceDate'].strftime('%m/%d/%Y')  # Format the service date as a string
        if item['ServiceDate'] < today:  # Check if the service date is in the past
            file.write(f"{ItemId}, {item['Manufacturer']}, {item['ItemType']}, {item.get('Price', 'N/A')}, {ServiceDateString}" + (f", {item['Damaged']}" if item['Damaged'] else "") + "\n")  # Write the item details to the file
        else:  # If the service date is not in the past
            'N/A'  # Do nothing
    file.close()  # Close the file

def DamagedInventory(Inventory):  # Define a function to write damaged inventory to a file
    """Writes DamagedInventory.txt sorted by price from highest to lowest."""
    damaged_items = []  # Create an empty list to store damaged items
    for ItemId in Inventory:  # Iterate over each item in the inventory
        item = Inventory[ItemId]  # Get the item details from the inventory
        if item['Damaged']:  # Check if the item is damaged
            damaged_items.append((ItemId, item))  # Append the item ID and details to the list

    def get_price(item):  # Define a helper function to get the price of an item
        return item[1].get('Price', 0)  # Return the price of the item, or 0 if not available

    damaged_items.sort(key=get_price, reverse=True)  # Sort the damaged items by price in descending order
    
    file = open("DamagedInventory.txt", 'w')  # Open a file named "DamagedInventory.txt" in write mode
    for ItemId, item in damaged_items:  # Iterate over each sorted damaged item
        ServiceDateString = item.get('ServiceDate', 'N/A')  # Get the service date or 'N/A' if not available
        if ServiceDateString != 'N/A':  # If the service date is available
            ServiceDateString = item['ServiceDate'].strftime('%m/%d/%Y')  # Format the service date as a string
        file.write(f"{ItemId}, {item['Manufacturer']}, {item['ItemType']}, {item.get('Price', 'N/A')}, {ServiceDateString}\n")  # Write the item details to the file
    file.close()  # Close the file

def main():  # Define the main function
    ManufacturerList = ReadTheFile("ManufacturerList.txt")  # Read the manufacturer list from the file
    PriceList = ReadTheFile("PriceList.txt")  # Read the price list from the file
    ServiceDatesList = ReadTheFile("ServiceDatesList.txt")  # Read the service dates list from the file
    
    Inventory = ProcessTheInventory(ManufacturerList, PriceList, ServiceDatesList)  # Process the lists into an inventory dictionary
    
    FullInventory(Inventory)  # Write the full inventory to a file
    ItemTypeInventory(Inventory)  # Write separate inventory files per item type
    PastServiceDateInventory(Inventory)  # Write the past service date inventory to a file
    DamagedInventory(Inventory)  # Write the damaged inventory to a file
    print("Inventory has been conducted for this.")  # Print a message indicating the inventory process is complete

if __name__ == "__main__":
    main() #Starts the main function of the for the process of conducting inventory. 


