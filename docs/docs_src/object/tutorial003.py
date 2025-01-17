from pprint import pprint

from sadie.receptor.rearrangment import AlignmentAnnotations

# Model 3 - Alignment Annotations
alignment_annotations_model = AlignmentAnnotations(
    sequence_alignment="CAGGTGCAGCTGGTGCAGTCTGGGGGTCAGATGAAGAAGCCTGGCGAGTCGATGAGAATTTCTTGTCGGGCTTCTGGATATGAATTTATTGATTGTACGCTAAATTGGATTCGTCTGGCCCCCGGAAAAAGGCCTGAGTGGATGGGATGGCTGAAGCCTCGGGGGGGGGCCGTCAACTACGCACGTCCACTTCAGGGCAGAGTGACCATGACTCGAGACGTTTATTCCGACACAGCCTTTTTGGAGCTGCGCTCGTTGACAGTAGACGACACGGCCGTCTACTTTTGTACTAGGGGAAAAAACTGTGATTACAATTGGGACTTCGAACACTGGGGCCGGGGCACCCCGGTCATCGTCTCATCAG",
    sequence_alignment_aa="QVQLVQSGGQMKKPGESMRISCRASGYEFIDCTLNWIRLAPGKRPEWMGWLKPRGGAVNYARPLQGRVTMTRDVYSDTAFLELRSLTVDDTAVYFCTRGKNCDYNWDFEHWGRGTPVIVSS",
    germline_alignment="CAGGTGCAGCTGGTGCAGTCTGGGGCTGAGGTGAAGAAGCCTGGGGCCTCAGTGAAGGTCTCCTGCAAGGCTTCTGGATACACCTTCACCGGCTACTATATGCACTGGGTGCGACAGGCCCCTGGACAAGGGCTTGAGTGGATGGGATGGATCAACCCTAACAGTGGTGGCACAAACTATGCACAGAAGTTTCAGGGCAGGGTCACCATGACCAGGGACACGTCCATCAGCACAGCCTACATGGAGCTGAGCAGGCTGAGATCTGACGACACGGCCGTGTATTACTGTGCGAGNNNNNNNNNNNNTGATTACGTTTGGGACTTCCAGCACTGGGGCCAGGGCACCCTGGTCACCGTCTCCTCAG",
    germline_alignment_aa="QVQLVQSGAEVKKPGASVKVSCKASGYTFTGYYMHWVRQAPGQGLEWMGWINPNSGGTNYAQKFQGRVTMTRDTSISTAYMELSRLRSDDTAVYYCAXXXXXDYVWDFQHWGQGTLVTVSS",
    v_score=168.2,
    d_score=17.8,
    j_score=52.6,
    v_identity=0.6825,
    d_identity=0.85,
    j_identity=0.86,
    v_cigar="6S293M76S3N",
    d_cigar="311S6N14M50S17N",
    j_cigar="325S7N45M5S",
    v_support=6.796e-44,
    d_support=0.5755,
    j_support=5.727e-11,
    junction="TGTACTAGGGGAAAAAACTGTGATTACAATTGGGACTTCGAACACTGG",
    junction_aa="CTRGKNCDYNWDFEHW",
    np1="GGGAAAAAACTG",
    c_score=100,
    c_identity=1,
    c_support=1e-44,
    c_cigar="6S293M76S3N",
)
# alignment_sequence_annotation_model = AlignmentAnnotations(**alignment_dict)
pprint(alignment_annotations_model.__dict__)
