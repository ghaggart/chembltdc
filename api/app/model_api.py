import os,sys

from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.security.decorators import permission_name, has_access_api
from flask_appbuilder.api import ModelRestApi
from flask_appbuilder.filters import *
from . import appbuilder
import json

if os.environ['CHEMBLTDCLIB'] not in sys.path:
    sys.path.append(os.environ['CHEMBLTDCLIB'])

from lib.models import *

# TODO: Add the remaining models!

class Assay(ModelRestApi):
    resource_name = 'assays'
    datamodel = SQLAInterface(Assay)
    class_permission_name = "ModelAPI"

class Activity(ModelRestApi):
    resource_name = 'activities'
    datamodel = SQLAInterface(Activity)
    class_permission_name = "ModelAPI"

class CompoundStructure(ModelRestApi):
    resource_name = 'compound_structure'
    datamodel = SQLAInterface(CompoundStructure)
    class_permission_name = "ModelAPI"

class CompoundRecord(ModelRestApi):
    resource_name = 'compound_records'
    datamodel = SQLAInterface(CompoundRecord)
    class_permission_name = "ModelAPI"

class MoleculeDictionary(ModelRestApi):
    resource_name = 'molecule_dictionary'
    datamodel = SQLAInterface(MoleculeDictionary)
    class_permission_name = "ModelAPI"

appbuilder.add_api(Assay)
appbuilder.add_api(Activity)
appbuilder.add_api(CompoundStructure)
appbuilder.add_api(CompoundRecord)
appbuilder.add_api(MoleculeDictionary)

