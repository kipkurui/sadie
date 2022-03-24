# All of these ignores are because pylance can't figure out fixtures
# pyright: reportUnknownMemberType=false
# pyright: reportUnknownParameterType=false
# pyright: reportUnknownVariableType=false
# pyright: reportMissingParameterType=false

# from gzip import GzipFile
# from pathlib import Path

from io import TextIOWrapper
from pathlib import Path

import pytest

# third part
from Bio.SeqIO.AbiIO import AbiIterator
from Bio.SeqIO.FastaIO import FastaIterator
from Bio.SeqIO.QualityIO import FastqPhredIterator
from Bio.SeqRecord import SeqRecord

# package
from sadie.utility.io import get_file_buffer, get_sequence_file_iter, get_sequence_file_type, guess_input_compression
from sadie.utility.io import SadieInputFile


def test_io_methods(fixture_setup):
    """Text methods in IO that are used mostly in objects"""

    # get fastq files
    multi_fastq: Path = fixture_setup.get_multiple_fastq()
    multi_fastq_gz: Path = fixture_setup.get_multiple_fastq_compressed("gz")
    multi_fastq_bz: Path = fixture_setup.get_multiple_fastq_compressed("bz2")
    fastq_dir_path: Path = fixture_setup.fastq_inputs  # this is a directory
    # this is not implemented
    multi_fastq_xz: Path = fixture_setup.get_multiple_fastq_compressed("xz")

    # Step 1 is to explicitly get buffer
    # "rt" mode
    multi_fastq_fb = get_file_buffer(multi_fastq)
    multi_fastq_gz_fb = get_file_buffer(multi_fastq_gz, "gz")
    multi_fastq_bz_fb = get_file_buffer(multi_fastq_bz, "bz2")
    assert all(isinstance(x, TextIOWrapper) for x in [multi_fastq_fb, multi_fastq_gz_fb, multi_fastq_bz_fb])

    with pytest.raises(TypeError):
        get_file_buffer(multi_fastq_bz, "zip")

    # Step 2 is to guess compression type
    assert not guess_input_compression(multi_fastq)
    assert guess_input_compression(multi_fastq_gz) == "gz"
    assert guess_input_compression(multi_fastq_bz) == "bz2"
    assert guess_input_compression(fastq_dir_path) == "directory"
    with pytest.raises(NotImplementedError):
        guess_input_compression(multi_fastq_xz)

    # need to grab fasta files here
    fasta_file = fixture_setup.get_pg9_heavy_fasta()
    fasta_file_gz = fixture_setup.get_pg9_heavy_fasta_compressed("gz")
    fasta_file_bz2 = fixture_setup.get_pg9_heavy_fasta_compressed("bz2")
    assert all(get_sequence_file_type(x) == "fasta" for x in [fasta_file, fasta_file_gz, fasta_file_bz2])
    assert all(get_sequence_file_type(x) == "fastq" for x in [multi_fastq, multi_fastq_bz, multi_fastq_gz])
    assert all(get_sequence_file_type(x) == "abi" for x in fixture_setup.get_abi_files())

    with pytest.raises(ValueError):
        # don't accept phylip format
        get_sequence_file_type(fixture_setup.get_phy_file())

    # get explicit iterators
    assert isinstance(get_sequence_file_iter(fixture_setup.get_abi_files()[0], "abi"), AbiIterator)
    assert isinstance(get_sequence_file_iter(fixture_setup.get_abi_files()[0], "abi-trim"), AbiIterator)
    assert isinstance(get_sequence_file_iter(fasta_file, "fasta"), FastaIterator)
    assert isinstance(get_sequence_file_iter(multi_fastq, "fastq"), FastqPhredIterator)

    with pytest.raises(NotImplementedError):
        get_sequence_file_iter(fixture_setup.get_phy_file(), "phy")


def test_sadie_input(fixture_setup):
    multi_fastq: Path = fixture_setup.get_multiple_fastq()
    multi_fastq_gz: Path = fixture_setup.get_multiple_fastq_compressed("gz")
    multi_fastq_bz: Path = fixture_setup.get_multiple_fastq_compressed("bz2")
    fastq_dir_path: Path = fixture_setup.fastq_inputs  # this is a directory

    # infer both compression and filetype
    SadieInputFile(multi_fastq)
    SadieInputFile(multi_fastq_gz)
    SadieInputFile(multi_fastq_bz)
    SadieInputFile(multi_fastq, "fastq", None)
    SadieInputFile(multi_fastq_gz, "fastq", "gz")
    SadieInputFile(multi_fastq_bz, "fastq", "bz2")
    # test __str__
    print(SadieInputFile(multi_fastq_bz, "fastq", "bz2"))
    print(SadieInputFile(multi_fastq_bz, "fastq", "bz2").__repr__())

    gzip_fastq = SadieInputFile(multi_fastq_gz, "fastq", "gz")
    bzip_fastq = SadieInputFile(multi_fastq_bz, "fastq", "bz2")

    # test equivalence of get_seq_records across compression
    assert [i.seq for i in gzip_fastq.get_seq_records()] == [i.seq for i in bzip_fastq.get_seq_records()]
    assert [i.id for i in gzip_fastq.get_seq_records()] == [i.id for i in bzip_fastq.get_seq_records()]

    # test __iter__ directly
    assert [i.seq for i in gzip_fastq] == [i.seq for i in bzip_fastq]

    with pytest.raises(TypeError):
        # no paths in input file
        SadieInputFile(fastq_dir_path)
    with pytest.raises(ValueError):
        # bad compression
        SadieInputFile(multi_fastq_bz, "fastq", "bz")

    with pytest.warns(UserWarning):
        # compression does not match declared
        SadieInputFile(multi_fastq_gz, "fastq", "bz2")
    phy_file = fixture_setup.get_phy_file()
    with pytest.raises(NotImplementedError):
        SadieInputFile(phy_file, "phy")

    for seq in SadieInputFile(multi_fastq_gz):
        assert isinstance(seq, SeqRecord)


# def test_io_single_files(fixture_setup):
#     # infer filetypes of non compressed
#     input_file = fixture_setup.get_pg9_heavy_multiple_fasta()
#     io = SadieIO(input_file, out_format="csv")
#     assert io.input == Path(input_file)
#     assert io.infer_input
#     assert not io.input_compressed
#     assert io.input_file_type == "fasta"
#     assert not io.isdir

#     input_file = fixture_setup.get_multiple_fastq()
#     io = SadieIO(input_file, out_format="csv")
#     assert io.input == Path(input_file)
#     assert io.infer_input
#     assert not io.input_compressed
#     assert io.input_file_type == "fastq"
#     assert not io.isdir

#     input_file = fixture_setup.get_abi_files()[0]
#     io = SadieIO(input_file, out_format="csv")
#     assert io.input == Path(input_file)
#     assert io.infer_input
#     assert not io.input_compressed
#     assert io.input_file_type == "abi"
#     assert not io.isdir

#     # infer filetypes of non compressed
#     input_file = fixture_setup.get_pg9_heavy_fasta_compressed("gz")
#     io = SadieIO(input_file, out_format="csv")
#     assert io.input == Path(input_file)
#     assert io.infer_input
#     assert io.input_compressed == "gz"
#     assert io.input_file_type == "fasta"
#     assert not io.isdir

#     input_file = fixture_setup.get_multiple_fastq_compressed("gz")
#     io = SadieIO(input_file, out_format="csv")
#     assert io.input == Path(input_file)
#     assert io.infer_input
#     assert io.input_compressed == "gz"
#     assert io.input_file_type == "fastq"
#     assert not io.isdir

#     input_file = fixture_setup.get_compressed_abi_files("gz")[0]
#     io = SadieIO(input_file, out_format="csv")
#     assert io.input == Path(input_file)
#     assert io.infer_input
#     assert io.input_compressed == "gz"
#     assert io.input_file_type == "abi"
#     assert not io.isdir


# def test_io_folders(fixture_setup):
#     # infer filetypes of non compressed
#     input_file = fixture_setup.fasta_inputs
#     io = SadieIO(input_file, output_path="test.csv", out_format="csv")
#     assert io.input == Path(input_file)
#     assert io.infer_input
#     assert io.input_compressed == "directory"
#     assert io.input_file_type == "fasta"
#     assert io.isdir
#     assert all([isinstance(i, SeqRecord) for i in io.get_input_records()])

#     input_file = fixture_setup.fastq_inputs
#     io = SadieIO(input_file, output_path="test.csv", out_format="csv")
#     assert io.input == Path(input_file)
#     assert io.infer_input
#     assert io.input_compressed == "directory"
#     assert io.input_file_type == "fastq"
#     assert io.isdir
#     assert all([isinstance(i, SeqRecord) for i in io.get_input_records()])

#     input_file = fixture_setup.abi_inputs
#     io = SadieIO(input_file, output_path="test.csv", out_format="csv")
#     assert io.input == Path(input_file)
#     assert io.infer_input
#     assert io.input_compressed == "directory"
#     assert io.input_file_type == "abi"
#     assert io.isdir
#     assert all([isinstance(i, SeqRecord) for i in io.get_input_records()])


# def test_output(tmpdir, fixture_setup):
#     # uses tmpdir pytest fixture
#     input_file = sorted(fixture_setup.get_compressed_abi_files("gz"))[0]
#     # case 1 no output path is set, but infer is set by default
#     with pytest.raises(IOInferError):
#         io_output = SadieIO(input_file)

#     with pytest.raises(ValueError):
#         io_output = SadieIO(input_file, output_path="myfile.gsv")

#     with pytest.warns(UserWarning):
#         io_output = SadieIO(input_file, output_path="myfile.tsv.zip")

#     # case 2 no output path is set, but infer is set by default
#     for suffix in ["csv", "tsv", "feather", "json"]:
#         io_output = SadieIO(input_file, out_format=f"{suffix}")
#         assert io_output.output == Path(f"file1.{suffix}")
#         assert io_output.output_compressed == "infer"
#         assert io_output.output_format == suffix
#         assert io_output.infered_output_format is None
#         assert io_output.infered_output_compression is None

#     # case 3 no output path is set, but infer is set by default and compression
#     for suffix in ["csv", "tsv", "feather", "json"]:
#         for compression in ["gz", "bz2"]:
#             io_output = SadieIO(input_file, out_format=f"{suffix}", compressed=f"{compression}")
#             assert io_output.output == Path(f"file1.{suffix}.{compression}")
#             assert io_output.output_compressed == compression
#             assert io_output.infered_output_compression is None
#             assert io_output.output_format == suffix
#             assert io_output.infered_output_format is None

#     # case 4 output and input are set with infer type and compression
#     for suffix in ["csv", "tsv", "feather", "json"]:
#         for compression in ["gz", "bz2"]:
#             output_file_dummy = Path(f"somedummy_file.{suffix}.{compression}")
#             io_output = SadieIO(input_path=input_file, output_path=output_file_dummy)
#             assert io_output.output == output_file_dummy
#             assert io_output.output_compressed == "infer"
#             assert io_output.infered_output_compression == compression
#             assert io_output.output_format == "infer"
#             assert io_output.infered_output_format == suffix
