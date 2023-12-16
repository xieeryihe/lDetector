import pandas as pd
import ast
import re

def get_self_leak(poi_name, searched_shops):  # If a query can find the target shop
    the_pattern = r'[^\w\s\[\]\'\",]'
    poi_name = poi_name.replace("（", "(").replace("）", ")").replace("，",",")
    poi_name = re.sub(the_pattern, '', poi_name)
    searched_shops = searched_shops.replace("（", "(").replace("）", ")").replace("，",",")
    searched_shops = re.sub(the_pattern, '', searched_shops)
    the_shop_list=ast.literal_eval(searched_shops)
    if str(poi_name) in the_shop_list:
        self_leak='no'
    else:
        self_leak='yes'
    return self_leak

def get_query_type(test_case, poi_name):
    if test_case==poi_name:
        query_type='accurate_query'
    else:
        query_type='equal_query'
    return query_type

def get_equal_ratio(a_df):  # based on shops that can be searched by query
    the_ref=a_df[a_df['self_leak']=='no']
    ref_list=[]
    for item in the_ref['searched_shops']:
        ref_list.extend(item)
    ref_list=list(set(ref_list))
    list_equal_ratio=[]
    all_results=a_df['searched_shops'].values.tolist()
    for i in range(len(all_results)):
        the_common_part=set(all_results[i]).intersection(set(ref_list))
        list_sim=len(the_common_part)/len(set(all_results[i]))
        list_equal_ratio.append(list_sim)
    a_df.insert(0, 'equal_ratio',list_equal_ratio)
    return a_df

def get_accurate_leak(a_df):  # check if leak happens in accurate search
    the_target_list=a_df[a_df['query_type']=='accurate_query']['self_leak'].values.tolist()
    if len(the_target_list)==1:
        a_df.insert(0,'accurate_leak',the_target_list[0])
    else:
        a_df.insert(0,'accurate_leak','not_valid')
    return a_df


def get_equal_leak_exist(a_df):  # check if leak happens in equal_query
    equal_query_results_list=a_df[a_df['query_type']=='equal_query']['self_leak'].values.tolist()
    if 'yes' in equal_query_results_list and 'no'in equal_query_results_list:
        equal_leak_exist='partial_leak'
    elif 'yes' in equal_query_results_list and 'no' not in equal_query_results_list:
        equal_leak_exist='full_leak'
    elif 'yes' not in equal_query_results_list and 'no' in equal_query_results_list:
        equal_leak_exist='full_normal'
    else:  # other circumstances
        equal_leak_exist='not_valid'
    a_df.insert(0,'equal_leak_exist', equal_leak_exist)
    return  a_df

# get query that may leak
def get_leak_judgement(accurate_leak, query_type, self_leak, equal_leak_exist):
    # accurate search does not come up, equivalent query search does not come up partly, the equivalent query that does not come up has problems
    if query_type=='equal_query' and self_leak=='yes'and accurate_leak=='yes' and equal_leak_exist=='partial_leak':  
        leak_judement='leak'
    # accurate search comes up, equivalent query search does not come up all, the equivalent query that does not come up has problems
    elif query_type=='equal_query' and self_leak=='yes'and accurate_leak=='no':
        leak_judement='leak'
    else:
        leak_judement='normal'
    return leak_judement

if __name__=='__main__':
    data=pd.read_excel('input.xlsx', index_col=0)
    data.insert(0,'self_leak',data.apply(lambda x: get_self_leak(x['poi_name'],x['searched_shops']),axis=1))
    data.insert(0,'query_type',data.apply(lambda x: get_query_type(x['test_case'],x['poi_name']),axis=1))
    data=data.groupby('poi_name').apply(get_equal_ratio).reset_index(drop=True)
    data=data.groupby('poi_name').apply(get_accurate_leak).reset_index(drop=True)
    data=data.groupby('poi_name').apply(get_equal_leak_exist).reset_index(drop=True)
    data.insert(0,'leak_judgement',data.apply(lambda x: get_leak_judgement(x['accurate_leak'],x['query_type'],x['self_leak'],x['equal_leak_exist']),axis=1))
    # important leak
    important_leak=data[(data['leak_judgement']=='leak')&(data['test_case_judegement']=='yes')&(data['equal_ratio']>0.7)]
    important_leak.info()
    important_leak.to_excel('output.xlsx',index=True) 


important_leak.head()

a=set(important_leak['poi_name'].values.tolist())
print(len(a))
print(a)



