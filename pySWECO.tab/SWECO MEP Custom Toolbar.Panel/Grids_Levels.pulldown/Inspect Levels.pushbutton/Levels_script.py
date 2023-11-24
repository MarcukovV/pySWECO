# import pyrevit libraries 
from pyrevit import revit, DB, forms, script
import os

# get current Revit document
doc = __revit__.ActiveUIDocument.Document

# collect all levels in the current project / returns a list
levels_all = DB.FilteredElementCollector(doc).\
			OfClass(DB.Level).\
			WhereElementIsNotElementType().\
			ToElements()

# create lists of pinned and unpinned levels by checking levels Pinned property
levels_list_pinned   = [lvl for lvl in levels_all if lvl.Pinned == True]
levels_list_unpinned = [lvl for lvl in levels_all if lvl.Pinned == False]

# count pinned, unpinned and total number of levels
count_False  = len(levels_list_unpinned)
count_True   = len(levels_list_pinned)
count_levels = len(levels_all)

# turn integers into strings and present as a list
data = [
		[str(count_levels),
		str(count_True),
		str(count_False)]
		]

# get current working directory where current Python script is located
# specify the relative path to the file image
# join the current directory with the relative path to create the full path
current_dir      = os.path.dirname(os.path.realpath(__file__))
relative_path    = 'pySWECOLogo.png'
sweco_image_path = os.path.join(current_dir, relative_path)

# output module 
output = script.get_output()

# set output window style
output.add_style('body { color: black; font-size: 14px; background-color: gainsboro; font-family: Arial; }')

# import SWECO logo
output.print_image(sweco_image_path)

# output as a table / pyrevit forms
output.print_table(data, 
				columns = ["Total Number of Levels", "Pinned Levels Count", "Un-Pinned Levels Count"],
				title = "LEVELS INSPECTION RESULTS", 
				last_line_style ='color:green' if count_False == 0 else 'color:red')
script.exit()