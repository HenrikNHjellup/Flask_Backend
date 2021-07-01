import requests
import sys
#from tkinter import *

BASE = "http://127.0.0.1:5000/"

def populateInitProd():
	response = requests.put(BASE + "product/0", {"name": "Air_Jordan", "shortDesc": "Basketball shoes", "longDesc": "Good shoes for playing basketball.", "sizes": "40 41 42 43 44 45", "price": 199, "colors": "Red"})
	print(response.json())
	response = requests.put(BASE + "product/1", {"name": "Converse", "shortDesc": "Walking shoes", "longDesc": "Good shoes for walking.", "sizes": "40 41 42 43 44 45", "price": 129, "colors": "Red Blue"})
	print(response.json())
	response = requests.put(BASE + "product/2", {"name": "Nike_Air_Max", "shortDesc": "Running shoes", "longDesc": "Good shoes for running.", "sizes": "40 41 42 43 44 45", "price": 149, "colors": "Red Blue Black"})
	print(response.json())
	response = requests.put(BASE + "product/3", {"name": "Nike_Revolt", "shortDesc": "Hiking shoes", "longDesc": "Good shoes for hiking.", "sizes": "40 41 42 43 44 45", "price": 99, "colors": "Red"})
	print(response.json())
	response = requests.put(BASE + "product/4", {"name": "Sneakers", "shortDesc": "Park shoes", "longDesc": "Good shoes for playing in the park.", "sizes": "40 41 42 43 44 45", "price": 109, "colors": "Red White"})
	print(response.json())


populateInitProd()

#action_list = ["get", "put", "delete"]
#resource_list = ["product", "user", "chatroom"]
#index_list = []
#index = 0


#response = requests.put(BASE + "product/0", {"name": "This is name", "price": 100, "colors": 100})
#response = requests.patch(BASE + "product/0", {"price":300})
"""
counter = 0
while True:
	name = input("Name: ")
	description = input("Description: ")
	sizes = input("Sizes: ")
	price = input("Price: ")
	colors = input("Colors: ")
	response = requests.patch(BASE + "product/" + str(counter), {"name": name, "description": description, "price": price, "sizes": sizes, "colors": colors})
	print(response.json())
	br = input("Break")
	counter += 1
	if br:
		break
"""

"""
counter = 0
while True:
	product = input("Product: ")
	number = input("Number: ")
	price = input("Price: ")
	size = input("Size: ")
	color = input("Color: ")
	response = requests.put(BASE + "cart/" + str(counter), {"product": product, "number": number, "price": price, "size": size, "color": color})
	response = requests.put(BASE + "product/5", {"name": "Two_Shoes", "shortDesc": "Driving shoes", "longDesc": "Good shoes for driving.", "sizes": "40 41 42 43 44 45", "price": 159, "colors": "Red Black"})
	print(response.json())

populateInitProd()
