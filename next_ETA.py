
import pandas as pd

def get_ETA(given_datetime, time_col, csv_filename):
    
    df_data_all = pd.read_csv(csv_filename)
    df_data_all[given_datetime] = pd.to_datetime(df_data_all[given_datetime], infer_datetime_format=True) + pd.Timedelta(2, unit='h')
    
    df_data_all['given_time'] = \
    pd.to_datetime(
                pd.to_datetime(df_data_all[given_datetime],
                               infer_datetime_format=True).dt.strftime('%H:%M:%S'),
                infer_datetime_format=True
                )
    ## Above line converts time from string to datetime format
    
    diff_col = []
    for col in time_col:
        print(col)
        df_data_all['diff_'+col] = df_data_all[col] - df_data_all['given_time']
        diff_col.append('diff_'+col)
    
    df_min = pd.DataFrame(df_data_all[diff_col].min(axis=1))
    df_min.columns = ['min_time']
    df_max = pd.DataFrame(df_data_all[diff_col].max(axis=1))
    df_max.columns = ['max_time']
    
    df1 = pd.concat([df_data_all,df_min,df_max], axis=1)
    df2 = df1[(df1.max_time > pd.Timedelta(0)) & (df1.min_time < pd.Timedelta(0))]
    df3 = df1[~((df1.max_time > pd.Timedelta(0)) & (df1.min_time < pd.Timedelta(0)))]
    
    if df2.shape[0]!=0:
        for col in diff_col:
            df2.loc[(df2[col] < pd.Timedelta(0)), col] = pd.NaT
        df2.min_time = pd.DataFrame(df2[diff_col].min(axis=1))
        df4 = df3.append(df2)
    else:
        df4 = df3.copy()
    
    del(df_min,df_max)
    
    
    for col in diff_col:
        df4.loc[(df4[col] == df4.min_time), 'flag'] = df4.loc[(df4[col] == df4.min_time), col[5:]]
        df4.loc[(df4[col] == df4.min_time), 'diff_time'] = df4.loc[(df4[col] == df4.min_time), col]
        
    df5 = df4.copy()
    df5['date_x'] = pd.to_datetime(df5[given_datetime], infer_datetime_format=True).dt.date
    df5['date_y'] = df5['date_x'] + pd.DateOffset(1)
    df5['date_y'] = pd.to_datetime(df5['date_y']).dt.date
    
    df5['expected_date'] = pd.NaT
    df5.loc[(df5.diff_time<pd.Timedelta(0)), 'expected_date'] = df5.loc[(df5.diff_time<pd.Timedelta(0)), 'date_y']
    df5.loc[(df5.diff_time>=pd.Timedelta(0)), 'expected_date'] = df5.loc[(df5.diff_time>=pd.Timedelta(0)), 'date_x']
    df5 = df5.reset_index()
    
    ####### Check for reindexing error ########
    #####################################
    df5['exp_date_test'] = pd.to_datetime(df5['expected_date']).dt.date.astype(str)
    df5['flag_test'] = df5['flag'].dt.time.astype(str)
    df5['expected_date'] = df5['exp_date_test'] + ' ' +df5['flag_test']
    
    df5.to_csv('ETA_file.csv')
