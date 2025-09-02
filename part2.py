import datetime  # Importing the datetime module for date manipulation

class InventoryManager:
    """Manages inventory: file reading, processing, saving, and user querying."""

    def __init__(self):
        # Initializes the inventory dictionary to store item details
        self.inventory = {}

    def read_file(self, filename):
        """Reads a file and returns its content as a list of lists."""
        file = open(filename, 'r')  # Opens the file in read mode
        lines = file.readlines()  # Reads all lines from the file
        file.close()  # Closes the file
        data = []  # Initializes an empty list to store processed data
        for line in lines:  # Iterates through each line in the file
            data.append(line.strip().split(','))  # Splits the line by commas and adds to the list
        return data  # Returns the processed data

    def process_inventory(self, manufacturer_list, price_list, service_dates_list):
        """Processes the input lists into a structured inventory dictionary."""
        for item in manufacturer_list:  # Iterates through the manufacturer list
            ItemId = item[0].strip()  # Extracts and trims the item ID
            Manufacturer = item[1].strip()  # Extracts and trims the manufacturer name
            ItemType = item[2].strip()  # Extracts and trims the item type
            Damaged = item[3].strip() if len(item) > 3 else ""  # Extracts damage status if available
            # Adds the item to the inventory dictionary
            self.inventory[ItemId] = {
                'Manufacturer': Manufacturer,
                'ItemType': ItemType,
                'Damaged': Damaged
            }

        for item in price_list:  # Iterates through the price list
            ItemId = item[0].strip()  # Extracts and trims the item ID
            Price = int(item[1].strip())  # Extracts and converts the price to an integer
            if ItemId in self.inventory:  # Checks if the item ID exists in the inventory
                self.inventory[ItemId]['Price'] = Price  # Adds the price to the inventory

        for item in service_dates_list:  # Iterates through the service dates list
            ItemId = item[0].strip()  # Extracts and trims the item ID
            ServiceDateString = item[1].strip()  # Extracts and trims the service date string
            # Converts the service date string to a datetime object
            ServiceDate = datetime.datetime.strptime(ServiceDateString, "%m/%d/%Y") if ServiceDateString else None
            if ItemId in self.inventory:  # Checks if the item ID exists in the inventory
                self.inventory[ItemId]['ServiceDate'] = ServiceDate  # Adds the service date to the inventory

    def sort_by_manufacturer(self):
        """Returns a list of item IDs sorted alphabetically by manufacturer."""
        item_ids = list(self.inventory.keys())  # Gets all item IDs from the inventory
        # Bubble sort to sort item IDs by manufacturer name
        for i in range(len(item_ids)):
            for j in range(i + 1, len(item_ids)):
                if self.inventory[item_ids[i]]['Manufacturer'] > self.inventory[item_ids[j]]['Manufacturer']:
                    item_ids[i], item_ids[j] = item_ids[j], item_ids[i]  # Swaps the item IDs
        return item_ids  # Returns the sorted list of item IDs

    def sort_by_item_id(self, items):
        """Sorts items by item ID."""
        # Bubble sort to sort items by item ID
        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                if items[i][0] > items[j][0]:
                    items[i], items[j] = items[j], items[i]  # Swaps the items
        return items  # Returns the sorted list of items

    def sort_by_service_date(self, items):
        """Sorts items by service date from oldest to most recent."""
        # Bubble sort to sort items by service date
        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                if items[i][1]['ServiceDate'] > items[j][1]['ServiceDate']:
                    items[i], items[j] = items[j], items[i]  # Swaps the items
        return items  # Returns the sorted list of items

    def full_inventory(self):
        """Writes FullInventory.txt sorted alphabetically by manufacturer."""
        sorted_items = self.sort_by_manufacturer()  # Sorts items by manufacturer
        file = open("FullInventory.txt", 'w')  # Opens the output file in write mode
        for item_id in sorted_items:  # Iterates through the sorted item IDs
            item = self.inventory[item_id]  # Retrieves the item details
            service_date_string = item.get('ServiceDate', 'N/A')  # Gets the service date or 'N/A'
            if service_date_string != 'N/A':  # Formats the service date if available
                service_date_string = item['ServiceDate'].strftime('%m/%d/%Y')
            # Writes the item details to the file
            file.write(f"{item_id}, {item['Manufacturer']}, {item['ItemType']}, {item.get('Price', 'N/A')}, {service_date_string}" + (f", {item['Damaged']}" if item['Damaged'] else "") + "\n")
        file.close()  # Closes the file

    def item_type_inventory(self):
        """Writes separate inventory files per item type, sorted by item ID."""
        item_types = {}  # Initializes a dictionary to group items by type
        for item_id in self.inventory:  # Iterates through the inventory
            item = self.inventory[item_id]  # Retrieves the item details
            item_type = item['ItemType']  # Gets the item type
            if item_type not in item_types:  # Creates a new list for the item type if not already present
                item_types[item_type] = []
            item_types[item_type].append((item_id, item))  # Adds the item to the corresponding list

        for item_type in item_types:  # Iterates through each item type
            sorted_items = self.sort_by_item_id(item_types[item_type])  # Sorts items by item ID
            file = open(f"{item_type.capitalize()}Inventory.txt", 'w')  # Opens the output file for the item type
            for item_id, item in sorted_items:  # Iterates through the sorted items
                service_date_string = item.get('ServiceDate', 'N/A')  # Gets the service date or 'N/A'
                if service_date_string != 'N/A':  # Formats the service date if available
                    service_date_string = item['ServiceDate'].strftime('%m/%d/%Y')
                # Writes the item details to the file
                file.write(f"{item_id}, {item['Manufacturer']}, {item.get('Price', 'N/A')}, {service_date_string}" + (f", {item['Damaged']}" if item['Damaged'] else "") + "\n")
            file.close()  # Closes the file

    def past_service_date_inventory(self):
        """Writes PastServiceDateInventory.txt sorted by oldest service date."""
        today = datetime.datetime.now()  # Gets the current date and time
        past_service_items = []  # Initializes a list to store past service items
        for item_id in self.inventory:  # Iterates through the inventory
            item = self.inventory[item_id]  # Retrieves the item details
            if 'ServiceDate' in item:  # Checks if the item has a service date
                past_service_items.append((item_id, item))  # Adds the item to the list

        sorted_items = self.sort_by_service_date(past_service_items)  # Sorts items by service date
        file = open("PastServiceDateInventory.txt", 'w')  # Opens the output file in write mode
        for item_id, item in sorted_items:  # Iterates through the sorted items
            if item['ServiceDate'] < today:  # Checks if the service date is in the past
                service_date_string = item['ServiceDate'].strftime('%m/%d/%Y')  # Formats the service date
                # Writes the item details to the file
                file.write(f"{item_id}, {item['Manufacturer']}, {item['ItemType']}, {item.get('Price', 'N/A')}, {service_date_string}\n")
        file.close()  # Closes the file

    def damaged_inventory(self):
        """Writes DamagedInventory.txt sorted by price from highest to lowest."""
        damaged_items = []  # Initializes a list to store damaged items
        for item_id in self.inventory:  # Iterates through the inventory
            item = self.inventory[item_id]  # Retrieves the item details
            if item['Damaged']:  # Checks if the item is damaged
                damaged_items.append((item_id, item))  # Adds the item to the list

        # Manual descending sort by price
        for i in range(len(damaged_items)):
            for j in range(i + 1, len(damaged_items)):
                if damaged_items[i][1].get('Price', 0) < damaged_items[j][1].get('Price', 0):
                    damaged_items[i], damaged_items[j] = damaged_items[j], damaged_items[i]  # Swaps the items

        file = open("DamagedInventory.txt", 'w')  # Opens the output file in write mode
        for item_id, item in damaged_items:  # Iterates through the sorted damaged items
            service_date_string = item.get('ServiceDate', 'N/A')  # Gets the service date or 'N/A'
            if service_date_string != 'N/A':  # Formats the service date if available
                service_date_string = item['ServiceDate'].strftime('%m/%d/%Y')
            # Writes the item details to the file
            file.write(f"{item_id}, {item['Manufacturer']}, {item['ItemType']}, {item.get('Price', 'N/A')}, {service_date_string}\n")
        file.close()  # Closes the file

    def find_best_match(self, manufacturer, item_type):
        """Finds the best item matching manufacturer and item type."""
        today = datetime.datetime.now()  # Gets the current date and time
        matched_items = []  # Initializes a list to store matched items

        for item_id, item in self.inventory.items():  # Iterates through the inventory
            # Checks if the item matches the manufacturer and item type, is not damaged, and is within service date
            if item['Manufacturer'].lower() == manufacturer.lower() and item['ItemType'].lower() == item_type.lower():
                if not item['Damaged'] and item['ServiceDate'] > today:
                    matched_items.append((item_id, item))  # Adds the item to the matched list

        if matched_items:  # Checks if there are matched items
            most_expensive = matched_items[0]  # Initializes the most expensive item
            for item in matched_items:  # Iterates through the matched items
                if item[1]['Price'] > most_expensive[1]['Price']:  # Finds the most expensive item
                    most_expensive = item
            return most_expensive  # Returns the most expensive item
        else:
            return None  # Returns None if no match is found

    def find_closest_alternative(self, selected_item_id, item_type, selected_price):
        """Finds a different manufacturer with similar item type and closest price.""" 
        today = datetime.datetime.now()  # Gets the current date and time
        alternatives = []  # Initializes a list to store alternative items 

        for item_id, item in self.inventory.items():  # Iterates through the inventory
            # Checks if the item matches the item type, is not damaged, and is within service date
            if item_id != selected_item_id and item['ItemType'].lower() == item_type.lower():
                if not item['Damaged'] and item['ServiceDate'] > today:
                    alternatives.append((item_id, item))  # Adds the item to the alternatives list

        closest = None  # Initializes the closest alternative
        min_price_diff = None  # Initializes the minimum price difference

        for item in alternatives:  # Iterates through the alternative items
            price_diff = abs(item[1]['Price'] - selected_price)  # Calculates the price difference
            if min_price_diff is None or price_diff < min_price_diff:  # Finds the closest price
                min_price_diff = price_diff
                closest = item

        return closest  # Returns the closest alternative

    def process_query(self, user_input):
        """Processes user input for a query."""
        words = user_input.lower().split()  # Splits the user input into words
        manufacturers = []  # Initializes a list to store manufacturers
        item_types = []  # Initializes a list to store item types

        for word in words:  # Iterates through the input words
            for item in self.inventory.values():  # Iterates through the inventory
                # Checks if the word matches a manufacturer or item type
                if word == item['Manufacturer'].lower() and word not in manufacturers:
                    manufacturers.append(word)
                if word == item['ItemType'].lower() and word not in item_types:
                    item_types.append(word)

        if len(manufacturers) != 1 or len(item_types) != 1:  # Checks if there is exactly one match for each
            print("No such item in inventory")  # Prints an error message
            return

        manufacturer = manufacturers[0]  # Gets the matched manufacturer
        item_type = item_types[0]  # Gets the matched item type

        result = self.find_best_match(manufacturer, item_type)  # Finds the best match

        if result:  # Checks if a match is found
            item_id, item = result  # Retrieves the matched item details
            # Prints the matched item details
            print(f"Your item is: {item_id}, {item['Manufacturer']}, {item['ItemType']}, {item['Price']}")
            alternative = self.find_closest_alternative(item_id, item_type, item['Price'])  # Finds an alternative
            if alternative:  # Checks if an alternative is found
                alt_id, alt_item = alternative  # Retrieves the alternative item details
                # Prints the alternative item details
                print(f"You may, also, consider: {alt_id}, {alt_item['Manufacturer']}, {alt_item['ItemType']}, {alt_item['Price']}")
        else:
            print("No such item in inventory")  # Prints an error message if no match is found

def main():
    manager = InventoryManager()  # Creates an instance of the InventoryManager class

    # Reads the input files and processes the inventory
    manufacturer_list = manager.read_file("ManufacturerList.txt")
    price_list = manager.read_file("PriceList.txt")
    service_dates_list = manager.read_file("ServiceDatesList.txt")
    manager.process_inventory(manufacturer_list, price_list, service_dates_list)

    # Generates the inventory reports
    manager.full_inventory()
    manager.item_type_inventory()
    manager.past_service_date_inventory()
    manager.damaged_inventory()

    while True:  # Loops to process user queries
        user_input = input("\nPlease enter manufacturer and item type (or 'q' to quit): ")  # Prompts the user
        if user_input.lower() == 'q':  # Checks if the user wants to quit
            break  # Exits the loop
        manager.process_query(user_input)  # Processes the user query

    print("Thank you for using the Inventory System!")  # Prints a thank-you message

if __name__ == "__main__":
    main()  # Calls the main function to start the program
