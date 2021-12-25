import datetime
import requests
import json
import os

def postCarbsToNightscout(carbs, protein, fat):
	print("posting to nightscout")
	tz = datetime.timezone(datetime.timedelta(hours=-3))
	now = datetime.datetime.now().astimezone(tz)
	nowDate = str(now).split(' ')[0]
	nowTime = str(now).split(' ')[1]

	querystring = {"token":os.environ.get('NIGHTSCOUT_TOKEN')}

	payload = json.dumps({
		"carbs": carbs,
		"protein": protein,
		"fat": fat,
		"created_at": nowDate + "T" + nowTime,
		"duration": 0,
		"enteredBy": "MyFitenessPal",
		"eventType": "Carb Correction"
	})

	# print('Payload: ' + payload)
	headers = {
	    'Content-Type': "application/json",
	    'cache-control': "no-cache",
	    'Postman-Token': "8d3ce8d7-5551-4392-8904-a975b16d4433"
	}

	print('Carbs Added: ' + carbs + ' Protein Added: ' + protein + ' Fat Added: ' + fat)
	response = requests.request("POST", os.environ.get('NIGHTSCOUT_URL').rstrip("/") + '/api/v1/treatments', data=payload, headers=headers, params=querystring)
