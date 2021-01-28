# Variant Validator frequency and constraint project

We gathered user stories from STP trainees, clinical scientists and research scientists to identify what information would be useful to incorporate into Variant Validator(https://trello.com/b/ZX7FfQJP/gnomadvv). The Users wanted to see information such as variant allele frequencies and regional constraint scores as this will reduce time spent searching for this information, reduce errors and missing data and provide an improved training resource for the future. Currently, to receive this data, Users are required to search for the variant in GnomAD using VCF descriptions or search through the variant list on the GnomAD page for the gene of interest, this can be a long and error prone process. For regional constraint scores, individuals would need to search the ExAC V1 database (only available for some genes) or other sources such as decipher to find this information. Upon further discussions, we updated our user requirements to include allele frequencies for all populations and global constraint scores. Our original aim was to utilise a GnomAD API to extract allele frequencies and an ExAC API to extract the global constraint scores. We quickly realised that the available third party API [GnomAD API](https://github.com/furkanmtorun/gnomad_python_api) would not function as we needed it to, the only way to query the API was using RSIDs which are not appropriate (because they refer to a locus and not a specific variant). We raised an issue on Github but the issue is not going to be resolved and so we were required to identify an alternative. We therefore decided to use an ExAC API to extract the allele frequencies. The code we have written produces a dictionary which contains the allele frequencies, population acs, population homozygotes and global gene constraint scores for a given variant.

## Installation

The ExAC constraint information is available from MyGene [https://docs.mygene.info/projects/mygene-py/en/latest/](https://docs.mygene.info/projects/mygene-py/en/latest/) and so this will need to be installed prior to the script being run. For example:

```bash
pip install mygene
```

## Usage

For the allele frequency use, the script requires a variant in VCF format (for example 14-21853913-T-C) as this allows data collection from the API. When this is incorporated into Variant Validator, the variant of interest can be directly added into the script.

For the constraint scores, the script requires an ensembl transcript ID for the API use, as above, when incorporated into Variant Validator the canonical or reference transcript can be directly incorporated.
 
The script can be run using:

```bash
python vvExacData.py
```

## Output

This script outputs a python dictionary (exac_data) which contains allele frequency, populations acs and population homozygotes for the variant requested and constraint scores for the transcript requested. The separate variant and constraint information will be easily accessible and specific information can be extracted for specific needs. For future use in VariantValidator, the required information can be extracted from the dictionary to create a table that can be presented on VariantValidator. 

##  Development

Now that the data is available in a single dictionary, it should be possible to integrate into Variant Validator so that Variant Validator queries also return both frequency data and missense/LOF constraint information. Going forward, it would be beneficial to replace this data with information from GnomAD, as GnomAD is most commonly used in the clinic for variant interpretation (because the dataset is much larger, more diverse and more up to date). Unfortunately, the allele frequency information cannot currently be extracted from GnomAD using an API because the third-party API is not functional, and the Broad institute have not developed their own API. Constraint data can only be accessed with reference to ExAC, global constraint scores are available in GnomAD but an API would be required to access this data. Following development of a GnomAD API, or the improvement of the existing third-party API, it may be possible to integrate the data into Variant Validator. 

In our user stories, some of our users suggested that regional constraint would also be beneficial. This work was out of the scope of this project but in future it would be beneficial to many of the users to incoporate this data into the script. When the data is availble through an API it can easily be extracted and added to the current nested dictionary. 
