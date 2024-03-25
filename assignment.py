import pygame
from PIL import Image
import time
import pandas as pd


# load dataset for keyword dictionary - provided
def load_stall_keywords(data_location="canteens.xlsx"):
    # get list of canteens and stalls
    canteen_data = pd.read_excel(data_location)
    canteens = canteen_data['Canteen'].unique()
    canteens = sorted(canteens, key=str.lower)

    stalls = canteen_data['Stall'].unique()
    stalls = sorted(stalls, key=str.lower)

    keywords = {}
    for canteen in canteens:
        keywords[canteen] = {}

    copy = canteen_data.copy()
    copy.drop_duplicates(subset="Stall", inplace=True)
    stall_keywords_intermediate = copy.set_index('Stall')['Keywords'].to_dict()
    stall_canteen_intermediate = copy.set_index('Stall')['Canteen'].to_dict()

    for stall in stalls:
        stall_keywords = stall_keywords_intermediate[stall]
        stall_canteen = stall_canteen_intermediate[stall]
        keywords[stall_canteen][stall] = stall_keywords

    return keywords


# load dataset for price dictionary - provided
def load_stall_prices(data_location="canteens.xlsx"):
    # get list of canteens and stalls
    canteen_data = pd.read_excel(data_location)
    canteens = canteen_data['Canteen'].unique()
    canteens = sorted(canteens, key=str.lower)

    stalls = canteen_data['Stall'].unique()
    stalls = sorted(stalls, key=str.lower)

    prices = {}
    for canteen in canteens:
        prices[canteen] = {}

    copy = canteen_data.copy()
    copy.drop_duplicates(subset="Stall", inplace=True)
    stall_prices_intermediate = copy.set_index('Stall')['Price'].to_dict()
    stall_canteen_intermediate = copy.set_index('Stall')['Canteen'].to_dict()

    for stall in stalls:
        stall_price = stall_prices_intermediate[stall]
        stall_canteen = stall_canteen_intermediate[stall]
        prices[stall_canteen][stall] = stall_price

    return prices


# load dataset for location dictionary - provided
def load_canteen_location(data_location="canteens.xlsx"):
    # get list of canteens
    canteen_data = pd.read_excel(data_location)
    canteens = canteen_data['Canteen'].unique()
    canteens = sorted(canteens, key=str.lower)

    # get dictionary of {canteen:[x,y],}
    canteen_locations = {}
    for canteen in canteens:
        copy = canteen_data.copy()
        copy.drop_duplicates(subset="Canteen", inplace=True)
        canteen_locations_intermediate = copy.set_index('Canteen')['Location'].to_dict()
    for canteen in canteens:
        canteen_locations[canteen] = [int(canteen_locations_intermediate[canteen].split(',')[0]),
                                      int(canteen_locations_intermediate[canteen].split(',')[1])]

    return canteen_locations


# get user's location with the use of PyGame - provided
def get_user_location_interface():
    # get image dimensions
    image_location = 'NTUcampus.jpg'
    pin_location = 'pin.png'
    screen_title = "NTU Map"
    image = Image.open(image_location)
    image_width_original, image_height_original = image.size
    scaled_width = int(image_width_original * 0.9)  # image's width scaled according to the screen
    scaled_height = int(image_height_original * 0.9)  # image's height scaled according to the screen
    pinIm = pygame.image.load(pin_location)
    pinIm_scaled = pygame.transform.scale(pinIm, (60, 60))
    # initialize pygame
    pygame.init()
    # set screen height and width to that of the image
    screen = pygame.display.set_mode([scaled_width, scaled_height])
    # set title of screen
    pygame.display.set_caption(screen_title)
    # read image file and rescale it to the window size
    screenIm = pygame.image.load(image_location)
    screenIm_scaled = pygame.transform.scale(screenIm, (scaled_width, scaled_height))

    # add the image over the screen object
    screen.blit(screenIm_scaled, (0, 0))
    # will update the contents of the entire display window
    pygame.display.flip()

    # loop for the whole interface remain active
    while True:
        # checking if input detected
        pygame.event.pump()
        event = pygame.event.wait()
        # closing the window
        if event.type == pygame.QUIT:
            pygame.display.quit()
            mouseX_scaled = None
            mouseY_scaled = None
            break
        # resizing the window
        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode(
                event.dict['size'], pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)
            screen.blit(pygame.transform.scale(screenIm_scaled, event.dict['size']), (0, 0))
            scaled_height = event.dict['h']
            scaled_width = event.dict['w']
            pygame.display.flip()
        # getting coordinate
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # get outputs of Mouseclick event handler
            (mouseX, mouseY) = pygame.mouse.get_pos()
            # paste pin on correct position
            screen.blit(pinIm_scaled, (mouseX - 25, mouseY - 45))
            pygame.display.flip()
            # return coordinates to original scale
            mouseX_scaled = int(mouseX * 1281 / scaled_width)
            mouseY_scaled = int(mouseY * 1550 / scaled_height)
            # delay to prevent message box from dropping down
            time.sleep(0.2)
            break

    pygame.quit()
    pygame.init()
    return mouseX_scaled, mouseY_scaled


# Keyword-based Search Function - to be implemented
# def search_by_keyword(keywords)

# Price-based Search Function - to be implemented
# def search_by_price(keywords, max_price)

# Location-based Search Function - to be implemented
# def search_nearest_canteens(user_locations, k)

# Any additional function to assist search criteria can be used


# Main Python Program Template
# dictionary data structures
canteen_stall_keywords = load_stall_keywords("canteens.xlsx")
canteen_stall_prices = load_stall_prices("canteens.xlsx")
canteen_locations = load_canteen_location("canteens.xlsx")
df_canteen_stall_keywords = pd.DataFrame(canteen_stall_keywords)


# main program template - provided
def main():
    loop = True

    """
    Depending on the option chosen in 
    menu, different datasets and variables 
    will be used for clarity
    """

    option_to_dataset = {
        2: canteen_stall_keywords,
        3: canteen_stall_prices,
        4: canteen_locations
    }

    class FoodCourt:
        # name: String, location: tuple of size 2
        def __init__(self, name, location):
            self.name = name
            self.location = location

        def __str__(self):
              return f"{self.name}, {self.location}"

    # Organises the given dictionary into appropriate lists for use based on options 2, 3 and 4
    def populate_list(dataset, option):
        FoodCourt_list = []
        valid_keyword_list = []
        complete_stall_list = []
        complete_stall_list_keyword = []
        if option == 4:
            # Converts stall list dictionary to list and returns list
            for food_court in dataset:
                FoodCourt_list.append(FoodCourt(food_court, (dataset[food_court][0], dataset[food_court][1])))
            for element in FoodCourt_list:
                print(element)
            return FoodCourt_list
        # If options 2 or 3, merges 1D stall list and 1D corresponding keywords into a 2D list, and also creates a list of unique keywords
        for food_court in dataset:
            for canteen_stall in option_to_dataset[option][food_court]:
                complete_stall_list.append(
                    [food_court, canteen_stall, option_to_dataset[option][food_court][canteen_stall]])
                keyword_intermediate = canteen_stall_keywords[food_court][canteen_stall].split(", ")
                for element in keyword_intermediate:
                    if element not in valid_keyword_list:
                        valid_keyword_list.append(element)
        # If searching by keyword, returns a list containing 2D merged list and 1D unique keyword list.
        # Else, returns list containing 2D merged list, 1D unique keyword list and 2D list with store and price
        if option == 2:
            return [complete_stall_list, valid_keyword_list]
        else:
            for food_court in dataset:
                for canteen_stall in canteen_stall_keywords[food_court]:
                    complete_stall_list_keyword.append(
                        [food_court, canteen_stall, canteen_stall_keywords[food_court][canteen_stall]]
                    )
            return [complete_stall_list, valid_keyword_list, complete_stall_list_keyword]

    def list_initialisation(option):
        if option == 2:
            or_presence = False
            populated_dataset = populate_list(option_to_dataset[option], option)
            return populated_dataset
        
        if option == 4:
            FoodCourt_list = populate_list(option_to_dataset[option], option)
            return FoodCourt_list

        populated_dataset = populate_list(option_to_dataset[option], option)
        return populated_dataset

    def keyword_split(keyword_orPresence):
        keyword_orPresence[0] = keyword_orPresence[0].lstrip().rstrip().upper()
        if " " in keyword_orPresence[0]:
            split_keywords = keyword_orPresence[0].split(" ")
            split_keywords = list(dict.fromkeys(split_keywords))
            if "OR" in split_keywords:
                keyword_orPresence[1] = True
                split_keywords.remove("OR")
            if "AND" in split_keywords:
                split_keywords.remove("AND")
            if "" in split_keywords:
                split_keywords.remove("")
            keyword_count = 0
            for keyword in split_keywords:
                split_keywords[keyword_count] = keyword.lstrip().rstrip().capitalize()
                keyword_count += 1
            keyword_orPresence[0] = split_keywords
            return keyword_orPresence
        else:
            keyword_orPresence[0] = [keyword_orPresence[0].lstrip().rstrip().capitalize()]
        return keyword_orPresence

    def output_stores_by_keyword(keyword_orPresence):
        finalised_stores = []
        if keyword_orPresence[1] == True:
            for stall in complete_stall_list:
                for indiv_keyword in keyword_orPresence[0]:
                    if indiv_keyword in stall[2] and stall not in finalised_stores:
                        finalised_stores.append(stall)
        else:
            print(complete_stall_list)
            for stall in complete_stall_list:
                count = 0
                for indiv_keyword in keyword_orPresence[0]:
                    if indiv_keyword not in stall[2]:
                        break
                    elif indiv_keyword in stall[2] and count == len(keyword_orPresence[0]) - 1:
                        finalised_stores.append(stall)
                    else:
                        count += 1
                        continue
        print(finalised_stores)
        return finalised_stores

    def convert_keyword_to_price(finalised_stores):
        print(finalised_stores)
        finalised_stores_price = []
        finalised_stores_count = 0
        if finalised_stores != []:
            for stall_index in range(len(complete_stall_list_keyword)):
                print(complete_stall_list_keyword[stall_index][1])
                print(finalised_stores[finalised_stores_count][1])
                if complete_stall_list_keyword[stall_index][1] == finalised_stores[finalised_stores_count][1]:
                    finalised_stores_price.append(complete_stall_list_keyword[stall_index])
                    finalised_stores_count += 1
                if finalised_stores_count == len(finalised_stores):
                    break

            print(finalised_stores_price)
            return finalised_stores_price
        else: 
            return []

    def output_stores_by_price(price, filtered_stores):
        finalised_stores = []
        for stall in filtered_stores:
            if stall[2] <= price:
                finalised_stores.append(stall)
        return finalised_stores

    def print_list(finalised_stores):
        print(finalised_stores)
        print(f"Food Stalls found: {len(finalised_stores)}")
        for store in finalised_stores:
            print(f"{store[0]} - {store[1]}")
        return 0
    
    def print_list_price(finalised_stores):
        print(finalised_stores)
        print(f"Food Stalls found: {len(finalised_stores)}")
        for store in finalised_stores:
            print(f"{store[0]} - {store[1]} - S${store[2]:.2f}")
        return 0

    def keyword_isEmpty(keyword):
        if keyword == " ":
            print("Error: No input found. Please try again.")
            return 1
        return 0

    def keyword_isInvalid(keyword):
        for element in keyword:
            if element not in valid_keyword_list:
                if element in ["Mixed", "Rice"]:
                    keyword.remove(element)
                    if element == "Mixed": 
                        keyword.append("Mixed Rice")
                    continue
                print(f"Food Stalls found: No food stall found with input keyword {element}.")
                return 1
        return 0

    def search_by_keyword(keywords):
        or_presence = False
        keyword_orPresence = [keywords, or_presence]

        if keyword_isEmpty(keyword_orPresence[0]) == 1:
            return 1

        keyword_orPresence = keyword_split(keyword_orPresence)

        if keyword_isInvalid(keyword_orPresence[0]) == 1:
            return 1

        finalised_stores = output_stores_by_keyword(keyword_orPresence)

        print_list(finalised_stores)

        return 0

    def search_by_price(keywords, max_price):
        or_presence = False
        keyword_orPresence = [keywords, or_presence]

        if keyword_isEmpty(keyword_orPresence[0]) == 1:
            return 1

        keyword_orPresence = keyword_split(keyword_orPresence)
        keywords = keyword_orPresence[0]

        if keyword_isInvalid(keyword_orPresence[0]) == 1:
            return 1

        if max_price < 0:
            print("Error: Meal price cannot be a negative number. Please try again.")
            return 1

        if 0 < max_price < 1.5:
            print("Food Stalls found: No food stall found with specified price range.")
            print("Food Stall with the closest price range.")
            print("Food Court 14 – Willy Waffles – S$1.50")
            return 1

        filtered_stores = convert_keyword_to_price(output_stores_by_keyword(keyword_orPresence))

        finalised_stores = output_stores_by_price(max_price, filtered_stores)

        print_list_price(finalised_stores)
        return 0

    def search_nearest_canteens(user_locations, k):
        FoodCourt_distance_list = []

        # Abstracts data into readable variables for easy maintenance 
        userA_xCoord = user_locations[0][0]
        userA_yCoord = user_locations[0][1]
        userB_xCoord = user_locations[1][0]
        userB_yCoord = user_locations[1][1]

        for food_court in FoodCourt_list:
            # Finds the euclidean distance between each stall from the respective users
            distance_a = ((userA_xCoord - food_court.location[0]) ** 2 + ((userA_yCoord - food_court.location[1]) ** 2)) ** 0.5
            distance_b = ((userB_xCoord - food_court.location[0]) ** 2 + ((userB_yCoord - food_court.location[1]) ** 2)) ** 0.5
            FoodCourt_distance_list.append([food_court.name, distance_a, distance_b, max(distance_a, distance_b)])

        # Sorts food courts by shortest distance to BOTH users
        FoodCourt_distance_list.sort(key=lambda a: a[3])
        # print(food_court_distance_list)

        finalised_FoodCourt_list = FoodCourt_distance_list[0:k]
        # print(finalised_food_court_list)

        print(f"{len(finalised_FoodCourt_list)} Nearest Canteen(s) found:")
        for food_court in finalised_FoodCourt_list:
            print(f"{food_court[0]} - {int(food_court[1])}m (User A), {int(food_court[2])}m (User B)")
        return 0

    while loop:
        print("========================")
        print("F&B Recommendation Menu")
        print("1 -- Display Data")
        print("2 -- Keyword-based Search")
        print("3 -- Price-based Search")
        print("4 -- Location-based Search")
        print("5 -- Exit Program")
        print("========================")
        option = int(input("Enter option [1-5]: "))

        if option == 1:
            # print provided dictionary data structures
            print("1 -- Display Data")
            print("Keyword Dictionary: ", canteen_stall_keywords)
            print("Price Dictionary: ", canteen_stall_prices)
            print("Location Dictionary: ", canteen_locations)
        elif option == 2:
            # keyword-based search
            keyword_and_stall_list = list_initialisation(option)
            valid_keyword_list = keyword_and_stall_list[1]
            complete_stall_list = keyword_and_stall_list[0]
            print(valid_keyword_list)
            print(complete_stall_list)

            print("2 -- Keyword-based Search")
            keywords = input("Enter type of food: ")
            result = search_by_keyword(keywords)
            while result == 1:
                keywords = input("Enter type of food: ")
                result = search_by_keyword(keywords)

            # call keyword-based search function
            # search_by_keyword(keywords)
        elif option == 3:
            # price-based search
            keyword_and_stall_list = list_initialisation(option)
            valid_keyword_list = keyword_and_stall_list[1]
            complete_stall_list = keyword_and_stall_list[2]
            complete_stall_list_keyword = keyword_and_stall_list[0]
            print(valid_keyword_list)
            print(complete_stall_list)
            print(complete_stall_list_keyword)

            print("3 -- Price-based Search")
            keywords = input("Enter type of food: ")
            max_price = float(input("Enter maximum meal price (S$): "))
            result = search_by_price(keywords, max_price)
            while result == 1:
                keywords = input("Enter type of food: ")
                max_price = float(input("Enter maximum meal price (S$): "))
                result = search_by_price(keywords, max_price)
            # call price-based search function
            # search_by_price(keywords, max_price)
        elif option == 4:
            # location-based search
            FoodCourt_list = list_initialisation(option)
            print("4 -- Location-based Search")

            # call PyGame function to get two users' locations
            userA_location = get_user_location_interface()
            print("User A's location (x, y): ", userA_location)
            userB_location = get_user_location_interface()
            print("User B's location (x, y): ", userB_location)
            user_locations = [userA_location, userB_location]
            try:
                k = int(input("Number of canteens: "))
            except:
                print("Warning: k cannot be negative value. Default k = 1 is set.")
                k = 1

            if k < 1:
                print("Warning: k cannot be negative value. Default k = 1 is set.")
                k = 1

            search_nearest_canteens(user_locations, k)

            # call location-based search function
            # search_nearest_canteens(user_locations, k)
        elif option == 5:
            # exit the program
            print("Exiting F&B Recommendation")
            loop = False


main()
