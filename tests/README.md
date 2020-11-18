# Pytests for variant_external_resources.py  (VER) added to variantValidator/tests/test_variant_external_resources.py

## 1)  successful request for example variant
	 GIVEN I have a valid variant and it exists in ClinVar and dbSNP
	 WHEN I input a single variant 'NM_000088.3:c.589G>T'  into VER
	 THEN the expected result is {'dbsnp': 'https://www.ncbi.nlm.nih.gov/snp/8179178', 'clinvar': 'http://www.ncbi.nlm.nih.gov/clinvar/RCV000490693.1'}
	 
	Added to Pytests: test_valid_variant
	 
## 2) HCBI Variant Services unavailable
	 GIVEN I have a valid variant and it exists in ClinVar and dbSNP
	 WHEN I input a single variant 'NM_000088.3:c.589G>T'  into VER 
	 AND Variant External Resource is unable to establish a connection
	 THEN the expected result is a ConnectionError
	 AND the warning message is - Unable to establish a connection to nlm.nih.gov/variation/v0/  to retrieve the links for dbSNP or ClinVar
	 
	Not added - not suitable for automated test
	 
## 3) test empty string input 
	GIVEN I don't have a valid variant
	WHEN I input an empty string ' ' into VER
	THEN the expected result is that a warning message is returned
	AND the warning message is - You have entered an empty string. Please enter a valid HGVS Genomic Variant
	 
	Added to Pytests: test_empty_variant

## 4)  successful test when variant exists only in dbSNP and not clinvar
	GIVEN I have a valid variant that exists in dbSNP but not on clinvar
	WHEN I input a single variant NM_032119.3:c.17667C>G into VER
	THEN the expected result is a dictionary with just one url for dbSNP {'dbsnp': 'https://www.ncbi.nlm.nih.gov/snp/5638258}
	 
	Added to Pytests: test_not_in_clinvar
	 
## 5) successful test when variant exists only in ClinVar and not dbSNP
	GIVEN I have a valid variant 
    WHEN I input a single variant into VER
	THEN the expected result is a dictionary with just one url for ClinVar {'clinvar': 'some link'}
		 
	not added - unable to find an example at this time

# Test NCBI Variation services error messaging. These error messages come from NCBI and are returned via a dictionary**

##  6) test invalid variant input 
	GIVEN I have an invalid variant with an eroneous 'X' appended to the string
	WHEN I input 'NM_000088.3:c.589G>TX' into VER
	THEN the expected result is a dictionary with an entry for the error message
	 
	Added to Pytests: test_invalid_variant
	 
## 7) test when no RSID found 
	GIVEN I have a valid variant and it doesn't have an RSID 
	WHEN I input a single variant 'NC_000006.11:g.102503229C>T' into VER
	THEN the expected result is a dictionary with an entry for the error message
	 
	Added to Pytests: test_empty_rsid

# API  Suggested tests for variant_external_resources.py when called by vvweb 

**Note tests 8-13 have not been implemented at this time**

## 8) successful request for valid variant 
	 GIVEN I have a valid variant and it exists in ClinVar and dbSNP
	 WHEN I input a single variant 'NM_000088.3:c.589G>T' on the VV page and select GRCh37 (hg19, build19) 
	 THEN the expected result is a link for dbSNP which takes me to https://www.ncbi.nlm.nih.gov/snp/rs8179178
     AND a link for clinvar which takes me to https://www.ncbi.nlm.nih.gov/clinvar/RCV000490693.1/

 ## 9) successful test when variant exists only in dbSNP and not clinvar 
	GIVEN I have a valid variant that exists in dbSNP but not on clinvar
	WHEN I input a single variant NM_032119.3:c.17667C>G on the VV page and select 
	THEN the expected result is a dictionary with just one url for dbSNP {'dbsnp': 'https://www.ncbi.nlm.nih.gov/snp/5638258} 
	 
## 10) HCBI Variant Services unavailable - do we want a test for this or let vvweb handle it? 
	 GIVEN I have a valid variant and it exists in ClinVar and dbSNP
	 WHEN I input a single variant 'NM_000088.3:c.589G>T'  on the VV page and select GRCh37 (hg19, build19)
	 AND vvweb is unable to establish a connection
	 THEN the expected result is a ConnectionError
	 AND the warning message is - Unable to establish a connection to nlm.nih.gov/variation/v0/  to retrieve the links for dbSNP or ClinVar
	        currently when no wifi connection VV fails with: Error
			Unable to validate the submitted variant NM_000088.3:c.589G>T against the GRCh37 assembly.
			Please check your submission and re-submit.

## 11) test empty string input - not applicable for vvweb - empty string handled by VV
	
## 12)  test invalid variant input - not applicable for vvweb will be picked up by VV
	 
## 13)  test when no RSID found
	GIVEN I have a valid variant and it doesn't have an RSID 
	WHEN I input a single variant 'NC_000006.11:g.102503229C>T' on the VV page and select GRCh37 (hg19, build19)
	THEN the expected result is that no url links will be included for dbSNP or clinvar 
	AND the warning message is 'no associated RSID was returned by NCBI Variant Services therefore dbSNP and ClinVar links have not been included in the output'