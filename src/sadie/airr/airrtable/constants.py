from typing import Any, Dict

IGBLAST_AIRR: Dict[Any, str] = {
    "sequence_id": "object",
    "sequence": "object",
    "locus": "object",
    "stop_codon": "object",
    "vj_in_frame": "object",
    "v_frameshift": "object",
    "productive": "object",
    "rev_comp": "object",
    "complete_vdj": "object",
    "sequence_alignment": "object",
    "sequence_alignment_aa": "object",
    "germline_alignment": "object",
    "germline_alignment_aa": "object",
    "fwr1": "object",
    "fwr1_aa": "object",
    "fwr1_start": "Int16",
    "fwr1_end": "Int16",
    "cdr1": "object",
    "cdr1_aa": "object",
    "cdr1_start": "Int16",
    "cdr1_end": "Int16",
    "fwr2": "object",
    "fwr2_aa": "object",
    "fwr2_start": "Int16",
    "fwr2_end": "Int16",
    "cdr2": "object",
    "cdr2_aa": "object",
    "cdr2_start": "Int16",
    "cdr2_end": "Int16",
    "fwr3": "object",
    "fwr3_aa": "object",
    "fwr3_end": "Int16",
    "fwr3_start": "Int16",
    "cdr3": "object",
    "cdr3_aa": "object",
    "cdr3_end": "Int16",
    "cdr3_start": "Int16",
    "fwr4": "object",
    "fwr4_aa": "object",
    "fwr4_end": "Int16",
    "fwr4_start": "Int16",
    "v_alignment_start": "Int16",
    "v_alignment_end": "Int16",
    "v_call": "object",
    "v_cigar": "object",
    "v_germline_alignment": "object",
    "v_germline_alignment_aa": "object",
    "v_germline_start": "Int16",
    "v_germline_end": "Int16",
    "v_identity": "float32",
    "v_score": "float32",
    "v_sequence_alignment": "object",
    "v_sequence_alignment_aa": "object",
    "v_sequence_start": "Int16",
    "v_sequence_end": "Int16",
    "v_support": "float64",
    "d_alignment_start": "Int16",
    "d_alignment_end": "Int16",
    "d_call": "object",
    "d_cigar": "object",
    "d_germline_alignment": "object",
    "d_germline_alignment_aa": "object",
    "d_germline_start": "Int16",
    "d_germline_end": "Int16",
    "d_identity": "float32",
    "d_score": "float32",
    "d_sequence_alignment": "object",
    "d_sequence_alignment_aa": "object",
    "d_sequence_start": "Int16",
    "d_sequence_end": "Int16",
    "d_support": "float64",
    "j_alignment_start": "Int16",
    "j_alignment_end": "Int16",
    "j_call": "object",
    "j_cigar": "object",
    "j_germline_alignment": "object",
    "j_germline_alignment_aa": "object",
    "j_germline_start": "Int16",
    "j_germline_end": "Int16",
    "j_identity": "float32",
    "j_score": "float32",
    "j_sequence_alignment": "object",
    "j_sequence_alignment_aa": "object",
    "j_sequence_start": "Int16",
    "j_sequence_end": "Int16",
    "j_support": "float64",
    "junction": "object",
    "junction_aa": "object",
    "junction_aa_length": "Int16",
    "junction_length": "Int16",
    "np1": "object",
    "np1_length": "Int16",
    "np2": "object",
    "np2_length": "Int16",
}

CONSTANTS_AIRR = {
    "c_call": "object",
    "c_cigar": "object",
    "c_germline_alignment": "object",
    "c_germline_alignment_aa": "object",
    "c_germline_start": "Int16",
    "c_germline_end": "Int16",
    "c_identity": "float32",
    "c_score": "float32",
    "c_sequence_alignment": "object",
    "c_sequence_alignment_aa": "object",
    "c_sequence_start": "Int16",
    "c_sequence_end": "Int16",
    "c_support": "float64",
}

OTHER_COLS = {
    "d_call_top": "object",
    "d_mutation": "float32",
    "d_mutation_aa": "float32",
    "d_penalty": "Int16",
    "germline_alignment_aa_corrected": bool,
    "iGL": "object",
    "iGL_aa": "object",
    "j_call_top": "object",
    "j_mutation": "float32",
    "j_mutation_aa": "float32",
    "j_penalty": "Int16",
    "liable": "bool",
    "padded_five_prime": "bool",
    "padded_three_prime": "bool",
    "reference_name": "object",
    "v_call_top": "object",
    "v_germline_alignment_aa_corrected": "bool",
    "v_mutation": "float32",
    "v_mutation_aa": "float32",
    "v_penalty": "Int16",
    "vdj_aa": "object",
    "vdj_aa": "object",
}
