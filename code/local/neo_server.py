from fastapi import FastAPI, Request
from transformers import AutoTokenizer, AutoModelForCausalLM
import uvicorn, json, datetime
import torch

DEVICE = "cuda"
DEVICE_ID = "1"
CUDA_DEVICE = f"{DEVICE}:{DEVICE_ID}" if DEVICE_ID else DEVICE

def torch_gc():
    if torch.cuda.is_available():
        with torch.cuda.device(CUDA_DEVICE):
            torch.cuda.empty_cache()
            torch.cuda.ipc_collect()

app = FastAPI()

@app.post("/")
async def create_item(request: Request):
    global model, tokenizer
    json_post_raw = await request.json()
    json_post = json.dumps(json_post_raw)
    json_post_list = json.loads(json_post)
    prompt = json_post_list.get('prompt')
    inputs = tokenizer(prompt, return_tensors="pt").to(DEVICE)
    input_ids = inputs.input_ids
    attention_mask = inputs.attention_mask
    size = input_ids.size()[1]
    outputs = model.generate(input_ids, attention_mask = attention_mask, do_sample = False, num_beams = 1, num_return_sequences = 1, max_length = size + 128)
    prediction = tokenizer.batch_decode(outputs)
    prediction = [pred[len(prompt): ] for pred in prediction]

    now = datetime.datetime.now()
    time = now.strftime("%Y-%m-%d %H:%M:%S")
    answer = {
        "response": prediction,
        "status": 200,
        "time": time
    }
    log = "[" + time + "] " + '", prompt:"' + prompt + '", response:"' + repr(prediction) + '"'
    print(log)
    torch_gc()
    return answer


if __name__ == '__main__':
    model_path = "/path/gpt-neo-2.7B"
    print("model: "+ model_path)
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForCausalLM.from_pretrained(model_path, pad_token_id = tokenizer.eos_token_id).to(DEVICE)
    uvicorn.run(app, host='0.0.0.0', port=8000, workers=1)
