# import pyrevit libraries
from pyrevit import revit, DB, forms, script

# output module 
output = script.get_output()

# get current Revit document
doc = __revit__.ActiveUIDocument.Document

# create a variable as a flag to catch errorrs
error_occurred = False

# collect all grids in the model
grids_all = DB.FilteredElementCollector(doc).\
			OfClass(DB.Grid).\
			WhereElementIsNotElementType().\
			ToElements()

# create a list if un-pinned grids
unpinned_grids = [grd for grd in grids_all if grd.Pinned == False]

if not grids_all:
	forms.alert(
	"There are no grids in this project",
	title = "Script is cancelled",
	ok = False
	)
	script.exit()
elif not unpinned_grids:
	forms.alert(
	"All grids are already pinned",
	title = "Script is cancelled",
	ok = False
	)
	script.exit()
else:
	yes_outcome = forms.alert(
	'All grids will be pinned. Would you like to proceed?\n\nClick "Yes" to proceed \
	or "No" to cancel',
	yes = True,
	no = True,
	warn_icon = False,
	exitscript = True
	)
	if yes_outcome == True:
		with revit.Transaction("Pin All Grids"):
			for grd in unpinned_grids:
				try:
					grd.Pinned = True
				except Exception as e:
					error_occurred = True
					error_message = output.print_md("<span style='color: black; font-family: Arial; font-size: 15px;'> \
					The grid '{}' could not be pinned due to the following error:\
					'{}'</span>".format(grd.Name, type(e).__name__))
		# final user message
		if error_occurred == False:
			msg = "All grids have been successfully pinned"
			forms.alert(
						msg,
						title = "Script is completed",
						ok = False,
						warn_icon = False
						)