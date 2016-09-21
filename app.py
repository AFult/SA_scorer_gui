from guidata.dataset.datatypes import DataSet, BeginGroup, EndGroup, ValueProp

from guidata.dataset.dataitems import (FloatItem, IntItem, BoolItem, ChoiceItem,
                             MultipleChoiceItem, ImageChoiceItem, FilesOpenItem,
                             StringItem, TextItem, ColorItem, FileSaveItem,
                             FileOpenItem, DirectoryItem, FloatArrayItem,
                             DateItem, DateTimeItem)

import pandas as pd
import score_code as sc

prop1 = ValueProp(False)
prop2 = ValueProp(False)

class FindData(DataSet):

    g1 = BeginGroup('Data Upload')
    fname = FileOpenItem('Open File', ('xlsx', 'xls'))
    weight1 = TextItem('name of column with food dep weight')
    weight2 = TextItem('name of column with weight before food dep')
    _g1 = EndGroup('Data Upload')

    g2 = BeginGroup('Optional Parameters')
    enable = BoolItem('activate optional parameters',
                      default=False).set_prop('display', store=prop1)
    rescore = IntItem('# of choices to score').set_prop('display', active=prop1)
    rescore6 = BoolItem('rescore 6 minutes', default=False)
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

    if e.fname:
        df = pd.read_excel(e.fname, index_col=0, header=0)

        if e.rescore:
            scored = sc.SA(df, rescore = (e.rescore+1)).astype(float)
        else:
            scored = sc.SA(df).astype(float)

        if e.weight1 and e.weight2 in df.columns:
            df['percent weight'] = df[e.weight1] / df[e.weight2]

        if 'group' in df.columns and 'per' in df.columns:
            scored = pd.concat([df['group'], df['per'], scored], axis=1)
            group = scored.groupby('group')
            descr = group[['% alternation', 'arm entries']].describe()

        writer = pd.ExcelWriter(e.save)
        scored.to_excel(writer, 'scored data')
        if 'group' in df.columns and 'per' in df.columns:
            descr.to_excel(writer, 'described')
        writer.save()
