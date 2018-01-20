import requests
import csv
import os
from bs4 import BeautifulSoup
from user_agent import generate_user_agent
import time


def parse_content(doc):
	soup = BeautifulSoup(doc.content, "html.parser")
	rows = soup.select("form#compareForm div.searchResult")
	result_data = []
	for item in rows:
		var_id_tags = item.select("div.col-xs-4.col-sm-2.hidden-xs.text-center")
		if len(var_id_tags) > 0:
			var_id = var_id_tags[0].text.strip().replace('.', '') 
		else:
			var_id = None
		var_name_tags = item.select("div.col-xs-8.col-sm-3.text-center a")
		if len(var_name_tags) > 0:
			var_name = var_name_tags[0].text
			var_url = '{}{}'.format('https://www.icpsr.umich.edu',var_name_tags[0].get('href'))
		else:
			var_name = var_url = None
		
		var_label = item.find('p').text.strip()

		var_dataset = item.find('em').text.strip()
		
		if var_id is not None:
			result_data.append((var_id, var_name, var_url, var_label, var_dataset))
	return result_data


def main(URL, OUTFILE):
	
	with open(OUTFILE,'w') as outfile:
		writer = csv.writer(outfile)
		writer.writerow(['var_id', 'var_name', 'var_url', 'var_label', 'var_dataset'])
		START_PAGE = 1
		#while START_PAGE < 202: # only the first 4 pages
		while START_PAGE < 4960852: # the whole thing
			AGENT = generate_user_agent(device_type = "desktop", os=('mac', 'linux')) #new agent each time
			headers = {'User-Agent':AGENT}
			CURR_URL = URL.format(START_PAGE)
			res = requests.get(CURR_URL, headers=headers)
			data = parse_content(res)
			
			print("First pass with {} results starting at row {}".format(len(data), START_PAGE))
			for line in data:
				writer.writerow(line)
			
			time.sleep(3)
			START_PAGE += 50



if __name__ == '__main__':
	_VAR_URL = 'https://www.icpsr.umich.edu/icpsrweb/ICPSR/ssvd/variables?q=*&paging.startRow={}' #this should return all the variables, just have to scrape them
	_OUTPUT_FILE = '../output/all_vars.csv'
	main(_VAR_URL, _OUTPUT_FILE)