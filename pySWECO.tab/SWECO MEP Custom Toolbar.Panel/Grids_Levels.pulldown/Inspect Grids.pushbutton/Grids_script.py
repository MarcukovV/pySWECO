# import pyrevit libraries 
from pyrevit import revit, DB, forms, script
import os

# get current Revit document
doc = __revit__.ActiveUIDocument.Document

# collect all grids in the current project
grids_all = DB.FilteredElementCollector(doc).\
			OfClass(DB.Grid).\
			WhereElementIsNotElementType().\
			ToElements()

# create pinned and un-pinned grids lists by checking grids Pinned property
grids_list_pinned   = [grd for grd in grids_all if grd.Pinned == True]
grids_list_unpinned = [grd for grd in grids_all if grd.Pinned == False]

# count pinned, un-pinned and total number of grids
count_False = len(grids_list_unpinned)
count_True 	= len(grids_list_pinned)
count_grids = len(grids_all)

# turn integers into strings and present as a list
data = [
		[str(count_grids),
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
				columns = ["Total Number of Grids", "Pinned Grids Count", "Un-Pinned Grids Count"],
				title = "GRIDS INSPECTION RESULTS", 
				last_line_style ='color:green' if count_False == 0 else 'color:red')
script.exit()