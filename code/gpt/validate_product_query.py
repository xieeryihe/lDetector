
import openai
import time 
import pandas as pd
the_sys_template = ''' 
你是一个智能搜索助手,给定要搜索的商品标题(title)和自动构建的搜索关键词(generated_query),给出判断该搜索关键词是否合理的答案（answer）。
构建的搜索关键词需要贴近真实用户表达搜索意图的方式,并且能够表达对该给定商品的搜索意图，否则便不合理.
表达方式奇怪，不符合普通用户表达方式属于不合理。answer='否'.
无法表达对商品的搜索意图属于不合理。answer='否'.

以下是一些例子,请参考这些例子。
例一：
title="可##自制肉桂香料碱水面包解馋小零食休闲食品小吃健康早餐面包"
generated_query="碱水面包"
answer="是"
例二：
title="可##自制肉桂香料碱水面包解馋小零食休闲食品小吃健康早餐面包"
generated_query="解馋小吃"
该搜索关键词过于宽泛，无法表达搜索意图.
answer="否"

例三：
title="优尚####同款黑松露火腿苏打饼干梳打春节送礼年货休闲零食礼盒1200g"
generated_query="####黑松露火腿苏打饼干 春节"
该搜索关键词不符合一般表达方式.
answer="否"

例四：
title="ZX##轻奢高端品牌夹克男外套冲锋 衣三合一秋冬休闲新款潮流防风衣服 黑色【刺绣标】三合一冬款 4XL 180-195斤"
generated_query="ZX##潮流衣"
该搜索关键词不符合一般表达方式.
answer="否"

请严格按找例子的answer格式输出,只输出"是"或者"否"。不要输出其他内容.
'''

openai.api_key = "your_key"

def validate_query(the_product_title, the_generated_query, the_sys_template):
    messages = [
        {"role": "system", "content": the_sys_template},
        {"role": "user", "content": f"现在 title = {the_product_title}, generated_query = {the_generated_query}, answer= ?"}
    ]
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  
        messages=messages,
        temperature=0,
        max_tokens=1000  
    )
    return response['choices'][0]['message']['content'].strip()

def get_validation_with_retry(the_product_title, the_generated_query, the_sys_template, max_retries=3):
    retries=0
    while retries<max_retries:
        try:
            the_result=validate_query(the_product_title, the_generated_query, the_sys_template)
            return the_result
            break
        except BaseException as e:
            retries+=1
            print(f"Attempt {retries} failed with error: {str(e)}")
            time.sleep(5)
    else:
        print("All attempts failed")
        return('failed')
            
if __name__=='__main__':
    data=pd.read_excel('path_to_your_file.xlsx')

    data['validation_result'] = data.apply(
        lambda row: get_validation_with_retry(row['title'], row['generated_query'], the_sys_template),
        axis=1
    )
    data2=data[data['validation_result']=='是']
    data2.to_excel('path_to_your_file.xlsx', index=False)


