# lDetector

Here we list all artifacts of lDetector. We report both codes used and raw experimental results.

​    

## 1.Data



### 1.1 Result overview

- Comparing models of **different sizes**, the test results are as follows:

| Model                                                        | Model Size | Generated Test Cases                                         | Suspicious missed recalls                                    | Shops Involved | Confirmed missed recalls | Confirmed Shops Involved | False positive |
| ------------------------------------------------------------ | ---------- | ------------------------------------------------------------ | ------------------------------------------------------------ | -------------- | ------------------------ | ------------------------ | -------------- |
| [gpt-neo-2.7B](https://huggingface.co/EleutherAI/gpt-neo-2.7B) | 2.7B       | [2607](https://github.com/xieeryihe/lDetector/blob/main/data/cases/gpt-neo-2.7B.xlsx) | [35](https://github.com/xieeryihe/lDetector/blob/main/data/final/final-gpt-neo-2.7B.xlsx) | 35             | 6                        | 6                        | 29             |
| [chatglm2-6b](https://huggingface.co/THUDM/chatglm2-6b)      | 6B         | [3803](https://github.com/xieeryihe/lDetector/blob/main/data/cases/chatglm2-6b.xlsx) | [54](https://github.com/xieeryihe/lDetector/blob/main/data/final/final-chatglm2-6b.xlsx) | 44             | 32                       | 26                       | 22             |
| [Qwen-14B-Chat-Int4](https://huggingface.co/Qwen/Qwen-14B-Chat-Int4) | 14B        | [4375](https://github.com/xieeryihe/lDetector/blob/main/data/cases/Qwen-14B-Chat-Int4.xlsx) | [64](https://github.com/xieeryihe/lDetector/blob/main/data/final/final-Qwen-14B-Chat-Int4.xlsx) | 48             | 54                       | 40                       | 10             |
| [gpt-3.5-turbo](https://platform.openai.com/docs/models/gpt-3-5) | over 100B  | [3724](https://github.com/xieeryihe/lDetector/blob/main/data/cases/chatgpt3.5-cot.xlsx) | [47](https://github.com/xieeryihe/lDetector/blob/main/data/final/final-chatgpt3.5-cot.xlsx) | 33             | 46                       | 33                       | 1              |

To make it easier to understand, let's take the first row an example: 

> lDetector with gpt-neo-2.7B generates 2607 test cases, and reports 35 suspicipus missed recalls in total, invoving 35 shops. After human confirmation, 6 entries are confirmed as real missed recalls, involving 6 shops. 

​    


The **generated test cases** raw data can be found in the hyperlink in `Generated Test Cases` column of the table, as well as the **missed recalls** shown in the `Suspicious missed recalls` column. 

- For model **gpt-3.5-turbo**, we compared the results of different prompts:

| Prompt                | Generated Test Cases                                         | Suspicious missed recalls                                    | Shops Involved | Confirmed missed recalls | Confirmed Shops Involved | False positive |
| --------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | -------------- | ------------------------ | ------------------------ | -------------- |
| Chain of Thought(cot) | [3724](https://github.com/xieeryihe/lDetector/blob/main/data/cases/chatgpt3.5-cot.xlsx) | [47](https://github.com/xieeryihe/lDetector/blob/main/data/final/final-chatgpt3.5-cot.xlsx) | 33             | 46                       | 33                       | 1              |
| few-shot              | [5700](https://github.com/xieeryihe/lDetector/blob/main/data/cases/chatgpt3.5-few-shot.xlsx) | [156](https://github.com/xieeryihe/lDetector/blob/main/data/final/final-chatgpt3.5-few-shot.xlsx) | 98             | 121                      | 76                       | 35             |
| zero-shot             | [4622](https://github.com/xieeryihe/lDetector/blob/main/data/cases/chatgpt3.5-zero-shot.xlsx) | [46](https://github.com/xieeryihe/lDetector/blob/main/data/final/final-chatgpt3.5-zero-shot.xlsx) | 42             | 39                       | 37                       | 7              |

​    

**Without LLM validation step**, a total of 3,724 test cases were generated, and [78 missed recalls](https://github.com/xieeryihe/lDetector/blob/main/data/final/final-no_check_gpt3.5results.xlsx) were found, involving 45 stores. After manual inspection, 71 of the data were accurate (involving 42 stores), and another 7 were false positives.

​    

> For privacy concerns and security of cooperational tools, we remove **the_search_url** and **the_city_id** columns and anonymized **poi_name**, **latitude**, **longitude** and **test_case** columns, while masked data in the following table is only used to show the data format.

​    

### 1.2 File：./data/shop.xlsx

The [shop.xlsx](https://github.com/xieeryihe/lDetector/blob/main/data/shops.xlsx) displays 652 pieces of raw data that we manually obtained from Meituan APP. The sample data format is shown in the table below.

| poi_name                 | latitude  | longitude | city | poi_type |
| ------------------------ | --------- | --------- | ---- | -------- |
| `***餐厅(*里河店)`       | Anonymous | Anonymous | 北京 | 鲁菜     |
| `*****铁锅烀羊肉(*井店)` | Anonymous | Anonymous | 北京 | 中餐馆   |
| ...                      | ...       | ...       | ...  | ...      |

The `poi_name` indicates the full name of the store, and `poi_type` indicates the category of the store.

​    

### 1.3 Folder：./data/cases

For each file in the [cases](https://github.com/xieeryihe/lDetector/tree/main/data/cases) directory, such as `chatglm2-6b.xlsx`, we first use `chatglm2-6b` model to generate related search keywords(`test_case`) based on the raw data in `shops.xlsx`. Then we use the **same** `chatglm2-6b` model to self-check whether these keywords can retrieve the corresponding store. The sample data format of `chatglm2-6b.xlsx` is shown in the table below.

| poi_name           | latitude  | longitude | city | poi_type | test_case          | test_case_judgement |
| ------------------ | --------- | --------- | ---- | -------- | ------------------ | ------------------- |
| `***餐厅(*里河店)` | Anonymous | Anonymous | 北京 | 鲁菜     | `***餐厅(*里河店)` | no                  |
| `***餐厅(*里河店)` | Anonymous | Anonymous | 北京 | 鲁菜     | `***餐厅`          | yes                 |
| `***餐厅(*里河店)` | Anonymous | Anonymous | 北京 | 鲁菜     | `*里河店`          | yes                 |
| ..                 | ...       | ...       | ...  | ...      | ...                | ...                 |

The `test_case` column represents the keywords generated by the model, and the `test_case_judgement` column represents the self-checking results. Item `yes` indicates that the model believes the store can be searched through this keyword and `no` indicates the opposite.

​    

### 1.4 Folder：./data/final

For each file in [final](https://github.com/xieeryihe/lDetector/tree/main/data/final) directory, such as `final-chatGLm2-6b.xlsx`, the sample data format of is shown in the table below.

|      | leak_judgement | equal_leak_exist | accurate_leak | equal_ratio | query_type  | self_leak | searched_shops                                       | poi_name                      | latitude  | longitude | city | poi_type | test_case    | test_case_judgement | human |
| ---- | -------------- | ---------------- | ------------- | ----------- | ----------- | --------- | ---------------------------------------------------- | ----------------------------- | --------- | --------- | ---- | -------- | ------------ | ------------------- | ----- |
| 102  | leak           | partial_leak     | yes           | 0.952380952 | equal_query | yes       | `["***创意汉堡(**港湾店)",  "****创意汉堡(**屯店)"]` | `["***创意汉堡(**港湾店)",  ` | Anonymous | Anonymous | 北京 | 汉堡     | `**创意汉堡` | yes                 | 0     |

The data in the first few columns of the table is mainly used for the judgment in the code, and the specific meaning can be understood in oracle.py. The main concern is the **human** column, indicating the result of human judgment, where **1** indicates that it is a **missed recall** and **0** indicates not.

​    

## 2.code

We test lDetector on both local(gpt-neo-2.7B, etc) and remote models(gpt-3.5-turbo), so we have two versions of code in directories `code/local` and `code/gpt` respectively.

> For the same reasons of privacy and other reasons, we mask part of the prompt, while it doesn't affect understanding.

​    

### 2.1 Folder: ./code/local

| File                                                         | Description                                                  |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| [generate_local.py](https://github.com/xieeryihe/lDetector/blob/main/code/local/generate_local.py) | Use the raw data in `shops.xlsx` to generate the `test_case`. |
| [check_local.py](https://github.com/xieeryihe/lDetector/blob/main/code/local/check_local.py) | Use the `test_case` generated by `generate_local.py` to check if the test_case can be a missed recall. |
| [*_server.py](https://github.com/xieeryihe/lDetector/blob/main/code/local/glm_server.py) | Deploy the model locally so that we can access the local model as we would the remote model. |

​    

### 2.2 Folder: ./code/gpt

| File                                                         | Description                        |
| ------------------------------------------------------------ | ---------------------------------- |
| [generate_gpt.py](https://github.com/xieeryihe/lDetector/blob/main/code/gpt/generate_gpt.py) | Use chatgpt-3.5-turbo to generate. |
| [check_gpt.py](https://github.com/xieeryihe/lDetector/blob/main/code/gpt/check_gpt.py) | Use chatgpt-3.5-turbo to check.    |

​    

### 2.3 File: ./code/oracle.py

The test [oracle code](https://github.com/xieeryihe/lDetector/blob/main/code/oracle.py).  

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

