import pandas as pd
import collections



#function to score spontaneous alternation
def SA(df, start = 9, rescore = 75, raw_data_start = 8):

    #build dataframe to hold rescored values
    infoframe = pd.DataFrame(index = df.index,
                             columns = ['alternations',
                                        'arm entries',
                                        '% alternation',
                                        '% perseverative errors',
                                        '% repeat entries',
                                        '% 1 entries',
                                        '% 2 entries',
                                        '% 3 entries',
                                        '% 4 entries',
                                        'arm entry inequality'])

    #score SA raw data from excel file and place in infoframe
    for index in df.index:
        drop = df.iloc[:, start:(rescore)].ix[index].dropna(how='all')
        if len(drop) > 4:
            alts = 0
            possible_alts = len(drop) - 3
            pers = 0
            repeat = 0
            arm_dict = {1:0, 2:0, 3:0, 4:0}
            for n in range(0, len(drop)):
                if drop.iloc[n] not in [1, 2, 3, 4]:
                    raise NameError('invalid arm entry input for subject %s on choice #%s: %s'
                                     % (index, n, drop.iloc[n]))
                arm_dict[drop.iloc[n]] += 1
                if n >= 2:
                    if drop.iloc[n] == drop.iloc[n-1]:
                        repeat += 1
                    if n >= 3:
                        if drop.iloc[n] == drop.iloc[n-2]:
                            pers +=1
                        if n >= 4:
                            alt_list = [drop.iloc[n], drop.iloc[n-1], drop.iloc[n-2], drop.iloc[n-3]]
                            alt_count = collections.Counter(alt_list).values()
                            if True not in map(lambda x: x > 1, alt_count):
                                alts += 1
            per_entry_diff = sum([float(x)/len(drop) - .25 if float(x)/len(drop) > .25 
                                  else .25 - float(x)/len(drop) 
                                  for x in arm_dict.values()])
            infoframe['alternations'][index] = int(alts)
            infoframe['arm entries'][index] = len(drop)
            infoframe['% alternation'][index] = float(alts)/possible_alts * 100
            infoframe['% perseverative errors'][index] = float(pers)/(len(drop) - 2) * 100
            infoframe['% repeat entries'][index] = float(repeat)/(len(drop) - 1) * 100
            infoframe['% 1 entries'][index] = float(arm_dict[1]) / len(drop) * 100
            infoframe['% 2 entries'][index] = float(arm_dict[2]) / len(drop) * 100
            infoframe['% 3 entries'][index] = float(arm_dict[3]) / len(drop) * 100
            infoframe['% 4 entries'][index] = float(arm_dict[4]) / len(drop) * 100
            infoframe['arm entry inequality'][index] = per_entry_diff / 4 * 100

    return infoframe.astype(float)