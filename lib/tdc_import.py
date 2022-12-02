import lib.database as db
from tdc.single_pred import ADME
from lib.models import *

# TODO: Add event logging, for example database gets and adds
# TODO: Add pydoc doc blocks for autodoc generation and code completion
class TDCImporter:

    # TODO: Move these to JSON that is loaded from disk
    # TODO: Add parsed publication info to load into docs table
    # TODO: Add activity type, e.g. 'Cell Effective Permeability'
    tdc_dataset_names = {
        'Caco2_Wang': {},
        'PAMPA_NCATS': {},
        'HIA_Hou': {},
        'Pgp_Broccatelli': {},
        'Bioavailability_Ma': {},
        'Lipophilicity_AstraZeneca': {},
        'Solubility_AqSolDB': {},
        'HydrationFreeEnergy_FreeSolv': {},
        'BBB_Martins': {},
        'PPBR_AZ': {},
        'VDss_Lombardo': {},
        'CYP2C19_Veith': {},
        'CYP2D6_Veith': {},
        'CYP3A4_Veith': {},
        'CYP1A2_Veith': {},
        'CYP2C9_Veith': {},
        'CYP2C9_Substrate_CarbonMangels': {},
        'CYP2D6_Substrate_CarbonMangels': {},
        'CYP3A4_Substrate_CarbonMangels': {},
        'Half_Life_Obach': {},
        'Clearance_Hepatocyte_AZ': {}
    }

    tdc_datasets = {}

    def __init__(self):

        self.db_session = db.get_database_session()

    def get_adme(self,name):

        data = ADME(name=name)
        return data

    def build_tdc_local_data(self):

        self.assay_type = self.db_session.query(AssayType).filter(AssayType.assay_desc=='ADME').first()
        self.source = self.db_session.query(Source).filter(Source.src_short_name == 'LITERATURE').first()

        for dataset_name in self.tdc_dataset_names:
            self.tdc_datasets[dataset_name] = self.get_adme(dataset_name)

    def import_to_db(self):

        for dataset_name, dataset in self.tdc_datasets.items():

            assay = self.get_or_add_assay(dataset_name)

            i = 0
            while i < len(dataset.entity1):

                smiles_matches = self.db_session.query(CompoundStructure).filter(CompoundStructure.canonical_smiles==dataset.entity1[i]).all()
                if len(smiles_matches) == 1:
                    compound_structure = smiles_matches[0]
                    if compound_structure.molecule.compound is not None:
                        self.get_or_add_activity(assay,compound_structure.molecule.compound,dataset.y[i])
                    else:
                        # TODO: Implement what to do when there is No ChEMBL record - e.g. add a record!
                        pass
                elif len(smiles_matches) > 1:
                    name_matches = self.db_session.query(MoleculeSynonym).join(MoleculeDictionary,CompoundStructure).filter(MoleculeSynonym.synonyms==str(dataset.entity1_idx[i]),
                                                                                                             CompoundStructure.canonical_smiles==dataset.entity1[i]).all()
                    if len(name_matches) == 1:
                        compound_structure = name_matches[0]
                        self.get_or_add_activity(assay, compound_structure.molecule.compound, dataset.y[i])
                else:
                    # TODO: Implement what to do when there is No ChEMBL record - e.g. add a record!
                    pass
                i = i + 1

    def get_or_add_assay(self,dataset_name):

        # TODO: Add publications to a Docs object and store this with Assay

        short_name = self.shorten_dataset_name(dataset_name)
        assay = self.db_session.query(Assay).filter(Assay.aidx==short_name).first()

        if not assay:
            assay_id = self.db_session.query(func.max(Assay.assay_id)).first()[0] + 1

            # TODO: Auto-generate next ChEMBL ID using string split, numeric cast, increment, string cast, and then join
            chembl_id = 'CHEMBLDM' + short_name
            chembl_id_lookup = ChemblIdLookup(chembl_id=chembl_id,
                                              entity_type='ASSAY',
                                              entity_id=assay_id,
                                              status="ACTIVE")
            self.db_session.add(chembl_id_lookup)
            self.db_session.flush()

            assay = Assay(assay_id=self.db_session.query(func.max(Assay.assay_id)).first()[0]+1,
                          aidx=short_name,
                          type=self.assay_type,
                          doc_id=1, # TODO: Add docs.id here
                          src_id=self.source.src_id,
                          chembl_id=chembl_id)
            self.db_session.add(assay)
            self.db_session.flush()

        return assay

    def shorten_dataset_name(self,dataset_name):

        return dataset_name.replace("_","").upper()[0:11]

    def get_or_add_activity(self,assay,compound_record,value):

        activity = self.db_session.query(Activity).filter(Activity.assay_id==assay.assay_id,
                                                          Activity.molregno==compound_record.molregno).first()
        if not activity:
            activity = Activity(activity_id=self.db_session.query(func.max(Activity.activity_id)).first()[0]+1,
                                assay_id=assay.assay_id,
                                molregno=compound_record.molregno,
                                record_id=compound_record.record_id,
                                type='', # TODO: Add the activity type here -> e.g. 'Cell Effective Permeability'
                                standard_value=value)
            self.db_session.add(activity)
            self.db_session.flush()


if __name__ == "__main__":
    tdc_importer = TDCImporter()
    tdc_importer.build_tdc_local_data()
    tdc_importer.import_to_db()