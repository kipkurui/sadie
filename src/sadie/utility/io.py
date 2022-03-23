from pathlib import Path
import warnings
from filetype import guess
from filetype.types.base import Type
from filetype.types.archive import Gz, Bz2
import gzip
import bz2
from typing import IO, Iterator, TextIO, Union, Any

from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from Bio.SeqIO.AbiIO import AbiIterator
from Bio.SeqIO.FastaIO import FastaIterator
from Bio.SeqIO.QualityIO import FastqPhredIterator


class NoExtensionNameWarning(UserWarning):
    pass


def guess_input_compression(input_path: Union[str, Path]) -> Union[str, None]:
    """Given a path, guess if it's compressed gz,bz2 or directory.
    If not compressed returned None

    Parameters
    ----------
    input_path : str
        input is compressed

    Returns
    -------
    Union[str,None]
        returns gz, bz2 or None

    Raises
    ------
    NotImplementedError
        If the file type compression is unsupported
    """

    # check if directory first
    if Path(input_path).is_dir():
        return "directory"

    # if not directory, check if it's bz2 or gz2 archive
    _filetype: Union[Type, None] = guess(str(input_path))
    if not _filetype:
        return None
    extension: str = _filetype.extension
    if isinstance(_filetype, (Gz, Bz2)):
        return extension
    else:
        raise NotImplementedError(f"filetype {extension} not supproted")


def get_file_buffer(file: Path, compression: Union[str, None] = None, mode: str = "rt") -> Union[TextIO, IO[Any]]:
    """Open a file with the correct file buffer

    Parameters
    ----------
    file : Path
        file path
    compression : str
        compression type, 'bz2', 'gz', None

    Returns
    -------
    TextIO
        Usually a TextIOWrapper

    Raises
    ------
    TypeError
        Can't determine file type
    """
    # get file buffer for compression
    if compression is None:
        return open(file, mode)
    elif compression == "gz":
        return gzip.open(file, "rt")
    elif compression == "bz2":
        return bz2.open(file, "rt")
    else:
        raise TypeError(f"{file} can't determine file encoding")


def get_sequence_file_type(file: Union[str, Path]) -> str:
    """Get file type of file

    Parameters
    ----------
    file : Path
        A file type

    Returns
    -------
    str
        the sequence file type, either 'abi','fasta' or 'fastq'
    Raises
    ------
    TypeError
        Can't determine filetype
    """
    file = Path(file)
    compression_extension = guess_input_compression(file)

    # The parse will consume the buffer so have to open it every time
    try:
        file_buffer = get_file_buffer(file, compression_extension)
        SeqIO.parse(file_buffer, "fasta").__next__()
        return "fasta"
    except (StopIteration, ValueError):
        pass

    try:
        file_buffer = get_file_buffer(file, compression_extension)
        SeqIO.parse(file_buffer, "fastq").__next__()
        return "fastq"
    except (StopIteration, ValueError):
        pass
    try:
        file_buffer = get_file_buffer(file, compression_extension, "rb")
        SeqIO.parse(file_buffer, "abi").__next__()
        return "abi"
    except (StopIteration, ValueError, OSError):
        raise ValueError(f"can't determine sequence file type of {file}")


def get_sequence_file_iter(
    file: Union[str, Path, TextIO, IO[Any]], file_type: str
) -> Union[AbiIterator, FastaIterator, FastqPhredIterator]:
    """Get a sequence file iterator from SeqIO module"""
    if file_type not in ["fasta", "fastq", "abi", "abi-trim"]:
        raise NotImplementedError(f"{file_type} is not a supported sequence file type")
    return SeqIO.parse(file, file_type)


class SadieInputFile:
    """Sadie Input File will handle input files. Use SadieInputDir for input directories"""

    def __init__(
        self,
        input_path: Union[Path, str],
        input_format: str = "infer",
        compression_format: Union[str, None] = "infer",
    ):
        self.input = input_path
        self.compression_format_inferred = False
        self.file_type_inferred = False

        # infer compression no matter what
        inferred_compression_format = guess_input_compression(self.input)

        # check if directory
        if inferred_compression_format == "directory":
            raise TypeError(f"{self.input} is a directory, use SadieInputDir instead")

        # if we are to infer, we will get a filetype back
        if compression_format == "infer":
            self.compression_format_inferred = True
            self.compression_format = inferred_compression_format
        else:
            # set what the user put in
            if compression_format not in ["gz", "bz2", None]:
                raise ValueError(f"{compression_format} is not a valid compression type, need gz or bz2")

            # only warn if we got it wrong
            if compression_format != inferred_compression_format:
                warnings.warn(
                    f"{self.input} is detected to be {inferred_compression_format} but you specified {compression_format}",
                    UserWarning,
                )
            self.compression_format = compression_format

        # handle the input format next
        self.input_format = input_format

        # if inferred, try to guess type
        if self.input_format == "infer":
            self.input_format_inferred = True
            self.input_format = get_sequence_file_type(self.input)
        else:
            # else its explicit, but check that its implemented
            if self.input_format not in ["fasta", "fastq", "abi", "abi-trim"]:
                raise NotImplementedError(
                    f"{self.input_format} is not a supported sequence file type, only fasta, fastq, abi, abi-trim"
                )

        # get open file
        self.input = Path(self.input)
        self.open_input = get_file_buffer(self.input, self.compression_format)

        # finally get the generator
        self.sequence_generator = get_sequence_file_iter(self.open_input, self.input_format)

    def __iter__(self) -> Iterator[SeqRecord]:
        for seq in self.sequence_generator:
            yield seq


# #         # check if input is compressed - gzip or bzip2
# #         self.input_compressed = self.guess_input_compression(self.input)

# #         # check if input format was specified
# #         self.infer_input = False
# #         if in_format == "infer":
# #             self.infer_input = True

# #         # infer input
# #         if self.infer_input:
# #             self.input_file_type = self.guess_sequence_file_type(self.input)
# #         # input type was set by user
# #         else:
# #             self.input_file_type = in_format

# #         # output format must set before output
# #         self._accepted_output_format = ["infer", "json", "csv", "tsv", "feather", "stdout"]
# #         self._accepted_output_format_suffix = ["json", "csv", "tsv", "feather"]
# #         self._accepted_output_compression = ["gz", "bz2", "infer"]
# #         self._accepted_output_compression_suffix = ["gz", "bz2"]
# #         self.output_format = out_format
# #         self.infered_output_format = None
# #         self.output_compressed = compressed
# #         self.infered_output_compression = None
# #         self.output = output_path

# #     @property
# #     def input(self) -> Path:
# #         return self._input

# #     @input.setter
# #     def input(self, input_path: Union[str, Path]):
# #         if isinstance(input_path, str):
# #             input_path = Path(input_path)
# #         if not isinstance(input_path, Path):
# #             raise TypeError(f"{input_path} needs to be str or path")
# #         if not input_path.exists:
# #             raise FileNotFoundError(f"{input_path} not found")
# #         self._input = input_path

# #     @property
# #     def isdir(self):
# #         return self._isdir

# #     @property
# #     def input_compressed(self):
# #         return self._input_compressed

# #     @input_compressed.setter
# #     def input_compressed(self, compressed_format: str):
# #         if compressed_format not in ["bz2", "gz", "directory", None]:
# #             raise TypeError(f"{compressed_format} needs to be bz2, gz or None")
# #         self._input_compressed = compressed_format

# #     @property
# #     def input_file_type(self) -> str:
# #         return self._input_file_type

# #     @input_file_type.setter
# #     def input_file_type(self, input_file: str):
# #         if input_file not in ["fasta", "abi", "fastq"]:
# #             raise NameError(f"{input_file} needs to be fasta,abi,fastq")
# #         self._input_file_type = input_file

# #     def _get_name_without_suffix(self, path: Union[str, Path]) -> Path:
# #         if isinstance(path, str):
# #             path = Path(path)
# #         if not isinstance(path, Path):
# #             raise TypeError(f"{path} must be str or Path")

# #         # recursive strip suffix
# #         for _ in range(len(path.suffixes)):
# #             path = Path(path.stem)
# #         return path

# #     def _get_parse(self, format, mode="rt"):
# #         return itertools.chain(
# #             *[
# #                 SeqIO.parse(SadieIO.get_file_buffer(x, self.guess_input_compression(x), mode), format)
# #                 for x in self.all_files_in_dir
# #             ]
# #         )

# #     def get_input_records(self) -> Union[FastaIterator, FastqPhredIterator, AbiIterator]:
# #         if not self.isdir:
# #             if self.input_file_type == "fasta":
# #                 return SeqIO.parse(SadieIO.get_file_buffer(self.input, self.input_compressed), "fasta")
# #             if self.input_file_type == "fastq":
# #                 return SeqIO.parse(SadieIO.get_file_buffer(self.input, self.input_compressed), "fastq")
# #             if self.input_file_type == "abi":
# #                 # A single instnace
# #                 return SeqIO.parse(SadieIO.get_file_buffer(self.input, self.input_compressed), "abi")
# #             raise TypeError(f"Requested bad file type {self.input}")
# #         else:

# #             # these are directories which will chain together iterators
# #             if self.input_file_type == "fasta":
# #                 return self._get_parse("fasta")
# #             if self.input_file_type == "fastq":
# #                 return self._get_parse("fastq")
# #             if self.input_file_type == "abi":
# #                 # has to be in rb
# #                 return self._get_parse("abi", "rb")

# #     @staticmethod
# #     def get_file_type_dict(directory_path: Union[Path, str]) -> Dict[str, str]:
# #         """[summary]

# #         Parameters
# #         ----------
# #         directory_path : Union[Path, str]
# #             [description]

# #         Returns
# #         -------
# #         dict
# #             [description]

# #         Raises
# #         ------
# #         TypeError
# #             [description]
# #         """
# #         if isinstance(directory_path, str):
# #             directory_path = Path(directory_path)
# #         if not isinstance(directory_path, Path):
# #             raise TypeError(f"{directory_path} must be of type str or Path not {type(directory_path)}")
# #         if not directory_path.is_dir():
# #             raise TypeError(f"{directory_path} must be directory")
# #         if not directory_path.exists:
# #             return FileNotFoundError(f"{directory_path} does not exist")
# #         glob_files = glob.glob(str(directory_path) + "/*")
# #         glob_files = list(filter(lambda x: Path(x).stem != "Icon\r", list(glob_files)))
# #         return {file: SadieIO.get_file_type(file, SadieIO.guess_input_compression(file)) for file in glob_files}

# #     @staticmethod
# #     def guess_sequence_file_type(input_path: Union[Path, str]) -> str:
# #         """Guess Sequence File type.

# #         Returns
# #         -------
# #         filetype: str
# #             fasta, fastq or abi file format

# #         Raises
# #         ------
# #         NotImplementedError
# #             If a direcotry is passed as input and it contains heterogenous file types, we can not yet parse heterogenous file types
# #         """

# #         if isinstance(input_path, str):
# #             input_path = Path(input_path)
# #         if not isinstance(input_path, Path):
# #             raise TypeError(f"{input_path} is needs to be str of path or Path")

# #         if not input_path.is_dir():
# #             return SadieIO.get_file_type(input_path, SadieIO.guess_input_compression(input_path))

# #         # if dir
# #         else:
# #             _all_files_in_dir = SadieIO.get_file_type_dict(input_path)
# #             if len(set(_all_files_in_dir.values())) != 1:
# #                 raise NotImplementedError(
# #                     pformat(f"all files in {input_path} directory are not of the same type {_all_files_in_dir}")
# #                 )
# #             else:
# #                 return list(_all_files_in_dir.values())[0]

# #     @staticmethod
# #     def __repr__(self):
# #         property_dict = {
# #             "input_path": self.input,
# #             "input_compression": self.input_compressed,
# #             "input_file_type": self.input_file_type,
# #             "input_is_dir": self.isdir,
# #             "output_path": self.output,
# #             "output_file_type": self.output_format,
# #             "output_compressed": self.output_compressed,
# #         }
# #         return pformat(property_dict, indent=4)

# #     def __str__(self):
# #         return self.__repr__()


# # class SadieOutput:
# #     def __init__(self):
# #         pass

# #     @property
# #     def output(self) -> Union[Path, str, None]:
# #         # can be string because stdout
# #         return self._output

# #     @output.setter
# #     def output(self, output_path: Union[Path, str, None]) -> Union[Path, str, None]:
# #         if self.output_format == "stdout" and output_path:
# #             raise SadieIOError(f"output format explicitly specified as stdout with an output path {output_path} set")

# #         # no output was set
# #         if not output_path:
# #             if self.output_format == "infer":
# #                 raise IOInferError("Output format infer was set but no output name was given.")
# #             elif self.output_format == "stdout":
# #                 self._output = "stdout"
# #             else:
# #                 # add appropriate handle
# #                 if self.isdir:
# #                     raise ValueError("If a directory is input, you have to specify an output name")
# #                 output_path = self._get_name_without_suffix(self.input)
# #                 suffix = f".{self.output_format}"
# #                 if self.output_compressed in ["gz", "bz2"]:
# #                     suffix += f".{self.output_compressed}"
# #                 self._output = output_path.with_suffix(suffix)
# #         # output was set
# #         else:
# #             if isinstance(output_path, str):
# #                 output_path = Path(output_path)
# #             if self.output_format == "infer":
# #                 # we are inferring the format
# #                 self.infered_output_format = output_path.suffixes[0].lstrip(".")
# #                 if self.infered_output_format not in self._accepted_output_format_suffix:
# #                     raise ValueError(
# #                         f"{output_path} must have one of these suffixes {self._accepted_output_format_suffix}"
# #                     )
# #                 suffix = f".{self.infered_output_format}"

# #                 self.infered_output_compression = output_path.suffixes[-1].lstrip(".")
# #                 # don't fail an inferred compression but warn
# #                 if self.infered_output_compression not in self._accepted_output_compression_suffix:
# #                     warnings.warn(
# #                         f"{self.infered_output_compression} not in {self._accepted_output_compression_suffix}, not compressing",
# #                         NoExtensionNameWarning,
# #                     )

# #                 if self.output_compressed in ["gz", "bz2"] or self.infered_output_compression in ["gz", "bz2"]:
# #                     suffix += f".{self.output_compressed}"
# #                 self._output = output_path.with_suffix(suffix)

# #             else:
# #                 # we will not get a stdout
# #                 # output is set and output format is set. We can check if they are expected to match
# #                 inferred_format = output_path.suffixes[0].lstrip(".")
# #                 if inferred_format != self.output_format:
# #                     raise ValueError(f"{inferred_format} of {output_path} does not match selected {self.output_format}")

# #                 self.infered_output_format = self.output_format

# #                 # get compression
# #                 if self.output_compressed == "gz":
# #                     output_path = output_path.with_suffix(".gz")

# #                 elif self.output_compressed == "bz2":
# #                     output_path = output_path.with_suffix(".bz2")
# #             self._output = output_path

# #     @property
# #     def output_compressed(self) -> Union[None, str]:
# #         return self._output_compressed

# #     @output_compressed.setter
# #     def output_compressed(self, compressed: str):
# #         # if no output set and infer compressed
# #         if compressed not in self._accepted_output_compression:
# #             raise TypeError(f"{compressed} must be of {self._accepted_output_compression}")
# #         self._output_compressed = compressed

# #     @property
# #     def output_format(self) -> str:
# #         return self._output_format

# #     @output_format.setter
# #     def output_format(self, output_format: str):
# #         if output_format not in self._accepted_output_format:
# #             raise TypeError(f"{output_format} must be in {self._accepted_output_format}")
# #         self._output_format = output_format
