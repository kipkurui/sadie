"""
This type stub file was generated by pyright.
"""

from Bio.Align import MultipleSeqAlignment as MultipleSeqAlignment
from Bio.File import as_handle as as_handle
from Bio.SeqIO import (
    AbiIO as AbiIO,
    AceIO as AceIO,
    FastaIO as FastaIO,
    GckIO as GckIO,
    IgIO as IgIO,
    InsdcIO as InsdcIO,
    NibIO as NibIO,
    PdbIO as PdbIO,
    PhdIO as PhdIO,
    PirIO as PirIO,
    QualityIO as QualityIO,
    SeqXmlIO as SeqXmlIO,
    SffIO as SffIO,
    SnapGeneIO as SnapGeneIO,
    SwissIO as SwissIO,
    TabIO as TabIO,
    TwoBitIO as TwoBitIO,
    UniprotIO as UniprotIO,
    XdnaIO as XdnaIO,
)
from Bio.SeqRecord import SeqRecord as SeqRecord
from typing import Any

def write(sequences, handle, format) -> None: ...
def parse(handle, format, alphabet: Any | None = ...): ...
def read(handle, format, alphabet: Any | None = ...): ...
def to_dict(sequences, key_function: Any | None = ...): ...
def index(filename, format, alphabet: Any | None = ..., key_function: Any | None = ...): ...
def index_db(
    index_filename,
    filenames: Any | None = ...,
    format: Any | None = ...,
    alphabet: Any | None = ...,
    key_function: Any | None = ...,
): ...
def convert(in_file, in_format, out_file, out_format, molecule_type: Any | None = ...): ...
