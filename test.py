# location_dictionary = {
#       'Ananda Kitchen': [1051, 182], 
#       'Fine Food @ the South Spine': [592, 1280], 
#       'Food Court 1': [915, 894], 
#       'Food Court 11': [932, 115], 
#       'Food Court 13': [439, 428], 
#       'Food Court 14': [542, 321], 
#       'Food Court 16': [448, 565], 
#       'Food Court 2': [862, 724], 
#       'Food Court 9': [848, 348], 
#       'Foodgle Food Court': [1089, 191], 
#       'North Hill Food Court': [1129, 181], 
#       'North Spine': [372, 881], 
#       'North Spine Food Court': [348, 880], 
#       'Pioneer Food Court': [1166, 961], 
#       'Quad Cafe': [328, 1071]
#       }

# class FoodCourt:
#         # name: String, location: tuple of size 2
#         def __init__(self, name, location):
#             self.name = name
#             self.location = location

#         def __str__(self):
#               return f"{self.name}, {self.location}"

# FoodCourt1 = FoodCourt("Canteen 11", (100, 200))
# print(FoodCourt1)

# FoodCourt_list = []
# for line in location_dictionary: 
#     print(line, location_dictionary[line])
#     FoodCourt_list.append(FoodCourt(line, location_dictionary[line]))

# for foodcourt in FoodCourt_list:
#       print(foodcourt)
sampleList = [
    ["One", "Two"],
    ["Two", "One"], 
    ["One", "Two"]
]

print(sampleList)
sampleList = set(tuple(sampleList))
print(sampleList)
sampleList = list(sampleList)
print(sampleList)