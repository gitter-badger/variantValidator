import unittest
from VariantValidator.modules.variant_external_resources import get_external_resource_links

class TestExternalLinks(unittest.TestCase):

    def test_valid_variant(self):
        # test successful outcome for a valid variant
        output = get_external_resource_links('NM_000088.3:c.589G>T')
        self.assertEqual(output, {
            'dbsnp': 'https://www.ncbi.nlm.nih.gov/snp/8179178', 
            'clinvar': 'http://www.ncbi.nlm.nih.gov/clinvar/RCV000490693.1'
            })
 
    def test_empty_rsid(self):
        # test message returned when RSID isn't found by NCBI Variation services
        output = get_external_resource_links('NC_000006.11:g.102503229C>T')
        self.assertEqual(output, {
            'error_msg': "An error occurred: SPDI 'NC_000006.11:102503228:C:T' does not match any RSID", 
            'error_code': '404'
            })

    def test_empty_variant(self):
        # test when an empty string is given as input
        output = get_external_resource_links('')
        self.assertEqual(output, {
            'error_msg': "Please enter a HGVS Genomic Variant"
        })
     
    def test_not_in_clinvar(self):
        # test when the variant is present in dbSNP but not in ClinVar
        output = get_external_resource_links('NM_032119.3:c.17667C>G')
        self.assertEqual(output, {
            'dbsnp': 'https://www.ncbi.nlm.nih.gov/snp/56382582'
        })

    def test_invalid_variant(self):
        # test when an invalid variant is submitted
        output = get_external_resource_links('NM_000088.3:c.589G>TX')
        self.assertEqual(output, {'error_msg': "An error occurred: Error while processing 'NM_000088.3:c.589G>TX': This change should be expressed as a delins.",
       'error_code': '400'})




