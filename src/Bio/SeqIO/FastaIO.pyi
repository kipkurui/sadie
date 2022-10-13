from collections.abc import Generator
from typing import Any

from Bio.Seq import Seq as Seq
from Bio.SeqRecord import SeqRecord as SeqRecord

from .Interfaces import SequenceIterator as SequenceIterator
from .Interfaces import SequenceWriter as SequenceWriter

def SimpleFastaParser(handle) -> Generator[Any, None, None]: ...
def FastaTwoLineParser(handle) -> Generator[Any, None, None]: ...

class FastaIterator(SequenceIterator):
    title2ids: Any
    def __init__(self, source, alphabet: Any | None = ..., title2ids: Any | None = ...) -> None: ...
    def parse(self, handle): ...
    def iterate(self, handle) -> Generator[Any, None, None]: ...

class FastaTwoLineIterator(SequenceIterator):
    def __init__(self, source) -> None: ...
    def parse(self, handle): ...
    def iterate(self, handle) -> Generator[Any, None, None]: ...

class FastaWriter(SequenceWriter):
    wrap: Any
    record2title: Any
    def __init__(self, target, wrap: int = ..., record2title: Any | None = ...) -> None: ...
    def write_record(self, record) -> None: ...

class FastaTwoLineWriter(FastaWriter):
    def __init__(self, handle, record2title: Any | None = ...) -> None: ...

def as_fasta(record): ...
def as_fasta_2line(record): ...
