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
    weight1 = TextItem('name of column with food dep weight')
    weight2 = TextItem('name of column with weight before food dep')
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
            scored = sc.SA(df, start=e.start_col, rescore = (e.rescore+1)).astype(float)
        elif e.weight1 and e.weight2 in df.columns:
            scored = sc.SA(df, start=e.start_col).astype(float)
            df['per'] = df[e.weight1] / df[e.weight2]
            scored = pd.concat([df['group'], df['per'], scored], axis=1)
            group = scored.groupby('group')
            descr = group[['% alternation', 'arm entries']].describe()
        else:
            scored = sc.SA(df, start=e.start_col).astype(float)
            #df['weight per'] = df.iloc[:,e.weight1:(e.weight1+1)].div(df.iloc[:,e.weight2:(e.weight2+1)])
            #scored = pd.concat([df.iloc[:,:(e.start_col)], df['weight per'], scored], axis = 1) 
        writer = pd.ExcelWriter(e.save)
        scored.to_excel(writer, 'scored data')
        descr.to_excel(writer, 'described')
        writer.save()

