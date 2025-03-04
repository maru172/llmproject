# 캡셔닝 데이터베이스 생성
import requests
from PIL import Image
from transformers import AutoProcessor, AutoModelForImageTextToText

# 모델 및 프로세서 로드
processor = AutoProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
model = AutoModelForImageTextToText.from_pretrained("Salesforce/blip-image-captioning-large")

class Captioning:
    @staticmethod
    def generate_caption(image_url):
        """이미지 URL을 입력받아 캡션을 생성하는 함수"""
        try:
            image = Image.open(requests.get(image_url, stream=True).raw)  # 이미지 다운로드
            inputs = processor(images=image, return_tensors="pt")  # 모델 입력 변환
            outputs = model.generate(**inputs, max_new_tokens=50)  # 캡셔닝 수행
            caption = processor.decode(outputs[0], skip_special_tokens=True)  # 캡션 디코딩
            return caption
        except requests.exceptions.RequestException as e:
            print(f"이미지 다운로드 오류: {e}")
        except Exception as e:
            print(f"이미지 캡셔닝 실패: {e}")
        return None
