# import pyrevit libraries
from pyrevit import revit, DB, forms, script

forms.inform_wip()
script.exit()

# get current Revit document
doc_c = __revit__.ActiveUIDocument.Document

# import output module
output = script.get_output()

# create a dialog window with 2 choices: Sheet and Sheet Set
select_mode = forms.alert(
			msg = "Revision to be applied to an active sheet view only or to a sheets set?",
			ok = False,
			warn_icon = False,
			options = ["Active Sheet View Only", "Sheets Set"]
			)
# scenario where Revi user choose zero options
if not select_mode:
	forms.alert(
	msg = 'No option has been selected',
	title = 'Script is cancelled',
	ok = False,
	exitscript = True)

#1 scenario where Revit user chooses Active Sheet
if select_mode == "Active Sheet View Only":
	rev_opt_1 = forms.select_revisions(
	title = 'Select Revision to Apply to an Active Sheet View',
	button_name = 'Proceed',
	width = 500,
	multiple = False,
	filterfunc = None,
	doc = doc_c
	)
	if not rev_opt_1:
		forms.alert(
		msg = 'No revision has been selected',
		title = 'Script is cancelled',
		ok = False,
		exitscript = True)
#2 scenario where Revit user chooses Sheets Set
if select_mode == "Sheets Set":
	rev_opt_2 = forms.select_revisions(
	title = 'Select Revision to Apply to a Sheets Set',
	button_name = 'Proceed',
	width = 500,
	multiple = False,
	filterfunc = None,
	doc = doc_c
	)
	if not rev_opt_2:
		forms.alert(
		msg = 'No revision has been selected',
		title = 'Script is cancelled',
		ok = False,
		exitscript = True)


