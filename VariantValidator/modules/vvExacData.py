
## ensure mygene has been installed before running this script

# import required modules
import json
import mygene
import requests


# Take VCF variant description from Variant Validator and request data from exac database for variant
variant = "14-21853913-T-C"
r = requests.get('http://exac.hms.harvard.edu//rest/variant/variant/{}'.format(variant))
exac_freq = r.json()

# if loop to run through r, 400 and 404 will print errors and 200 means requests has worked and can continue
if r == "Response [400]":
	print(exac_freq)
elif r == "Response [404]":
	print(exac_freq)
else:
	print("Request OK")

# extract population frequecies from the exac_freq dictionary
population_freq = exac_freq['allele_freq']
homozygotes = exac_freq['pop_homs']
population_acs = exac_freq['pop_acs']

# create empty dictionary for population frequencies
variant_dictionary = {}

# transfer, allele frequency, pop_homs and pop_acs to variant_dictionary
variant_dictionary['allele_freq'] = population_freq
variant_dictionary['pop_homs'] = homozygotes
variant_dictionary['pop_acs'] = population_acs

# check dictionary looks correct
print(variant_dictionary)

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

# the following line can be run to check the data has pulled correctly from the API if wanted
#print(json.dumps(constraint_data, sort_keys=True, indent=4, separators=(',', ': ')))

# loop to extract the whole "all" dictionary from nested dictionary constraint_data and print to ensure the loop has worked effectively
exac_constraint = {}
exac_data = {}

for hit in constraint_data['hits']:
    try:
        exac_constraint = hit['exac']['all']
    except KeyError:
        print("Key not found! APIs are a pain in the bum!")
    finally:
        print(exac_constraint)

# create nested dictionary of frequency data and constraint data
exac_data = {}
exac_data['frequency_data'] = variant_dictionary
exac_data['constraint_data'] = exac_constraint

# print final nested dictionary in json format to make it easier to read
print(json.dumps(exac_data, sort_keys=True, indent=4, separators=(',', ': ')))




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
