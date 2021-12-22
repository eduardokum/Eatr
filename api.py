import myfitnesspal
import os
import time
from datetime import datetime
from nightscout import postCarbsToNightscout
from configparser import ConfigParser

# reading config file
parser = ConfigParser()
parser.read('configs/config.ini')

def login(user, pw):
    client = myfitnesspal.Client(user, pw)
    return client

def getDiet(client, date):
    print("getting diet")
    day = ''
    try: 
        day = client.get_date(int(date[0]), int(date[1]), int(date[2]))
    except:
        print("api error for get_date()")
    return day

# Every 10 minutes, make get request to see if any changes were made
# Make method for comparing day objects
# Check protein intake every x hours

def compareDays(oldDay, newDay):
    print("comparing days")

    latestMealIndex = -1
    different = False

    for i in range(len(newDay.meals)-1):
        if len(newDay.meals[i]) > 0:
            latestMealIndex = i

    #Find which meals to compare, and always pay attention to snacks
    for i in range(len(newDay.meals)-1):
        if i >= latestMealIndex:
            if len(newDay.meals[i]) > len(oldDay.meals[i]):
                different = True

    return latestMealIndex, different

#Checks difference between 2 days meals at a certain meal index
def mealDiff(old_day, new_day, mealIndex):
    print("getting difference")
    print('MealIndex: ' + str(mealIndex))

    oldMeal = old_day.meals[mealIndex].totals
    changedMeal = new_day.meals[mealIndex].totals
    if len(oldMeal) > 0:
        oldCarbs = oldMeal['carbohydrates']
        oldProtein = oldMeal['protein']
        oldFat = oldMeal['fat']
    else:
        oldCarbs = 0
        oldProtein = 0
        oldFat = 0

    newCarbs = changedMeal['carbohydrates']
    newProtein = changedMeal['protein']
    newFat = changedMeal['fat']
    return newCarbs - oldCarbs, newProtein - oldProtein, newFat - oldFat

def main():

    # Myfitnesspal login
    user = os.environ.get('MFP_USERNAME')
    pw = os.environ.get('MFP_PASSWORD')

    client = login(user, pw)

    date = (str(datetime.now())).split(' ')[0].split('-')
    day = getDiet(client, date)

    old_day = day

    while True:
        c = 0
        p = 0
        f = 0
        e = 0

        #Wait x seconds
        time.sleep(60)

        new_day = getDiet(client, date)

        #Checks what the index of the latest meal is and if days are equivalent
        mealIndex, diff = compareDays(old_day, new_day)

        if diff:
            if mealIndex > -1:
                c, p, f = mealDiff(old_day, new_day, mealIndex)

        if c > 0:
            postCarbsToNightscout(str(c), str(p), str(f))
        old_day = new_day

main()