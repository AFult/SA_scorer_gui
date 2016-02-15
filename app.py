from guidata.dataset.datatypes import DataSet, BeginGroup, EndGroup, ValueProp

from guidata.dataset.dataitems import (FloatItem, IntItem, BoolItem, ChoiceItem,
                             MultipleChoiceItem, ImageChoiceItem, FilesOpenItem,
                             StringItem, TextItem, ColorItem, FileSaveItem,
                             FileOpenItem, DirectoryItem, FloatArrayItem,
                             DateItem, DateTimeItem)

import pandas as pd
import score_code as sc

prop1 = ValueProp(False)

class FindData(DataSet):

    g1 = BeginGroup('Data Upload')
    fname = FileOpenItem('Open File', ('xlsx', 'xls'))
    start_col = IntItem(' # of First Column of Data', default=1)
    _g1 = EndGroup('Data Upload')

    g2 = BeginGroup('Optional Parameters')
    enable = BoolItem('activate optional parameters',
                      default=False).set_prop('display', store=prop1)
    rescore = IntItem('# of choices to score').set_prop('display', active=prop1)
    _g2 = EndGroup('Optional Parameters')


    save = FileSaveItem('create results', formats='xlsx')


if __name__ == "__main__":
    # Create QApplication
    import guidata
    _app = guidata.qapplication()
    e = FindData()
    print(e)
    if e.edit():
        print(e)

    if e.fname and e.start_col: 
        df = pd.read_excel(e.fname, index_col=0, header=0)
        if e.rescore:
            scored = sc.SA(df, start_col=e.start_col, rescore = (e.rescore+1)).astype(float)
        else:
            scored = sc.SA(df, start_col=e.start_col).astype(float)
        scored.to_excel(e.save)
