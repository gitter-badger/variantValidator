"""

Script to check syntax of expanded repeat variants
By Rebecca Locke + Rob Wilson

"""
# Import modules
import re

#  List of variants to check format and split into constituents
variant1="LRG_199t1:c.1ACT[20]"
variant2 = "LRG_199:g.1ACT[20]A"
variant3 = "LRG_199:g.1AC[20]"
variant4 = "LRG_199t1:c.1_3ACT[20]"
variant5 = "LRG_199t1:c.1AC[20]"
variant6 = "LRG_199t1:c.1act[20]"
variant7 = "LRG199:c.1A[12]"
variant8 = "LRG_199:g.13ACT[20]"
variant9 = "LRG_199:g.13_25ACTG[12]"
variant10 = "LRG199:g.13_125ACTG[1]"
variant11 = "ENSG00000198947.15:g.1ACT[10]"
variant12 = "ENST00000357033.8:c.13AC[22]"
variant13 = "LRG_199t1:c.1_2ACT[20]"
variant14 = "LRG_199t1:c.20A[A]"
variant15 = "NM_004006.2:c.13AC[22]"
variant15 = "NR_004430.2:c.13AC[22]"
variant16 = "LRG_199t1:c.ACT1_3[20]"
variant17 = "NG_004006.2:g.1_2act[22]"

# Parse the variant to get relevant parts
def parse_repeat_variant(my_variant):
    """
    Summary:
    This takes a variant string and breaks it into its constituents with regex.

    Args:
        my_variant (string): Variant string e.g. "LRG_199:g.1ACT[20]A"
    Returns:
        prefix (string): Everything before the first colon, e.g. "LRG_199"
        var_type (string): The variant genomic or coding type e.g. "g"
        var_pos (string): Position of the variant, e.g. "1" or "1_12"
        repeated_seq (string): The repeated sequence e.g. "ACT"
        no_of_repeats (string): The number of repeat units e.g. "20"
        after_the_bracket (string): Captures anything after the number of repeats bracket e.g. "A"
    """
    if "[" or "]" in my_variant:
        assert ":" in my_variant, f"Unable to identify a colon (:) in the variant description {my_variant}. A colon is required in HGVS variant descriptions to separate the reference accession from the reference type i.e. <accession>:<type>. e.g. :c"
        prefix, suffix = my_variant.split(":")
        # Find reference sequence used (g or c)
        variant_type = re.search('^.*?(.*?)\.', suffix)
        var_type = variant_type.group(1)
        # Get g or c position(s)
        #Extract bit between . and [ e.g. 1ACT
        pos_and_seq = suffix.split(".")[1].split("[")[0]
        assert re.search("[a-z]+", pos_and_seq, re.IGNORECASE), "Please ensure that the repeated sequence is included between the position and number of repeat units, e.g. g.1ACT[20]"
        rep_seq = re.search("[ACTG]+", pos_and_seq, re.IGNORECASE)
        repeated_seq = rep_seq.group()
        if "_" in pos_and_seq:
            assert re.search("[0-9]+_[0-9]+", pos_and_seq), "Please ensure the start and the end of the full repeat range is provided, separated by an underscore"
            variant_positions = re.search("[0-9]+_[0-9]+", pos_and_seq)
            var_pos = variant_positions.group()
        else:
            variant_position = re.search("\d+", pos_and_seq)
            var_pos = variant_position.group()
        # Get number of unit repeats
        repeat_no = re.search('\[(.*?)\]', my_variant)
        no_of_repeats = repeat_no.group(1)
        # Get anything after ] to check
        if re.search('\](.*)',my_variant):
            after_brac = re.search('\](.*)',my_variant)
            after_the_bracket = after_brac.group(1)
        else:
            after_the_bracket = None
        return prefix, var_type, var_pos, repeated_seq, no_of_repeats, after_the_bracket

variant_check = parse_repeat_variant(variant1)

the_prefix = variant_check[0]
variant_type = variant_check[1]
variant_position = variant_check[2]
repeated_sequence = variant_check[3]
number_of_repeats = variant_check[4]
after_bracket = variant_check[5]

print(the_prefix, variant_type, variant_position, repeated_sequence, number_of_repeats, after_bracket)

print(after_bracket)

def check_transcript_type(prefix):
    """
    [Find transcript type. N.B. Future development could instead store
    the transcript and replace it with refseq.]
    Args:
        prefix (string): The prefix from parse_variant_repeat
    Returns: 
        None, prints variant type
    Raises:
        NameError: [Error for unknown transcript type.]
    """
    if bool(re.match(r"^LRG", prefix)):
        print("LRG variant")
        # reformat_prefix_LRG(prefix)
    elif bool(re.match(r"^E", prefix)):
        print("Ensembl variant")
    elif bool(re.match(r"^N", prefix)):
        print("RefSeq variant")
    else:
        raise NameError('Unknown transcript type present. \
                        Try RefSeq transcript ID')

check_transcript_type(the_prefix)

def reformat_prefix(prefix):
    if re.match(r'^LRG', prefix):
        if re.match(r'^LRG\d+', prefix):
            prefix = prefix.replace('LRG','LRG_')
            print("LRG variant updated to include underscore")
        # Get transcript number
        if "t" in prefix:
            transcript_num = re.search("t(.*?)$", prefix)
            transcript_version = f"t{transcript_num.group(1)}"
            print(transcript_version)
    return prefix

the_prefix = reformat_prefix(the_prefix)

def check_genomic_or_coding(prefix, var_type):
    """Takes prefix and works out if variant type should be c. or g. and raises error if incorrect type supplied
    Args:
        prefix (string): The prefix e.g. "LRG_199"
        var_type (string): Variant type genomic or coding e.g. "g"
    """
    if re.match(r'^LRG', prefix):
        if "t" in prefix:
            assert var_type == "c", "Please ensure variant type is coding if an LRG transcript is provided"
        else:
            assert var_type == "g", "Please ensure variant type is genomic if LRG gene is used"
    elif re.match(r'^ENST', prefix):
        assert var_type == "c", "Please ensure variant type is coding if an Ensembl transcript is provided"
    elif re.match(r'^ENSG', prefix):
        assert var_type == "g", "Please ensure variant type is genomic if Ensembl gene is used"
    elif re.match(r'^NM', prefix):
        assert var_type == "c", "Please ensure variant type is coding if a RefSeq transcript is provided"
    elif re.match(r'^NC', prefix):
        assert var_type == "g", "Please ensure variant type is genomic if RefSeq chromosome is used"
    elif re.match(r'^NG', prefix):
        assert var_type == "g", "Please ensure variant type is genomic if RefSeq gene is used"

check_genomic_or_coding(the_prefix, variant_type)

# For variants with the full range of the position given (not only start pos)
def check_positions_given(repeated_sequence, variant_pos, no_of_rep_units):
    """Checks the position range given and updates it if it doesn't make match the length of the repeated sequence and number of repeat units
        Args:
        repeated_sequence (string): The repeated sequence e.g. "ACT"
        variant_pos (string): The position of the variant e.g. "1" or "1_5"
        no_of_rep_units (string): The number of repeat units e.g. "20"
    Returns: 
        full_range (string): The full range supplied if correct or the full range updated if inputted range was incorrect, e.g. "1_20"
    """
    start_range, end_range = variant_pos.split("_")
    rep_seq_length = len(repeated_sequence)
    the_range = int(end_range) - int(start_range) + 1
    repeat_length = (rep_seq_length * int(no_of_rep_units))
    if the_range == repeat_length:
        print("Range given matches repeat sequence length and number of repeat units")
        full_range = f"{start_range}_{end_range}"
    else:
        print("Warning: sequence range (X_X) given must match repeat unit sequence length and number of repeat units. Updating the range based on repeat sequence length and number of repeat units")
        new_end_range = int(start_range) + repeat_length - 1
        full_range = f"{start_range}_{new_end_range}"
    return full_range

# Reformat the variant for HGVS consistency
def reformat(var_prefix,the_variant_type, the_var_pos, the_repeated_sequence, the_number_of_repeats, all_after_bracket):
    # Check number of repeat units is integers and that the sequence is A,C,T or G
    assert the_number_of_repeats.isdecimal(),"The number of repeat units included between square brackets must be numeric"
    assert re.search("[actg]+", the_repeated_sequence, re.IGNORECASE), "Please ensure the repeated sequence includes only A, C, T or G"
    # Update the repeated sequence to be upper case
    the_repeated_sequence = the_repeated_sequence.upper()
    if "_" in the_var_pos:
        the_var_pos = check_positions_given(the_repeated_sequence, the_var_pos, the_number_of_repeats)
    if all_after_bracket != "":
        print("No information should be included after the number of repeat units. Mixed repeats are currently not supported.")
    return f"{var_prefix}:{the_variant_type}.{the_var_pos}{the_repeated_sequence}[{the_number_of_repeats}]"

print(reformat(the_prefix, variant_type, variant_position, repeated_sequence, number_of_repeats, after_bracket))

# Working on this now 
def convert_not_multiple_of_three(vartype, position, rep_seq, no_of_repeats):
    if len(rep_seq) % 3 != 0:
        print("Repeated sequence is not a multiple of three!")


"""Other useful functions"""

def check_no_repeats(start_range, end_range, repeated_sequence):
    rep_seq_length = len(repeated_sequence)
    the_range = int(end_range) - int(start_range) + 1
    no_of_units = int(the_range / rep_seq_length)
    return no_of_units

# Note Community Consultation is prepared which will suggest to allow only one format where the entire range of the repeated sequence must be indicated, e.g. g.123_191CAG[23]. This small function will give you the range from getting only a start position
def get_range_from_single_pos(repeated_sequence, start_range, no_of_rep_units):
    rep_seq_length = len(repeated_sequence)
    repeat_length = (rep_seq_length * int(no_of_rep_units))
    the_end_range = int(start_range) + repeat_length - 1
    full_range = f"{start_range}_{the_end_range}"
    return full_range

#if __name__ == "__main__":
#    main()
