import os
import sys

def defineHome():
	home = input("Enter x and y value of coordinate of home with a space inbetween.: ")
	home = [float(i) for i in home.split(" ")]

	homeFile = open("home.txt","r+")
	if (os.path.getsize("home.txt")!=0):
		homeFile.write(str(home[0]) +" " + str(home[1]))
	else:
		homeFile.truncate()
		homeFile.write(str(home[0]) +" " + str(home[1]))
	homeFile.close()
	print("Home coordinate has been defined")
    return home
    
if __name__ == '__main__':
    dontexit = True
    home = []
    try:
        homeFile = open("home.txt","r+")
	except:
		homeFile = open("home.txt","w+")

	if (os.path.getsize("home.txt")!=0):
		home = homeFile.readline()
		home = [float(i) for i in home.split(" ")]

	homeFile.close()

	while (dontexit):
		try:
			print("Enter [1] DEFINEHOME to define home location")
			print("Enter [6] EXIT to exit")

			nextCommand = input()

			if (nextCommand == "1"):
				home = defineHome()

			elif (nextCommand == "6"):
				dontexit = False