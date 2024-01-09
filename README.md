# lDetector
lDetector is a novel testing approach targeting missed recalls of search components in e-commerce apps.

To detect missed recalls, lDetector generates multiple queries toward the same target shop by LLM and compares the search results. Any inconsistency in the search results hints at a potential missed recall.  For example, five queries can be generated for the same restaurant. If four queries can recall this restaurant but one can not, lDetector reports a missed recall.

The designing of lDetector involves three major considerations: 1) the choice of the LLM used; 2)the prompt used for query generation; 3)the LLM validation step. 
To illustrate the effectiveness of lDetector, three experiments are designed targeting each of the three major considerations. Apart from that, an experiment using real online industrial data is conducted to explore lDetector's handiness in a real industrial setting.

Here we report 1）experimental codes; 2) raw experimental results. For data security concerns, we omit both data and the raw results of the real-industrial-data experiment. Reported data and code have been desensitized according to the data security requirements of M Inc.

The experimental codes are implemented with Python and require the following packages: pandas, re, itertools, jieba, concurrent, open ai, requests, tenacity, requests, json, jsonpath, ast. We recommend Python 3.8 and higher versions.


## 1.Data



### 1.1 Result overview

- Comparing models of **different parameter sizes**, the test results are as follows:

| Model                                                        | Model Size | Generated Test Cases                                         | Suspicious missed recalls                                    | Shops Involved | Confirmed missed recalls | Confirmed Shops Involved | False positive |
| ------------------------------------------------------------ | ---------- | ------------------------------------------------------------ | ------------------------------------------------------------ | -------------- | ------------------------ | ------------------------ | -------------- |
| [gpt-neo-2.7B](https://huggingface.co/EleutherAI/gpt-neo-2.7B) | 2.7B       | [2607](https://github.com/xieeryihe/lDetector/blob/main/data/cases/gpt-neo-2.7B.xlsx) | [35](https://github.com/xieeryihe/lDetector/blob/main/data/final/final-gpt-neo-2.7B.xlsx) | 35             | 6                        | 6                        | 29             |
| [chatglm2-6b](https://huggingface.co/THUDM/chatglm2-6b)      | 6B         | [3803](https://github.com/xieeryihe/lDetector/blob/main/data/cases/chatglm2-6b.xlsx) | [54](https://github.com/xieeryihe/lDetector/blob/main/data/final/final-chatglm2-6b.xlsx) | 44             | 32                       | 26                       | 22             |
| [Qwen-14B-Chat-Int4](https://huggingface.co/Qwen/Qwen-14B-Chat-Int4) | 14B        | [4375](https://github.com/xieeryihe/lDetector/blob/main/data/cases/Qwen-14B-Chat-Int4.xlsx) | [64](https://github.com/xieeryihe/lDetector/blob/main/data/final/final-Qwen-14B-Chat-Int4.xlsx) | 48             | 54                       | 40                       | 10             |
| [gpt-3.5-turbo](https://platform.openai.com/docs/models/gpt-3-5) | over 100B  | [3724](https://github.com/xieeryihe/lDetector/blob/main/data/cases/chatgpt3.5-cot.xlsx) | [47](https://github.com/xieeryihe/lDetector/blob/main/data/final/final-chatgpt3.5-cot.xlsx) | 33             | 46                       | 33                       | 1              |

To make it easier to understand, let's take the first row as an example: 

> lDetector with gpt-neo-2.7B generates 2607 test cases, and reports 35 suspicious missed recalls in total, involving 35 shops. After human confirmation, 6 entries are confirmed as real missed recalls, involving 6 shops. 

​    


The **generated test cases** raw data can be found in the hyperlink in `Generated Test Cases` column of the table, as well as the **missed recalls** shown in the `Suspicious missed recalls` column. 

- For model **gpt-3.5-turbo**, we compare the results of different prompts:

| Prompt                | Generated Test Cases                                         | Suspicious missed recalls                                    | Shops Involved | Confirmed missed recalls | Confirmed Shops Involved | False positive |
| --------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | -------------- | ------------------------ | ------------------------ | -------------- |
| Chain of Thought(cot) | [3724](https://github.com/xieeryihe/lDetector/blob/main/data/cases/chatgpt3.5-cot.xlsx) | [47](https://github.com/xieeryihe/lDetector/blob/main/data/final/final-chatgpt3.5-cot.xlsx) | 33             | 46                       | 33                       | 1              |
| few-shot              | [5700](https://github.com/xieeryihe/lDetector/blob/main/data/cases/chatgpt3.5-few-shot.xlsx) | [156](https://github.com/xieeryihe/lDetector/blob/main/data/final/final-chatgpt3.5-few-shot.xlsx) | 98             | 121                      | 76                       | 35             |
| zero-shot             | [4622](https://github.com/xieeryihe/lDetector/blob/main/data/cases/chatgpt3.5-zero-shot.xlsx) | [46](https://github.com/xieeryihe/lDetector/blob/main/data/final/final-chatgpt3.5-zero-shot.xlsx) | 42             | 39                       | 37                       | 7              |

​    
- For model **gpt-3.5-turbo**, and use **Chain of Thought prompt**, we compared the results with/ without a LLM validation step:
  
**Without LLM validation step**, a total of 3,724 test cases were generated, and [78 missed recalls](https://github.com/xieeryihe/lDetector/blob/main/data/final/final-no_check_gpt3.5results.xlsx) were found, involving 45 stores. After manual inspection, 71 of the them were accurate (involving 42 stores), and another 7 were false positives.

**With LLM validation step**, a total of 3,724 test cases were generated, and [47 missed recalls](https://github.com/xieeryihe/lDetector/blob/main/data/final/final-chatgpt3.5-cot.xlsx) were found, involving 33 stores. After manual inspection, 46 of them were accurate (involving 33 stores), and another 1 were false positives.
  

> For privacy concerns and security of cooperation tools, we removed **the_search_url** and **the_city_id** columns and anonymized **poi_name**, **latitude**, **longitude** and **test_case** columns, while masked data in the following table is only used to show the data format.

​    

### 1.2 File：./data/shop.xlsx

The [shop.xlsx](https://github.com/xieeryihe/lDetector/blob/main/data/shops.xlsx) displays shops that we used as the input data (target shops). Those shops were openly accessible via the Baidu Map API. The sample data format is shown in the table below.

| poi_name                 | latitude  | longitude | city | poi_type |
| ------------------------ | --------- | --------- | ---- | -------- |
| `***餐厅(*里河店)`       | Anonymous | Anonymous | 北京 | 鲁菜     |
| `*****铁锅烀羊肉(*井店)` | Anonymous | Anonymous | 北京 | 中餐馆   |
| ...                      | ...       | ...       | ...  | ...      |

The `poi_name` indicates the full name of the store, and `poi_type` indicates the category of the store.

​    

### 1.3 Folder：./data/cases

For each file in the [cases](https://github.com/xieeryihe/lDetector/tree/main/data/cases) directory, such as `chatglm2-6b.xlsx`, we first use `chatglm2-6b` model to generate search keywords(`test_case`) based on the raw data in `shops.xlsx`. Then we use the **same** `chatglm2-6b` model to self-check whether these keywords are reasonable (in line with human-constructed keywords). The sample data format of `chatglm2-6b.xlsx` is shown in the table below.

| poi_name           | latitude  | longitude | city | poi_type | test_case          | test_case_judgement |
| ------------------ | --------- | --------- | ---- | -------- | ------------------ | ------------------- |
| `***餐厅(*里河店)` | Anonymous | Anonymous | 北京 | 鲁菜     | `***餐厅(*里河店)` | no                  |
| `***餐厅(*里河店)` | Anonymous | Anonymous | 北京 | 鲁菜     | `***餐厅`          | yes                 |
| `***餐厅(*里河店)` | Anonymous | Anonymous | 北京 | 鲁菜     | `*里河店`          | yes                 |
| ..                 | ...       | ...       | ...  | ...      | ...                | ...                 |

The `test_case` column represents the keywords generated by the model, and the `test_case_judgement` column represents the self-checking results. Item `yes` indicates that the model believes a certain keyword is **reasonable** to be used to retrieve the target shop. And `no` indicates the opposite.

​    

### 1.4 Folder：./data/final

For each file in [final](https://github.com/xieeryihe/lDetector/tree/main/data/final) directory, such as `final-chatGLm2-6b.xlsx`, the sample data format is shown in the table below.

|      | leak_judgement | equal_leak_exist | accurate_leak | equal_ratio | query_type  | self_leak | searched_shops                                       | poi_name                      | latitude  | longitude | city | poi_type | test_case    | test_case_judgement | human |
| ---- | -------------- | ---------------- | ------------- | ----------- | ----------- | --------- | ---------------------------------------------------- | ----------------------------- | --------- | --------- | ---- | -------- | ------------ | ------------------- | ----- |
| 102  | leak           | partial_leak     | yes           | 0.952380952 | equal_query | yes       | `["***创意汉堡(**港湾店)",  "****创意汉堡(**屯店)"]` | `["***创意汉堡(**港湾店)",  ` | Anonymous | Anonymous | 北京 | 汉堡     | `**创意汉堡` | yes                 | 0     |

The first 6 columns of the table are mainly used to determine whether a missed recall occurs, and the specific meaning can be understood in oracle.py. The main concern is the **human** column, indicating the result of human judgment, where **1** indicates that it is a **missed recall** and **0** indicates a false positive.

​    

## 2.code

We test lDetector on both local(gpt-neo-2.7B, etc) and remote models(gpt-3.5-turbo), so we have two versions of code in directories `code/local` and `code/gpt`, respectively.

> For data security and privacy concerns, we mask shop names in the prompt while it doesn't affect understanding.

​    

### 2.1 Folder: ./code/local

| File                                                         | Description                                                  |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| [generate_local.py](https://github.com/xieeryihe/lDetector/blob/main/code/local/generate_local.py) | Use the shops in `shops.xlsx` as target shops to generate the `test_case`. |
| [check_local.py](https://github.com/xieeryihe/lDetector/blob/main/code/local/check_local.py) | Check whether the generated test cases are resonable. |
| [*_server.py](https://github.com/xieeryihe/lDetector/blob/main/code/local/glm_server.py) | Deploy the model locally so  we can access the local model in the same way as access the remote model. |

​    

### 2.2 Folder: ./code/gpt

| File                                                         | Description                        |
| ------------------------------------------------------------ | ---------------------------------- |
| [generate_gpt.py](https://github.com/xieeryihe/lDetector/blob/main/code/gpt/generate_gpt.py) | Use chatgpt-3.5-turbo to generate test cases. |
| [check_gpt.py](https://github.com/xieeryihe/lDetector/blob/main/code/gpt/check_gpt.py) | Use chatgpt-3.5-turbo to check whether the test cases are resonable.    |

​    

### 2.3 File: ./code/oracle.py

The [test oracle code](https://github.com/xieeryihe/lDetector/blob/main/code/oracle.py).  It is used to determine whether a missed recall occurs.

All search results are obtained from the search API of M Inc. 
We omit the code snippet of geting search results given the search keywords (test cases) for security concerns of the industrial search API.

​    

## 3.File Tree

We list the file tree of the repository.

```txt
│  README.md
│
├─code
│  │  oracle.py
│  │
│  ├─gpt
│  │      check_gpt.py
│  │      generate_gpt.py
│  │
│  └─local
│          check_local.py
│          generate_local.py
│          glm_server.py
│          neo_server.py
│          qwen_server.py
│
└─data
    │  shops.xlsx
    │
    ├─cases
    │      chatglm2-6b.xlsx
    │      chatgpt3.5-cot.xlsx
    │      chatgpt3.5-few-shot.xlsx
    │      chatgpt3.5-zero-shot.xlsx
    │      gpt-neo-2.7B.xlsx
    │      Qwen-14B-Chat-Int4.xlsx
    │
    └─final
            final-chatglm2-6b.xlsx
            final-chatgpt3.5-cot.xlsx
            final-chatgpt3.5-few-shot.xlsx
            final-chatgpt3.5-zero-shot.xlsx
            final-gpt-neo-2.7B.xlsx
            final-Qwen-14B-Chat-Int4.xlsx
```

