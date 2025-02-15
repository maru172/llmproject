# 캡셔닝 데이터 베이스 생성
import requests
from PIL import Image
from transformers import AutoProcessor, AutoModelForImageTextToText

processor = AutoProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
model = AutoModelForImageTextToText.from_pretrained("Salesforce/blip-image-captioning-large")


class Captioning:
    # 이미지 캡셔닝 수행 함수
    def generate_caption(image_url):
        try:
            image = Image.open(requests.get(image_url, stream=True).raw)  # 이미지 다운로드
            # prompt = "Describe the image briefly. If a person is present, use 'a man', 'a woman', or 'they' instead of names."
            prompt = "Describe the image briefly."
            # 프롬프트와 이미지를 입력으로 합치기
            inputs = processor(images=image,  return_tensors="pt")  # 모델 입력 형식으로 변환
            outputs = model.generate(**inputs, max_new_tokens=50)  # 이미지 캡셔닝 수행
            caption = processor.decode(outputs[0], skip_special_tokens=True)  # 캡션 디코딩
            return caption
        except requests.exceptions.RequestException as e:
            print(f"이미지 다운로드 오류: {e}")
            return None
        except Exception as e:
            print(f"이미지 캡셔닝 실패: {e}")
            return None

# img_url = "https://s.yimg.com/ny/api/res/1.2/QahBSopgBtAC5DedbV4DAQ--/YXBwaWQ9aGlnaGxhbmRlcjt3PTEyNDI7aD02OTk7Y2Y9d2VicA--/https://media.zenfs.com/en/thedailybeast.com/8c097e7ef0023d7f32afbfede04c6caf"
# generated_caption = generate_caption(img_url)  # 이미지 캡셔닝 수행   
# print(generated_caption)