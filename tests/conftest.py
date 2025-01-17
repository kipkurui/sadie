"""Pytest conftest with all the fixture classes"""
import bz2
import glob
import gzip
import json
import lzma
import shutil
from pathlib import Path
from typing import Dict, List, Tuple

import pandas as pd
import pytest
from Bio import SeqIO

from sadie.airr import Airr
from sadie.airr.airrtable import AirrTable


def _get_file_compressed(tmp_path: Path, uncompressed_file: Path, compression: str) -> Path:
    """helper funcitons for compressing files"""
    tmp_file_name = uncompressed_file.name + f".{compression}"
    return_path = tmp_path / tmp_file_name
    with open(uncompressed_file, "rb") as f_in:
        if compression == "bz2":
            fn = bz2.open(return_path, "wb")
        elif compression == "gz":
            fn = gzip.open(return_path, "wb")
        elif compression == "xz":
            fn = lzma.open(return_path, "wb")
        with fn as f_out:
            shutil.copyfileobj(f_in, f_out)
    return return_path


def _get_uncompressed_file(tmp_path: Path, compressed_file: Path, compression: str) -> Path:
    """helper funcitons for uncompressing files"""
    tmp_file_name = compressed_file.stem
    return_path = tmp_path / tmp_file_name
    if compression == "bz2":
        fn = bz2.open(compressed_file, "rb")
    elif compression == "gz":
        fn = gzip.open(compressed_file, "rb")
    with fn as f_in:
        with open(return_path, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)
    return return_path


class AirrSequences:
    """
    Organization of sequence fixtures that are used by Airr and Numbering primarily.
    Will be sub-classed by SadieFixtures
    """

    def __init__(self, tmp_path: Path, base_datadir: Path):
        self.base_datadir = base_datadir
        self.tmp_path = tmp_path
        self.fasta_inputs = self.base_datadir / "fasta_inputs/"
        self.fastq_inputs = self.base_datadir / "fastq_inputs/"
        self.airr_table_inputs = self.base_datadir / "airr_tables/"
        self.abi_inputs = self.base_datadir / "ab1_files/"
        self.single_seqs_json = json.load(open(self.base_datadir / "single-sequences.json"))

    def get_pg9_heavy_fasta(self) -> Path:
        """get the file path for PG9 heavy chain fasta"""
        return self.fasta_inputs / "PG9_H.fasta"

    def get_pg9_heavy_sequence(self) -> SeqIO.SeqRecord:
        """get the sequence recored for the PG9 heavy chain"""
        return SeqIO.read(self.get_pg9_heavy_fasta(), "fasta")

    def get_pg9_light_fasta(self) -> Path:
        """get the file path for PG9 light chain fasta"""
        return self.fasta_inputs / "PG9_L.fasta"

    def get_vrc01_light_fasta(self) -> Path:
        """get a file path for the vrc01 light fasta file"""
        return self.fasta_inputs / "vrc01_L.fasta"

    def get_vrc01_heavy_fasta(self) -> Path:
        """get a file path for the vrc01 light fasta file"""
        return self.fasta_inputs / "vrc01_H.fasta"

    def get_pg9_light_sequence(self) -> SeqIO.SeqRecord:
        """get the sequence recored for the PG9 light chain"""
        return SeqIO.read(self.get_pg9_light_fasta(), "fasta")

    def get_vrc01_light_sequecne(self) -> SeqIO.SeqRecord:
        return SeqIO.read(self.get_vrc01_light_fasta(), "fasta")

    def get_vrc01_heavy_sequence(self) -> SeqIO.SeqRecord:
        return SeqIO.read(self.get_vrc01_heavy_fasta(), "fasta")

    def get_pg9_heavy_multiple_fasta(self) -> Path:
        """get multiple fasta file path for multiple PG9 heavy chains"""
        return self.fasta_inputs / "PG9_H_multiple.fasta"

    def get_pg9_heavy_multiple_fasta_seqs(self) -> List[SeqIO.SeqRecord]:
        """get multiple SeqRecords for multiple PG9 heavy chains"""
        return list(SeqIO.parse(self.get_pg9_heavy_multiple_fasta(), "fasta"))

    def get_pg9_light_multiple_fasta(self) -> Path:
        """get multiple fasta file path for multiple PG9 light chains"""
        return self.fasta_inputs / "PG9_L_multiple.fasta"

    def get_pg9_light_multiple_fasta_seqs(self) -> List[SeqIO.SeqRecord]:
        """get multiple SeqRecords for multiple PG9 light chains"""
        return list(SeqIO.parse(self.get_pg9_light_multiple_fasta(), "fasta"))

    def get_pg9_heavy_fasta_compressed(self, compression: str) -> Path:
        """Get a pg9 heavy fasta file compressed with a given compression

        Parameters
        ----------
        compression : str
            the compression to use., eg. "gz" or "bz2"

        Returns
        -------
        Path
            file path for the compressed file
        """
        return _get_file_compressed(self.tmp_path, self.get_pg9_heavy_fasta(), compression)

    def get_pg9_light_fasta_compressed(self, compression) -> Path:
        """Get a pg9 light fasta file compressed with a given compression

        Parameters
        ----------
        compression : str
            the compression to use., eg. "gz" or "bz2"

        Returns
        -------
        Path
            file path for the compressed file
        """
        return _get_file_compressed(self.tmp_path, self.get_pg9_light_fasta(), compression)

    def get_scfv_fasta(self) -> Path:
        """get a fasta file path for the scfv file that contains duplicated scfv files"""
        return self.fasta_inputs / "scfv.fasta"

    def get_scfv_sequences(self) -> SeqIO.SeqRecord:
        """get the SeqRecords for the scfv fasta file that contains duplicated scfv files"""
        return SeqIO.parse(self.get_scfv_fasta(), "fasta")

    def get_long_scfv_fastq(self) -> List[SeqIO.SeqRecord]:
        """get a fastq file path for the scfv file records that contains many unique scfv files"""
        return list(
            SeqIO.parse(_get_uncompressed_file(self.tmp_path, self.fastq_inputs / "long_scfv.fastq.gz", "gz"), "fastq")
        )

    def get_multiple_fastq(self) -> Path:
        """get back a fastq file path that is uncompressed"""
        return self.fastq_inputs / "multiple.fastq"

    def get_multiple_fastq_compressed(self, compression: str) -> Path:
        return _get_file_compressed(self.tmp_path, self.get_multiple_fastq(), compression)

    def get_catnap_heavy_nt(self) -> Path:
        """get a file path for the catnap heavy nt file"""
        return self.fasta_inputs / "catnap_nt_heavy.fasta"

    def get_catnap_light_nt(self) -> Path:
        """get a file path for the catnap light nt file"""
        return self.fasta_inputs / "catnap_nt_light.fasta"

    def get_catnap_heavy_aa(self) -> Path:
        """get a file path for the catnap heavy aa file"""
        return self.fasta_inputs / "catnap_aa_heavy_sample.fasta"

    def get_catnap_light_aa(self) -> Path:
        """get a file path for the catnap light aa file"""
        return self.fasta_inputs / "catnap_aa_light_sample.fasta"

    def get_oas_fasta(self) -> Path:
        """Get a random 1000 subsample fasta file path of the OAS data set."""
        return self.fasta_inputs / "OAS_subsample_1000.fasta"

    def get_dog_aa_seqs(self) -> Path:
        "A fasta file path containing random canine AA sequences"
        return self.fasta_inputs / "random_dog_contigs_aa.fasta.gz"

    def get_fasta_files(self) -> List[Path]:
        """Get a list of different fasta files for CLI testing. scfv, pg9_h, pg9_h_multi, pg9_l, pg9_l_multi"""
        return [
            self.get_scfv_fasta(),
            self.get_pg9_heavy_multiple_fasta(),
            self.get_pg9_light_fasta(),
            self.get_pg9_light_multiple_fasta(),
        ]

    def get_adaptable_pentalty_test_seq(self) -> str:
        """get a signle sequence for the testing sequence for adaptable pentalties"""
        return self.single_seqs_json["adaptible_pentalty_test_seq"]

    def get_adaptable_pentalty_test_seq_scfv(self) -> str:
        """get a single scfv sequence for the testing sequence for adaptable pentalties"""
        return self.single_seqs_json["adaptible_pentalty_test_seq_scfv"]

    def get_OAS_correctable_pentalty_file(self) -> Path:
        "Get a file containing correctable sequences from OAS"
        return self.fasta_inputs / "OAS_correctable_liable.fasta"

    def get_OAS_liable_file(self) -> Path:
        "Get liable sequences from OAS that when adapt is turned off" ""
        return self.fasta_inputs / "OAS_liable.fasta"

    def get_monkey_edge_seq(self) -> str:
        """get a single sequence for the testing sequence for testing the weird macaque edge case"""
        return self.single_seqs_json["monkey_edge_case"]

    def get_pe_consensus_seq(self) -> str:
        """Get the consensus sequence to see if we are getting the best sequecnes from two paired end files"""

        return self.single_seqs_json["consensus_seq"]

    def get_abi_files(self) -> List[Path]:
        """Get a list of different abi files for io testing"""
        return list(self.abi_inputs.glob("*ab1"))

    def get_compressed_abi_files(self, compression: str) -> List[Path]:
        """Get a list of different compressed abi files for io testing"""
        return [_get_file_compressed(self.tmp_path, abi_file, compression) for abi_file in self.get_abi_files()]

    def get_abi_pe_files(self) -> List[Path]:
        """Get a list with two paired end abi files that can be used to make a consensus

        Returns:
            List[Path] -- [fwd_pe path, rev_pe path]
        """
        fwd = self.abi_inputs / "fwd_read.ab1"
        rev = self.abi_inputs / "rev_read.ab1"
        return [fwd, rev]

    def get_fasta_with_constant(self) -> Path:
        """Get a fasta file with a constant sequence"""
        return self.fasta_inputs / "HD_w_constant.fasta"


class AirrTables:
    """A class for organization of airrtable related fixtures"""

    def __init__(self, tmp_path: Path, base_datadir: Path):
        self.base_datadir = base_datadir
        self.tmp_path = tmp_path
        self.airr_table_inputs = self.base_datadir / "airr_tables/"

    def get_dog_airrtable(self) -> Path:
        """get a file path for the dog airr table .tsv.gz"""
        return self.airr_table_inputs / "dog_igh.tsv.gz"

    def get_dog_airrtable_with_missing_sequences(self) -> pd.DataFrame:
        """get a dataframe with missing seqeunces as nan that will throw errror"""
        dog_df = AirrTable.read_airr(self.get_dog_airrtable())
        dog_1 = dog_df.copy()
        dog_2 = dog_df.copy()
        dog_2.drop(["sequence", "sequence_id"], axis=1, inplace=True)
        dog_2 = dog_2.reset_index().rename({"index": "sequence_id"}, axis=1)
        double_dog = pd.concat([dog_1, dog_2])
        return double_dog

    def get_linked_airrtable(self) -> Path:
        """get file path to a linked airrtable for spliting and reassembling"""
        return self.airr_table_inputs / "linked_airrtable_scfv.csv.gz"

    def get_json_as_dataframe(self) -> Path:
        """get a file path for the airr table that is in json.gz"""
        return self.airr_table_inputs / "airrtable.json.gz"

    def get_uncompressed_json_as_dataframe(self) -> Path:
        """get a file path for the airr table that is in json."""
        return _get_uncompressed_file(self.tmp_path, self.get_json_as_dataframe(), "gz")

    def get_busted_airrtable(self) -> Path:
        """get a file path for the airr table that is in tsv. contains missing airrtables"""
        return self.airr_table_inputs / "busted.tsv.gz"

    def get_catnap_heavy_airrtable(self) -> Path:
        """get a file path for the CATNAP heavy airr table results. should match fasta input"""
        return self.airr_table_inputs / "catnap_heavy_airrtable.feather"

    def get_catnap_light_airrtable(self) -> Path:
        """get a file path for the CATNAP light airr table results. Should match fasta input"""
        return self.airr_table_inputs / "catnap_light_airrtable.feather"

    def get_imgt_airrtable(self) -> Path:
        """get a file path for the OAS sequences ran through IMGT Hi-V"""
        return self.airr_table_inputs / "imgt_v_quest_airr.tsv.gz"

    def get_catnap_heavy_with_mutational_analysis(self) -> Path:
        """get the heavy catnap airrtable that has precomputed mutational analysis"""
        return self.airr_table_inputs / "heavy_airrtable_with_mutational.feather"

    def get_catnap_light_with_mutational_analysis(self) -> Path:
        """get the light catnap airrtable that has precomputed mutational analysis"""
        return self.airr_table_inputs / "light_airrtable_with_mutational.feather"

    def get_catnap_joined_with_mutational_analysis(self) -> Path:
        """get the joined catnap airrtable that has precomputed mutational analysis"""
        return self.airr_table_inputs / "joined_airrtable_with_mutational.feather"

    def get_bum_igl_assignment(self) -> Path:
        """Get an airrtable feather path that is failing igl assignment"""
        return self.airr_table_inputs / "bum_igl_assignment_macaque.feather"

    def get_bum_igl_solution(self) -> Path:
        """Get an airrtable feather with teh solutions"""
        return self.airr_table_inputs / "igl_out.feather"

    def get_bum_link_igl_assignment(self) -> Path:
        """Get an airrtable feather path that is failing linked igl assignment"""
        return self.airr_table_inputs / "bum_link_input.feather"

    def get_bum_link_igl_solution(self) -> Path:
        """Get an airrtable feather with the linked solutions"""
        return self.airr_table_inputs / "bum_link_solution.feather"


class ReferenceFixtures:
    """A class for organization of reference related fixtures"""

    def __init__(self, tmp_path: Path, base_datadir: Path):
        self.base_datadir = base_datadir
        self.tmp_path = tmp_path
        self.reference_data = self.base_datadir / "reference/"

    def get_reference_dataset_csv(self) -> Path:
        """
        get a file path for the reference dataset csv
        this is a csv that contains all the reference data in a nice csv dataframe
        """
        return self.reference_data / "reference_object_dataframe.csv.gz"

    def get_aux_files(self) -> List[str]:
        """get a glob of aux files that come directly from imgt to make sure generated aux matches"""
        path = self.reference_data / "igblast_aux"
        return glob.glob(str(path / "**.aux"))

    def get_internal_files(self) -> List[str]:
        """get a glob of internal .imgt files to make sure generated internal matches"""
        path = self.reference_data / "igblast_internal"
        return glob.glob(str(path / "**.imgt"))

    def get_known_blast_dir_structure(self) -> List[str]:
        """get a list of names that should be in blast dir ref generation"""
        path = self.reference_data / "blast_dir.json"
        return sorted(json.load(open(path)))

    def get_known_internal_dir_structure(self) -> List[str]:
        """get a list of names that should be in internal dir ref generation"""
        path = self.reference_data / "internal.json"
        return sorted(json.load(open(path)))

    def get_known_aux_dir_structure(self) -> List[str]:
        """get a list of names that should be in aux dir ref generation"""
        path = self.reference_data / "aux.json"
        return sorted(json.load(open(path)))

    def get_known_nhd_dir_structure(self) -> List[str]:
        """get a list of names that should be in nhd (blast format files) dir ref generation"""
        path = self.reference_data / "nhd.json"
        return sorted(json.load(open(path)))

    def get_aux_exceptions(self) -> Dict[Tuple[str, str], str]:
        """get a dict of aux files that are known exceptions in the IgBlast aux dir"""
        return {
            ("mouse", "IGLJ4*01"): "igblast has wrong number of c-term remaining",
            ("rabbit", "IGHJ3*02"): "igblast has wrong reading frame",
        }

    def get_internal_db_excetions(self) -> List[List[str]]:
        """get a list of known exceptions from IMGT"""
        return [
            ["rat", "IGHV1S62*01"],
            ["rat", "IGHV2S1*01"],
            ["rat", "IGHV2S12*01"],
            ["rat", "IGHV2S13*01"],
            ["rat", "IGHV2S18*01"],
            ["rat", "IGHV2S30*01"],
            ["rat", "IGHV2S35*01"],
            ["rat", "IGHV2S54*01"],
            ["rat", "IGHV2S61*01"],
            ["rat", "IGHV2S63*01"],
            ["rat", "IGHV2S75*01"],
            ["rat", "IGHV2S78*01"],
            ["rat", "IGHV2S8*01"],
            ["rat", "IGHV5S10*01"],
            ["rat", "IGHV5S11*01"],
            ["rat", "IGHV5S13*01"],
            ["rat", "IGHV5S14*01"],
            ["rat", "IGHV5S23*01"],
            ["rat", "IGHV5S47*01"],
            ["rat", "IGHV5S54*01"],
            ["rat", "IGHV5S8*01"],
            ["rat", "IGHV8S18*01"],
            ["rat", "IGHV9S3*01"],
            ["human", "IGHV2-70*02"],
            ["human", "IGHV2-70*03"],
            ["human", "IGHV2-70*06"],
            ["human", "IGHV2-70*07"],
            ["human", "IGHV2-70*08"],
        ]

    def get_duplicated_yaml(self) -> Path:
        """get a file path for a yaml file that has duplicated entries"""
        return self.reference_data / Path("duplicated_in_source.yml")

    def get_duplicated_diff_source_yaml(self) -> Path:
        """get a file path for a yaml file that has duplicated entries"""
        return self.reference_data / Path("duplicated_inter_source.yml")

    def get_shortened_yaml(self) -> Path:
        """get a file path for a yaml file that is pretty short"""
        return self.reference_data / Path("short_reference.yml")


class NumberingFixtures:
    def __init__(self, tmp_path: Path, base_datadir: Path):
        self.base_datadir = base_datadir
        self.tmp_path = tmp_path
        self.numbering_data = self.base_datadir / "anarci/curated_alignments"
        self.alignment_data = self.base_datadir / "anarci/alignments"
        self.hmm_data = self.base_datadir.parent.parent.parent / "src/sadie/renumbering/data/hmms"


class SadieFixture(AirrSequences, AirrTables, ReferenceFixtures, NumberingFixtures):
    def __init__(self, tmp_path_factory):
        tmp_path = tmp_path_factory.mktemp("sadie_fixture")
        base_datadir = Path("tests/data/fixtures/")

        # three subclasses need to be initialized this way
        AirrSequences.__init__(self, tmp_path, base_datadir)
        AirrTables.__init__(self, tmp_path, base_datadir)
        ReferenceFixtures.__init__(self, tmp_path, base_datadir)
        NumberingFixtures.__init__(self, tmp_path, base_datadir)

        # then rest of attributes
        self.tmp_path = tmp_path
        self.base_datadir = base_datadir

    def get_card(self) -> Path:
        """get a png file path that has a card image. This is a nonsense file path to test unexpected files"""
        return self.base_datadir / "card.png"

    def get_phy_file(self) -> Path:
        """get a phylip sequence file which i guess should be unsupported by utilities IO"""
        return self.base_datadir / "usupported.phy"


@pytest.fixture(scope="session", autouse=True)
def fixture_setup(tmp_path_factory: pytest.TempPathFactory):
    return SadieFixture(tmp_path_factory)


@pytest.fixture(scope="session", autouse=False)
def heavy_catnap_airrtable(fixture_setup: SadieFixture) -> AirrTable:
    """A permanant fixture of the catnap heavy airr table run through adaptable airrtable"""
    airr_api = Airr("human", adaptable=True)
    airrtable_heavy = airr_api.run_fasta(fixture_setup.get_catnap_heavy_nt())
    airrtable_heavy["cellid"] = airrtable_heavy["sequence_id"].str.split("_").str.get(0)
    return airrtable_heavy


@pytest.fixture(scope="session", autouse=False)
def light_catnap_airrtable(fixture_setup: SadieFixture) -> AirrTable:
    """A permanant fixture of the catnap light airr table run through adaptable airrtable"""
    airr_api = Airr("human", adaptable=True)
    airrtable_light = airr_api.run_fasta(fixture_setup.get_catnap_light_nt())
    airrtable_light["cellid"] = airrtable_light["sequence_id"].str.split("_").str.get(0)
    return airrtable_light
