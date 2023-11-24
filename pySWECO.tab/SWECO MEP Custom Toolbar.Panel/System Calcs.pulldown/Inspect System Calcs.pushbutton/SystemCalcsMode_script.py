# import pyrevit libraries 
from pyrevit import revit, DB, forms, script
import os

# get current Revit document
doc = __revit__.ActiveUIDocument.Document

# collect duct system types in current model / returns a list
mep_duct_sys = DB.FilteredElementCollector(doc).\
				OfClass(DB.Mechanical.MechanicalSystemType).\
				WhereElementIsElementType().\
				ToElements()

# collect pipe system types in current model / returns a list
mep_pipe_sys = DB.FilteredElementCollector(doc).\
				OfClass(DB.Plumbing.PipingSystemType).\
				WhereElementIsElementType().\
				ToElements()

# create lists of system types and their calcs modes
duct_calcs_sys, pipe_calcs_sys = [], []

# append duct system types and calculation parameter modes to a list
for dc in mep_duct_sys:
	duct_sys	= dc.get_Parameter(DB.BuiltInParameter.ALL_MODEL_TYPE_NAME).AsString()
	duct_calcs	= dc.get_Parameter(DB.BuiltInParameter.RBS_DUCT_SYSTEM_CALCULATION_PARAM).AsValueString()
	duct_calcs_sys.append((duct_sys, duct_calcs))
	
# append pipe system types and calculation parameter modes to a list
for pp in mep_pipe_sys:
	pipe_sys	= pp.get_Parameter(DB.BuiltInParameter.ALL_MODEL_TYPE_NAME).AsString()
	pipe_calcs	= pp.get_Parameter(DB.BuiltInParameter.RBS_PIPE_SYSTEM_CALCULATION_PARAM).AsValueString()
	pipe_calcs_sys.append((pipe_sys, pipe_calcs))

# sort duct list in alphabetical order and count total number of duct system types
data_duct = sorted(duct_calcs_sys)
count_duct = len(duct_calcs_sys)

# sort pipe list in alphabetical order and count total number of pipe system types
data_pipe = sorted(pipe_calcs_sys)
count_pipe = len(pipe_calcs_sys)

# get current working directory where current Python script is located
# specify the relative path to the file image
# join the current directory with the relative path to create the full path
current_dir      = os.path.dirname(os.path.realpath(__file__))
relative_path    = 'pySWECOLogo.png'
sweco_image_path = os.path.join(current_dir, relative_path)

# output module / set output window style
output = script.get_output()
output.add_style('body { color: black; background-color: gainsboro; font-size: 14px; font-family: Arial }')

# import SWECO logo
output.print_image(sweco_image_path)

output.print_md("<span style='color: black; font-size: 15px;'> Current Revit document contains {} \
Duct System Types and {} Pipe System Types. Here are the lists of the system types and calculation \
parameter modes:</span>".format(str(count_duct), str(count_pipe)))

output.print_table(data_duct, 
					columns = ["1. DUCT SYSTEM TYPE", "CALCULATION PARAMETER MODE"]
					)

output.print_table(data_pipe, 
					columns = ["2. PIPE SYSTEM TYPE", "CALCULATION PARAMETER MODE"]
					)
script.exit()