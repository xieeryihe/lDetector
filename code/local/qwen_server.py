import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, AutoModel
from transformers.generation.utils import GenerationConfig
from fastapi import FastAPI, Request
import uvicorn, json, datetime

app = FastAPI()


@app.post("/")
async def create_item(request: Request):
    global model, tokenizer
    json_post_raw = await request.json()
    json_post = json.dumps(json_post_raw)
    json_post_list = json.loads(json_post)
    prompt = json_post_list.get('prompt')
    response, history = model.chat(tokenizer, prompt, history=None)
    # print(response)
    now = datetime.datetime.now()
    time = now.strftime("%Y-%m-%d %H:%M:%S")
    answer = {
        "response": response,
        "status": 200,
        "time": time
    }
    log = "[" + time + "] " + '", prompt:"' + prompt + '", response:"' + repr(response) + '"'
    print(log)
    torch.cuda.empty_cache()
    return answer


if __name__ == '__main__':
    model_path = "/path/Qwen-14B-Chat-Int4"
    print("模型："+ model_path)
    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(model_path, device_map="auto", trust_remote_code=True).eval()
    uvicorn.run(app, host='0.0.0.0', port=8000, workers=1)