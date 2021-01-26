# ensure mygene has been installed before
# import required modules
import json
import mygene
import requests

# create empty dictionary called exac_data_dict ..... - Sophie

# Take VCF variant description from Variant Validator and request data from exac database for variant
variant = "12-56360876-G-A"
r = requests.get('http://exac.hms.harvard.edu//rest/variant/variant/{}'.format(variant))
exac_freq = r.json()

# if loop to run through r, 400 and 404 will print errors and 200 means requests has worked and can continue
if r == "Response [400]":
	print(exac_freq)
elif r == "Response [404]":
	print(exac_freq)
else:
	print("Request OK")

#  pull information from allele frequency data
freq = exac_freq['allele_freq']
print(freq)
pop_homs = exac_freq['pop_homs']
print(pop_homs)

# add allele frequency data into new dictionary - Sophie

# Take canonical or reference transcript from variant validator and request data from mygene using exac fields 

transcript = "ENST00000266970"

r2 = requests.get('http://mygene.info/v3/query?q=exac.transcript:{}&fields=exac'.format(transcript))
constraint_data = r2.json()

# if loop to run through r2, 400 and 404 will print errors and 200 means requests has worked and can continue 
if r2 == "Response [400]":
	print(constraint_data)
elif r2 == "Response [404]":
	print(constraint_data)
else:
	print("Request OK")

print(json.dumps(constraint_data, sort_keys=True, indent=4, separators=(',', ': ')))

# loop to extract separated scores (e.g. lof_z) from nested dictionary constraint_data
#lof_scores = null
#for key, val in constraint_data.items():
#	try:
#		if "exac" in  val.keys():
#			break
#			for key ,val in exac.items:
#				try:
#					if "all" in val.keys():
#						break
#						for key, val in all.keys():
#							try:
#								if "lof_z" in all.keys():
#									lof_scores = val['lof_z']
#							except AttributeError:
#								continue
#print(lof_scores)

#or loop to extract the whole "all" dictionary from nested dictionary constraint_data - this would be ideal

#constraint_scores = null
#for key, val in constraint_data.items():
#	try:
#		if "exac" in  val.keys():
#		break
#			for key ,val in exac.items:
#				try:
#					if "all" in val.keys():
#					constraint_scores = all
#				break
#				except AttributeError:
#				continue


# print(json.dumps(exac_data_dict, sort_keys=True, indent=4, separators=(',', ': ')))

# add  constraint scores into dictionary - Sophie





# <LICENSE>
# Copyright (C) 2021 VariantValidator Contributors
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# </LICENSE>
