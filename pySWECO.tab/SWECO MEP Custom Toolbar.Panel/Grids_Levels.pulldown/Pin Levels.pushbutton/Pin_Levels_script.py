# import pyrevit libraries
from pyrevit import revit, DB, forms, script

# output module 
output = script.get_output()

# get current Revit document
doc = __revit__.ActiveUIDocument.Document

# create a variable as a flag to catch errors
error_occurred = False

# collect all levels in the model
levels_all = DB.FilteredElementCollector(doc).\
			OfClass(DB.Level).\
			WhereElementIsNotElementType().\
			ToElements()

# create a list if un-pinned levels
unpinned_levels = [lvl for lvl in levels_all if lvl.Pinned == False]

if not unpinned_levels:
	forms.alert(
	"All levels are already pinned", 
	title = "Script is cancelled", 
	ok = False
	)
	script.exit()
else:
	yes_outcome = forms.alert(
	'All levels will be pinned. Would you like to proceed?\n\nClick "Yes" to proceed \
	or "No" to cancel',
	yes = True,
	no = True,
	warn_icon = False,
	exitscript = True
	)
	if yes_outcome == True:
		with revit.Transaction("Pin All Levels"):
			for lvl in unpinned_levels:
				try:
					lvl.Pinned = True
				except Exception as e:
					error_occurred = True
					error_message = output.print_md("<span style='color: black; font-family: Arial; font-size: 15px;'> \
					The level '{}' could not be pinned due to the following error:\
					'{}'</span>".format(lvl.Name, type(e).__name__))
		# final user message
		if error_occurred == False:
			msg = "All levels have been successfully pinned"
			forms.alert(
						msg,
						title = "Script is completed", 
						ok = False, 
						warn_icon = False
						)