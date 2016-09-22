from guidata.dataset.datatypes import DataSet, BeginGroup, EndGroup, ValueProp

from guidata.dataset.dataitems import (FloatItem, IntItem, BoolItem, ChoiceItem,
                             MultipleChoiceItem, ImageChoiceItem, FilesOpenItem,
                             StringItem, TextItem, ColorItem, FileSaveItem,
                             FileOpenItem, DirectoryItem, FloatArrayItem,
                             DateItem, DateTimeItem)

import pandas as pd
from code import score_code as sc

prop1 = ValueProp(False)
prop2 = ValueProp(False)

class FindData(DataSet):

    g1 = BeginGroup('Data Upload')
    fname = FileOpenItem('Open File', ('xlsx', 'xls'))
    _g1 = EndGroup('Data Upload')

    g2 = BeginGroup('Optional Parameters')
    enable = BoolItem('activate optional parameters',
                      default=False).set_prop('display', store=prop1)
    rescore = IntItem('# of choices to score').set_prop('display', active=prop1)
    rescore6 = BoolItem('rescore 6 minutes', default=False)
    rescore12 = BoolItem('rescore 12 minutes', default=False)
    _g2 = EndGroup('Optional Parameters')


    save = FileSaveItem('create results', formats='xlsx')


if __name__ == "__main__":
    # Create QApplication
    import guidata
    _app = guidata.qapplication()
    e = FindData()
    print e
    if e.edit():
        print e
    if e.fname:
        writer = pd.ExcelWriter(e.save)
        df = pd.read_excel(e.fname, index_col=0, header=0)

        if df['pre_weight'].empty == False and \
           df['post_weight'].empty == False:
            weight_percentage = df['post_weight'] / df['pre_weight']
            weight_percentage.name = 'weight_percentage'

        if e.rescore:
            scored = sc.SA(df, rescore = (e.rescore+1)).astype(float)
        if e.rescore6:
            scored = sc.SA(df, rescore6 = True)
        if e.rescore12:
            scored = sc.SA(df, rescore12 = True)

        else:
            scored = sc.SA(df).astype(float)

        if weight_percentage.empty != True:
            scored = pd.concat([weight_percentage, scored], axis = 1)

        if 'group' in df.columns:
            scored = pd.concat([df['group'], scored], axis=1)
            scored = scored.dropna(thresh = 6, axis = 0)
            group = scored.groupby('group')
            descr = group[['% alternation', 'arm entries']].describe()
            scored.to_excel(writer, 'scored data')
            descr.to_excel(writer, 'described')
        else:
            scored = scored.dropna(thresh = 6, axis = 0)
            scored.to_excel(writer, 'scored data')

        writer.save()
    e.view()
