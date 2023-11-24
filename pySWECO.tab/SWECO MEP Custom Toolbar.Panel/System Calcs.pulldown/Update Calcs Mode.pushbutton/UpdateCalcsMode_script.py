# import pyrevit libraries
from pyrevit import revit, DB, forms, script
from Autodesk.Revit.DB.Mechanical import *

# get current Revit document
doc = __revit__.ActiveUIDocument.Document

# output module 
output = script.get_output()

# create a variable as a flag to catch errors
error_occurred = False

# collect all duct system types in current model
duct_sys_type = DB.FilteredElementCollector(doc).\
				OfClass(DB.Mechanical.MechanicalSystemType).\
				WhereElementIsElementType().\
				ToElements()

# collect all pipe system types in current model
pipe_sys_type = DB.FilteredElementCollector(doc).\
				OfClass(DB.Plumbing.PipingSystemType).\
				WhereElementIsElementType().\
				ToElements()

# create lists that will contain system types which modes do not equal to None and Performance
mep_non_none, mep_non_perf = [], []

# collect duct system types which modes do not equal to None and Performance and append to the above lists
for dc in duct_sys_type:
	duct_mode = dc.CalculationLevel
	if str(duct_mode) != "None":
		mep_non_none.append(dc)
	if str(duct_mode) != "Performance":
		mep_non_perf.append(dc)

# collect pipe system types which modes do not equal to None and Performance and append to the above lists
for pp in pipe_sys_type:
	pipe_mode = pp.CalculationLevel
	if str(pipe_mode) != "None":
		mep_non_none.append(pp)
	if str(pipe_mode) != "Performance":
		mep_non_perf.append(pp)

# create a dialog window with 2 choices: None and Performance
select_mode = forms.alert(
			msg = "Select either 'None' or 'Performance' calculation parameter mode:",
			ok = False,
			warn_icon = False,
			options = ["None", "Performance"]
			)

# scenario if Revit user chooses zero options
if not select_mode:
	forms.alert(
	"No calculation parameter mode selected",
	title = "Script is cancelled",
	ok = False
	)
	script.exit()

# 1 scenario where Revit user decides to set everything to None mode
if select_mode == "None":
# scenario where all system types have already mode None
	if not mep_non_none:
		forms.alert(
		'All duct and piping systems calculation parameters are already set to "None" mode',
		title = "Script is cancelled",
		ok = False,
		)
		script.exit()
	else:
		none_outcome = forms.alert(
		'All duct and piping systems calculation parameters will be set to\
		"None" mode. Would you like to proceed?\n\nClick "Yes" to proceed or "No" to cancel',
		sub_msg = 'Please note: BIM Managers only can perform this action',
		yes = True,
		no = True,
		warn_icon = False,
		exitscript = True
		)
		if none_outcome == True:
			with revit.Transaction('Set All Calculation Parameters to "None" Mode'):
				for mep in mep_non_none:
					try:
						mep.CalculationLevel = SystemCalculationLevel.None
					except Exception as e:
						error_occurred = True
						mep_type_name = mep.get_Parameter(DB.BuiltInParameter.ALL_MODEL_TYPE_NAME).AsString()
						error_message = output.print_md("<span style='color: black; font-family: Arial; font-size: 15px;'> \
						'{}' system type could not be updated due to the following error:\
						'{}'</span>".format(mep_type_name, type(e).__name__))
			# final user message (None)
			if error_occurred == False:
				msg = "All duct and piping systems calculation parameters have been set to None mode"
				forms.alert(
							msg, 
							title = "Script is successfully completed", 
							ok = False, 
							warn_icon = False
							)
# 2 scenario where Revit user decides to set everything to Performance mode
if select_mode == "Performance":
# scenario where all system types have already mode Performance
	if not mep_non_perf:
		forms.alert(
		'All duct and piping systems calculation parameters are already set to "Performance" mode',
		title = "Script is cancelled",
		ok = False
		)
		script.exit()
	else:
		performance_outcome = forms.alert(
		'All duct and piping systems calculation parameters will be set to\
		"Performance" mode. Would you like to proceed?\n\nClick "Yes" to proceed or "No" to cancel',
		sub_msg = 'Please note: BIM Managers only can perform this action',
		yes = True,
		no = True,
		warn_icon = False,
		exitscript = True
		)
		if performance_outcome == True:
			with revit.Transaction('Set All Calculation Parameters to "Performance" Mode'):
				for mep in mep_non_perf:
					try:
						mep.CalculationLevel = SystemCalculationLevel.Performance
					except Exception as e:
						error_occurred = True
						mep_type_name = mep.get_Parameter(DB.BuiltInParameter.ALL_MODEL_TYPE_NAME).AsString()
						error_message = output.print_md("<span style='color: black; font-family: Arial; font-size: 15px;'> \
						'{}' system type could not be updated due to the following error:\
						'{}'</span>".format(mep_type_name, type(e).__name__))
			# final user message (Performance)
			if error_occurred == False:
				msg = "All duct and piping systems calculation parameters have been set to Performance mode"
				forms.alert(
							msg, 
							title = "Script is successfully completed", 
							ok = False, 
							warn_icon = False
							)