import requests
import csv
import os
from bs4 import BeautifulSoup
from user_agent import generate_user_agent
import time
from tqdm import tqdm

def modify_url(url):
	'''turn `https://www.icpsr.umich.edu/icpsrweb/ICPSR/ssvd/studies/04406/datasets/0001/variables/DRG8ING5?q=*&paging.startRow=1`
	   into `https://www.icpsr.umich.edu/icpsrweb/ICPSR/studies/04406`'''
	modified_url = url.split('/datasets/')[0].replace('ssvd/', '')
	return modified_url


def fetch_doi(url):
	'''load url, get the doi'''
	print("Getting doi for {}".format(url))
	AGENT = generate_user_agent(device_type = "desktop", os=('mac', 'linux')) #new agent each time
	headers = {'User-Agent':AGENT}
	try:
		res = requests.get(url, headers=headers)
		soup = BeautifulSoup(res.content, "html.parser")
		doi = soup.select("p.doi")
		doi_text = doi[0].text
	except Exception as e:
		print("Could not parse: {} == {}".format(url, e))
		doi_text = None
	
	return doi_text


def get_len_csv(csvfile):
	with open(csvfile, 'r', encoding='utf-8') as countfile:
		reader = csv.reader(countfile)
		header = next(reader)
		csvlen = sum(1 for r in reader)
	return csvlen


def unique_datasets(csvfile):
	print("fetching unique datasets from: {}".format(csvfile))
	unique_datasets = []
	with open(csvfile, 'r', encoding='utf-8') as infile:
		reader = csv.reader(infile)
		header = next(reader)
		csvlen = get_len_csv(csvfile)
		for row in tqdm(reader, total=csvlen):
			updated_url = modify_url(row[2])
			if updated_url not in unique_datasets:
				unique_datasets.append((row[2],updated_url))
	return unique_datasets

if __name__ == '__main__':

	all_vars_csv = './output/all_in_one/all_vars.csv'
	doi_xwalk = './output/doi_xwalk.csv'
	unique_only = unique_datasets(all_vars_csv)
	print("Got {} datasets to match".format(len(unique_only)))

	xwalk = []
	for i in unique_only:
		doi_match = fetch_doi(i[1])
		xwalk.append((i[0], i[1], doi_match))


	with open(doi_xwalk, 'w', encoding='utf-8') as doiout:
		writer = csv.writer(doiout)
		header = ['url', 'updated_url', 'doi']
		writer.writerow(header)
		for row in xwalk:
			writer.writerow(row)
