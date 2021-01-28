
## ensure mygene has been installed before
# import required modules
import json
#import mygene
import requests

# create empty dictionary called exac_data_dict ..... - Sophie

# Take VCF variant description from Variant Validator and request data from exac database for variant
variant = "14-21853913-T-C"
r = requests.get('http://exac.hms.harvard.edu//rest/variant/variant/{}'.format(variant))
exac_freq = r.json()
population_freq = exac_freq['allele_freq']
homozygotes = exac_freq['pop_homs']
population_acs = exac_freq['pop_acs']
#print(type(exac_freq))

# if loop to run through r, 400 and 404 will print errors and 200 means requests has worked and can continue
if r == "Response [400]":
	print(exac_freq)
elif r == "Response [404]":
	print(exac_freq)
else:
	print("Request OK")
#create dictionary for population frequencies
variant_dictionary = {}
#  transfer pop_homs and pop_acs to variant_dictionary
variant_dictionary['allele_freq'] = population_freq
variant_dictionary['pop_homs'] = homozygotes
variant_dictionary['pop_acs'] = population_acs
#population_frequency = exac_freq['population_freq']
#population_counts = exac_freq['pop_acs']
print(variant_dictionary)

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
    #try:
        #if "exac" in  val.keys():
        #    continue
       # for key ,val in exac.items():
            #try:
                #if "all" in val.keys():
                #    continue
               # for key, val in all.keys():  # you have collected key and val but arent using them
                   # try:
                      #  if "lof_z" in key: # This could be in key since you collected key
                     #      lof_scores = val['lof_z']
                    #except:
                        #AttributeError:\
                         #   print("Attribute error, please start again and select another transcript")
                        #continue
                        #break
                            #print(lof_scores)

###NEW SCRIPT SOPHIE - loop to extract the whole "all" dictionary from nested dictionary constraint_data - this would be ideal
#constraint data[exac[]]
exac_constraint = {}
exac_data = {}

for hit in constraint_data['hits']:
    try:
        exac_constraint = hit['exac']['all']
    except KeyError:
        print("Key not found! APIs are a pain in the bum!")
    finally:
        print(exac_constraint)

exac_data.update(variant_dictionary)
exac_data.update(exac_constraint)
print(exac_data)


# constraint_scores = None
# for key, val in constraint_data.items():
#     try:
#         if "hits" in constraint_data.keys():
#             break
#         if "exac" in hits.keys():
#             break
#         for key ,val in exac.items():
#             if "all" in exac.keys():
#                 print(exac.keys)
#                 constraint_scores = all
#                 break
#     except AttributeError:
#                 print('Attribute error, please start again and select another transcript')
# print(constraint_scores)
# print(json.dumps(constraint_scores, sort_keys=True, indent=4, separators=(',', ': ')))

# print(json.dumps(exac_data_dict, sort_keys=True, indent=4, separators=(',', ': ')))

# dummy code for dictionary merging later 





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