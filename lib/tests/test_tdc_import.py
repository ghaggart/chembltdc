#import lib.database as db
from lib.tdc_import import TDCImporter
import pytest

class TestTDCImport:
    """TestDatabase class. Tests the Database connections
    """

    def test_connect_tdc(self):

        tdc_importer = TDCImporter()
        assert tdc_importer.get_adme('Caco2_Wang') is not None
        assert tdc_importer.get_adme('PAMPA_NCATS') is not None
        assert tdc_importer.get_adme('HIA_Hou') is not None
        assert tdc_importer.get_adme('Pgp_Broccatelli') is not None
        assert tdc_importer.get_adme('Bioavailability_Ma') is not None
        assert tdc_importer.get_adme('Lipophilicity_AstraZeneca') is not None
        assert tdc_importer.get_adme('Solubility_AqSolDB') is not None
        assert tdc_importer.get_adme('HydrationFreeEnergy_FreeSolv') is not None
        assert tdc_importer.get_adme('BBB_Martins') is not None
        assert tdc_importer.get_adme('PPBR_AZ') is not None
        assert tdc_importer.get_adme('VDss_Lombardo') is not None
        assert tdc_importer.get_adme('CYP2C19_Veith') is not None
        assert tdc_importer.get_adme('CYP2D6_Veith') is not None
        assert tdc_importer.get_adme('CYP3A4_Veith') is not None
        assert tdc_importer.get_adme('CYP1A2_Veith') is not None
        assert tdc_importer.get_adme('CYP2C9_Veith') is not None
        assert tdc_importer.get_adme('CYP2C9_Substrate_CarbonMangels') is not None
        assert tdc_importer.get_adme('CYP2D6_Substrate_CarbonMangels') is not None
        assert tdc_importer.get_adme('CYP3A4_Substrate_CarbonMangels') is not None
        assert tdc_importer.get_adme('Half_Life_Obach') is not None
        assert tdc_importer.get_adme('Clearance_Hepatocyte_AZ') is not None

    def test_build_local_dataset(self):

        tdc_importer = TDCImporter()
        tdc_importer.build_tdc_local_data()
        assert len(tdc_importer.tdc_datasets.keys()) == 21

    def test_import_to_db(self):
        tdc_importer = TDCImporter()
        tdc_importer.build_tdc_local_data()
        tdc_importer.import_to_db()








