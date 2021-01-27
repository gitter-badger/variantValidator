# Variant Validator frequency and constraint project

We gathered user stories from STP trainees, clinical scientists and research scientists to identify what information would be useful to incorporate into Variant Validator(https://trello.com/b/ZX7FfQJP/gnomadvv). The Users wanted to see information such as variant allele frequencies and regional constraint scores as this will reduce time spent searching for this information, reduce errors and missing data and provide an improved training resource for the future. Currently, to receive this data, Users are required to search for the variant in GnomAD using VCF descriptions or search through the variant list on the GnomAD page for the gene of interest, this can be a long and error prone process. For regional constraint scores, individuals would need to search the ExAC V1 database (only available for some genes) or other sources such as decipher to find this information. Upon further discussions, we updated our user requirements to include allele frequencies for all populations and global constraint scores. Our original aim was to utilise a GnomAD API to extract allele frequencies and an ExAC API to extract the global constraint scores. We quickly realised that the available third party [GnomAD API](https://github.com/furkanmtorun/gnomad_python_api) would not function as we needed it to, the only way to query the API was using RSIDs which are not appropriate . We raised an issue on Github but the issue is not going to be resolved and so we were required to identify an alternative. We therefore decided to replace GnomAD with an ExAC API to extract the allele frequencies. The code we have written produces a dictionary which contains the allele frequencies, population homozygotes and gene constraint scores for a given variant.

## Installation

The ExAC constraint information is available from MyGene [https://docs.mygene.info/projects/mygene-py/en/latest/](https://docs.mygene.info/projects/mygene-py/en/latest/) and so this will need to be installed prior to the script being run. For example:

```bash
pip install mygene
```

## Usage

For the allele frequency use, the script asks the User to input a variant in VCF format (chromosome-position-ref-alt, for example 12-56360876-G-A) as this enables the script to search the ExAC API. 

Additionally, for the constraint scores, the script asks the user to input a transcript ID in ensembl format (for example, ENST00000266970) as this enables the script to search the MyGene ExAC API for constraint scores.

The script can be run using:

```bash
python vvExacData.py
```

## Output

This script outputs a python dictionary (exac_data) which contains allele frequency and population homozygotes for the variant requested and constraint scores for the transcript requested. The separate variant and constraint information will be easily accessible and specific information can be extracted for specific needs. For future use in VariantValidator, the required information can be extracted from the dictionary to create a table that can be presented on VariantValidator. 

