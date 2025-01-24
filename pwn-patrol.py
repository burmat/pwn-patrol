# @burmat

import inquirer
import time
import json
import requests
import xlsxwriter

# conduct a lookup based on an email
def hibp_account_lookup(module, email_address):
	headers = {'User-Agent': 'haveibeenpwned-api','hibp-api-key': API_KEY}
	try:
		url = f'https://haveibeenpwned.com/api/v3/{module}/{email_address}'
		response = requests.request("GET", url, headers=headers)
		if response.status_code == 200:
			return response.json()
		else:
			return None # the account was not found
	except requests.RequestException as e:
		print(e)
		return False

# user chose to query a single account
def hibp_email_query(email):
	print(f'[>] Querying for: {email}')

	breaches = hibp_account_lookup('breachedaccount', email)
	if breaches:
		print("[+] Discovered breaches:\n")
		for breach in breaches:
			print(breach['Name'])

	pastes = hibp_account_lookup('pasteaccount', email)
	if pastes:
		print("[+] Discovered pastes:\n")
		for paste in pastes:
			if paste["Source"] == "Pastebin":
				print(f'Pastebin: https://pastebin.com/{paste['Id']}')
			else:
				print(f'{paste['Title']} ({paste['Source']})')

# when the user wants to use a list of emails
def hibp_list_ingester():
	EMAIL_COL		  = 0
	BREACHES_COL	= 1
	PASTES_COL		= 2

	questions = [
		inquirer. Path('file', path_type=inquirer.Path.FILE, exists=True, message="List of emails filepath")
	]

	filepath = inquirer.prompt(questions)['file']

	with open(filepath) as file:
		row = 0
		workbook = xlsxwriter.Workbook('pwn-patrol.xlsx')
		sheet = workbook.add_worksheet('Breaches & Pastes')
		wrap_format = workbook.add_format({'text_wrap': True})
		wrap_format.set_align('vcenter')

		# header row for the sheet:
		sheet.write(0, EMAIL_COL, 'Account', wrap_format)
		sheet.write(0, BREACHES_COL, 'Breaches', wrap_format)
		sheet.write(0, PASTES_COL, 'Pastes', wrap_format)

		row = 1

		for email in file:
			# rate limited at every 1.5sec. ~100 lookups = ~ 2.5min
			time.sleep(1.5)
			email = email.rstrip()
			if len(email):
				print(f'[>] Querying for {email}')
				breaches_value = ''		# will hold the cell contents for breaches
				pastes_value = '' 		# will hold the cell contents for pastes

				# line break the discovered breaches
				breaches = hibp_account_lookup('breachedaccount', email)
				if breaches:
					for breach in breaches:
						breaches_value += breach['Name'] + '\n'

				# line break the discovered pastes. if pastebin, the url is hardcoded.
				pastes = hibp_account_lookup('pasteaccount', email)
				if pastes:
					for paste in pastes:
						if paste["Source"] == "Pastebin":
							# pastebin, write the link to the file
							pastes_value += 'Pastebin: https://pastebin.com/' + paste['Id'] + ')\n'
						elif paste['Title']:
							# it has a title. write that to file
							pastes_value += paste['Title'] + ' (' + paste['Source'] + ')\n'
						else:
							# no title, but something was found. write it to file
							pastes_value += paste['Source'] + '\n'

				# if we have breach OR paste data, write it to a file and increment the row
				if breaches or pastes:
					sheet.write(row, EMAIL_COL, email, wrap_format)
					sheet.write(row, BREACHES_COL, breaches_value.strip('\n'), wrap_format)
					sheet.write(row, PASTES_COL, pastes_value.strip('\n'), wrap_format)
					row += 1
				# else: no breaches or pastes were discovered

		sheet.autofit()
		workbook.close()

	print('[+] Finished up! Output is saved to pwn-patrol.xlsx')

# main stuff
def main():
	global API_KEY
	question = [
		inquirer.Password('api_key', message="HIBP API Key")
	]
	answer = inquirer.prompt(question)
	API_KEY = answer['api_key']

	options = [
		'Looking up an email for pwnage (quick)',
		'Providing a list of emails to query (normal)',
		'Performing OSINT, then checking for pwnage (slowest)'
	]
	question = [inquirer.List('selection', 
						   message='What are we doing?',
						   choices=options)]
	answer = inquirer.prompt(question)
	mode = answer['selection']
	if 'quick' in mode:
		question = [inquirer.Text("email_address", message="Email Address")]
		answer = inquirer.prompt(question)
		email = answer['email_address']
		hibp_email_query(email)
	elif 'normal' in mode:
		hibp_list_ingester()
	elif 'slowest' in mode:
		print('[!] in the works - bbl.')
		exit(0)
	else:
		print('[!] An error occurred. Exiting.')
		exit(1)
		
	return None

if __name__ == "__main__":
	logo = """______ _    _ _   _       ______  ___ ___________ _____ _     
| ___ \\ |  | | \\ | |      | ___ \\/ _ \\_   _| ___ \\  _  | |    
| |_/ / |  | |  \\| |______| |_/ / /_\\ \\| | | |_/ / | | | |    
|  __/| |/\\| | . ` |______|  __/|  _  || | |    /| | | | |    
| |   \\  /\\  / |\\  |      | |   | | | || | | |\\ \\\\ \\_/ / |____
\\_|    \\/  \\/\\_| \\_/      \\_|   \\_| |_/\\_/ \\_| \\_|\\___/\\_____/
       🐾 No job is too big, no pwn is too small 🐾
	   """
	print(logo)
	main()
	exit(0)
