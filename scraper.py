from selenium import webdriver
import time
import csv

driver = webdriver.Firefox(executable_path = './geckodriver') 

def UrlFromCity(city):
	return "http://tpnagar.com/Search/Search?City=" + city + "&txtSearch=&ddlState="

cities = ["173~Ambala", "450~Amritsar", "241~Bangalore", "458~Bhiwadi", "945~Bokaro", "449~Chandigarh", "496~Chennai", "127~Delhi", "171~Faridabad", "598~Ghaziabad", "172~Gurgaon", "56~Guwahati", "523~Hyderabad", "258~Indore", "453~Jaipur", "452~Jalandhar", "203~Jammu", "206~Jamshedpur", "535~Kanpur", "335~Kolhapur", "619~Kolkata", "158~Kutch", "536~Lucknow", "451~Ludhiana", "310~Mumbai", "312~Nagpur", "588~Noida", "65~Patna", "130~Ponda", "311~Pune", "613~Rudrapur"]
cities = ["127~Delhi", "171~Faridabad", "598~Ghaziabad", "172~Gurgaon", "56~Guwahati", "523~Hyderabad", "258~Indore", "453~Jaipur", "452~Jalandhar", "203~Jammu", "206~Jamshedpur", "535~Kanpur", "335~Kolhapur", "619~Kolkata", "158~Kutch", "536~Lucknow", "451~Ludhiana", "310~Mumbai", "312~Nagpur", "588~Noida", "65~Patna", "130~Ponda", "311~Pune", "613~Rudrapur"]


last_transporter = ""
pagination_xpath = '//div[contains(@class, "col-12") and contains(@class, "pagination")]/ul/li'
next_btn_xpath = '//a[@id="next"]'
container_xpath = '//div[contains(@class, "box") and contains(@class, "searchboxlist")]'

# transporter_name_xpath = container_xpath + '/div[@class=top]'
# transporter_address_xpath = container_xpath + '/div[@class=second]/p[1]'
# transporter_numbers_xpath = container_xpath + '/div[@class=second]/p[2]/strong[1]'
# transporter_address_xpath = container_xpath + '/div[@class=second]/p[2]/strong[2]'

def get_btns():
	return driver.find_elements_by_xpath(pagination_xpath)

for city in cities:
	driver.get(UrlFromCity(city))
	time.sleep(2)

	all_data = []
	containers = driver.find_elements_by_xpath(container_xpath)
	for c in containers:
		data_row = c.text.split("\n")
		if(data_row == ['']):
			break
		else:
			this_page_last_data = data_row

	last_page_last_data = []


	while(last_page_last_data != this_page_last_data or len(all_data) == 0):
		current_btn = 0
		containers = driver.find_elements_by_xpath(container_xpath)
		time.sleep(2)
		next_btn = driver.find_elements_by_xpath(next_btn_xpath)
		if(len(all_data) == 0):
			last_page_last_data = ["bluu"]
		else:
			last_page_last_data = all_data[(len(all_data) - 1)]

		for c in containers:
			data_row = c.text.split("\n")
			if(data_row == ['']):
				current_btn += 1
				all_btns = get_btns()
				btns = all_btns[1:len(all_btns)]
				if(current_btn < len(btns)):
					print(".......BTN{current_btn} IN......{total}\n".format(current_btn = current_btn, total = len(btns)))
					time.sleep(2)
					flag = 1
					while(flag):
						try:
							all_btns[current_btn].click()
							flag = 0
							break
						except:
							print("Not clickable, waiting 2s")
							time.sleep(5)

					containers = driver.find_elements_by_xpath(container_xpath)
					time.sleep(2)
					pass
				else:
					print("\n\n....NEXT....\n\n")
					next_btn[0].click()
					time.sleep(2)
					break		
			else:
				this_page_last_data = data_row
				all_data.append(data_row)

	with open(city + '.csv', 'a', newline = '') as file:
		writer = csv.writer(file)
		writer.writerow(["Transporter", "Address", "Numbers", "Contact Person"])
		for data in all_data:
			writer.writerow(data)


driver.close()
