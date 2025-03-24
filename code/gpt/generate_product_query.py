import openai
import time 
import pandas as pd
the_sys_template = ''' 
你是一个智能搜索助手,给定要搜索的商品标题(product_title),构建一组针对这个商品的搜索关键词(user_query)。构建的搜索关键词
需要贴近真实用户表达搜索意图的方式,并且能够表达对该给定商品的搜索意图。让我们一步步进行思考。
首先,你从商品标题中提取该商品的本质。然后,你从商品标题中提取该商品具有的重要属性。最后,你
选择商品本质（必选）,再选择一些商品重要属性（可选）按照真实用户的表达方式整合出搜索关键词。
注意搜索关键词不要过长,用户通常不构建过长的搜索关键词。
请直接按照给定格式输出你生成的一组搜索关键词(user_query)。请严格按找例子的user_query格式输出，中间使用*进行分割，直接输出所有搜索关键词构成的字符串。不要输出其他内容
请严格按找例子的user_query格式输出，中间使用*进行分割，直接输出所有搜索关键词构成的字符串。不要输出其他内容
以下是一些例子,请参考这些例子。
例一：
product_title="贝*史努*睡衣女春秋季新款柔软棉长袖家居服可外穿大码长裤套装"
首先,这个商品的本质是："睡衣","家居服"
然后,这个商品的重要属性有："套装","贝#","春秋","女","史努#"
最后,选择商品本质和商品重要属性,可整合出搜索关键词：
"家居服套装","贝#家居服","家居服 女 贝#","家居服 春秋 贝#","史努#春秋家居服"
因此, user_query="家居服套装*贝#家居服*家居服 女  贝#*家居服 春秋 贝#*史努#春秋家居服"
例二：
product_title="德国OSTMA##豆浆机家用全自动小型迷你多功能新款破壁机免煮免滤"
首先,这个商品的本质是："豆浆机","破壁机"
然后,这个商品的重要属性有："STMA##","迷你","免煮免滤"
最后,选择商品本质和商品重要属性,可整合出搜索关键词：
"OSTMA## 豆浆机","OSTMA## 破壁机","迷你豆浆机","破壁机 免煮免滤"
因此, user_query="OSTMA## 豆浆机*OSTMA## 破壁机*迷你豆浆机*破壁机 免煮免滤"

例三：
product_title="猫##酸枣糕云南特产酸角糕无添加儿童孕妇酸味办公室休闲零食"
首先,这个商品的本质是："酸枣糕","酸角糕","猫##"
然后,这个商品的重要属性有："猫##","云南特产"
最后,选择商品本质和商品重要属性,可整合出搜索关键词：
"猫##酸枣糕","云南特产酸角糕","猫##","酸角糕 猫##"
因此, user_query="猫##酸枣糕*云南特产酸角糕* 猫##*酸角糕 猫##"

例四：
product_title="孔##马齿苋调养水补水喷雾舒缓屏障保湿爽肤水护肤水女学生国货"
首先,这个商品的本质是："喷雾"
然后,这个商品的重要属性有："补水","保湿","舒缓","孔##","马齿苋"
最后,选择商品本质和商品重要属性,可整合出搜索关键词：
"补水喷雾","保湿喷雾","舒缓喷雾","孔##喷雾","马齿苋喷雾"
因此, user_query="补水喷雾* 保湿喷雾*舒缓喷雾*孔##喷雾*马齿苋喷雾"
请严格按找例子的user_query格式输出，中间使用*进行分割，直接输出所有搜索关键词构成的字符串。不要输出其他内容
'''

openai.api_key = "your_key"
def generate_product_query(the_product_title, the_sys_template):
    messages = [
        {"role": "system", "content": the_sys_template},
        {"role": "user", "content": f"现在 product_title = {the_product_title}, user_query= ?"}
    ]
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  
        messages=messages,
        temperature=0,
        max_tokens=1000  
    )
    return response['choices'][0]['message']['content'].strip()


def get_query_with_retry(the_title,a_sys_template, max_retries=3):
    retries=0
    while retries<max_retries:
        try:
            the_result=generate_product_query(the_title, a_sys_template)
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
    data=pd.read_excel('path_to_your_data.xlsx')
    data['food_query'] = data['food'].apply(lambda x: get_query_with_retry(x, the_sys_template))
    data['wear_query'] = data['wear'].apply(lambda x: get_query_with_retry(x, the_sys_template))
    data['digital_query'] = data['digital'].apply(lambda x: get_query_with_retry(x, the_sys_template))
    data['cosmetic_query'] = data['cosmetic'].apply(lambda x: get_query_with_retry(x, the_sys_template))
    data.to_excel('path_to_your_results.xlsx', index=False)



