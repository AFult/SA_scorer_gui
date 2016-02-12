from guidata.dataset.datatypes import DataSet, BeginGroup, EndGroup

from guidata.dataset.dataitems import (FloatItem, IntItem, BoolItem, ChoiceItem,
                             MultipleChoiceItem, ImageChoiceItem, FilesOpenItem,
                             StringItem, TextItem, ColorItem, FileSaveItem,
                             FileOpenItem, DirectoryItem, FloatArrayItem,
                             DateItem, DateTimeItem)

import pandas as pd
import score_code as sc

class TestParameters(DataSet):


	fname = FileOpenItem('Open File', ('xlsx', 'xls'))
	start_col = IntItem(' # of First Column of Data', default=1)



if __name__ == "__main__":
    # Create QApplication
    import guidata
    _app = guidata.qapplication()
    e = TestParameters()
    print(e)
    if e.edit():
    	print(e)

    if e.fname and e.start_col: 
    	df = pd.read_excel(e.fname, index_col=0, header=0)
    	scored = sc.SA(df, start_col=e.start_col).astype(float)
    	print scored
