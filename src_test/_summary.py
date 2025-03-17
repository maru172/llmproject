from transformers import BartForConditionalGeneration, BartTokenizer
import torch

# 모델을 GPU로 이동
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model_name = "facebook/bart-large-cnn"
model = BartForConditionalGeneration.from_pretrained(model_name).to(device)
tokenizer = BartTokenizer.from_pretrained(model_name)

class Summary:
  def summary_Short(text):
    print("-- Short Type Version --")
    # 텍스트를 토큰화
    inputs = tokenizer(text, max_length=1024, return_tensors='pt', truncation=True)
    # 요약 생성
    summary_ids = model.generate(inputs['input_ids'].to(device), max_length=512, min_length=20, length_penalty=2.0, num_beams=4, early_stopping=True)
    # 요약된 텍스트 디코딩
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary
   

  def summary_Long(text):
    print("-- Long Type Version --")
    sentence = text.split('.')
    print(sentence)