from transformers import BartForConditionalGeneration, BartTokenizer
import torch

# 모델을 GPU로 이동
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model_name = "facebook/bart-large-cnn"
model = BartForConditionalGeneration.from_pretrained(model_name).to(device)
tokenizer = BartTokenizer.from_pretrained(model_name)

class Summary:
    @staticmethod
    def summary_Short(text):
        """짧은 요약 생성"""
        print("-- Short Type Version --")
        inputs = tokenizer(text, max_length=1024, return_tensors='pt', truncation=True)
        summary_ids = model.generate(
            inputs['input_ids'].to(device), 
            max_length=512, 
            min_length=20, 
            length_penalty=2.0, 
            num_beams=4, 
            early_stopping=True
        )
        return tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    
    @staticmethod
    def summary_Long(text):
        """긴 요약 생성 (현재 미완성)"""
        print("-- Long Type Version --")
        sentences = text.split('.')
        print(sentences)
