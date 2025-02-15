import pandas as pd
import time

# 엑셀 파일 경로
US_file_path = 'C:/Users/user/OneDrive/Desktop/llmproject2/US_news_data.xlsx'
Politics_file_path = 'C:/Users/user/OneDrive/Desktop/llmproject2/Politics_news_data.xlsx'
World_file_path = 'C:/Users/user/OneDrive/Desktop/llmproject2/World_news_data.xlsx'
Bug_file_path = 'C:/Users/user/OneDrive/Desktop/llmproject2/Bug_news_data.xlsx'

class excel:
    # 데이터 저장 함수
    def US_excel_setup():
        # 엑셀 파일이 없으면 새로 생성
        try:
            df = pd.read_excel(US_file_path, sheet_name="US",engine='openpyxl')
        except FileNotFoundError:
            # 엑셀 파일이 없을 경우 빈 DataFrame 생성
            df = pd.DataFrame(columns=['url', 'press', 'title', 'author', 'date_time', 'caption', "captionURL" , 'original_text', 'summary'])  # 열 이름 설정
            
        return df
    def Politics_excel_setup():
        # 엑셀 파일이 없으면 새로 생성
        try:
            df = pd.read_excel(Politics_file_path, sheet_name="Politics",engine='openpyxl')
        except FileNotFoundError:
            # 엑셀 파일이 없을 경우 빈 DataFrame 생성
            df = pd.DataFrame(columns=['url', 'press', 'title', 'author', 'date_time', 'caption', "captionURL" , 'original_text', 'summary'])  # 열 이름 설정
            
        return df
    def World_excel_setup():
        # 엑셀 파일이 없으면 새로 생성
        try:
            df = pd.read_excel(World_file_path, sheet_name="World",engine='openpyxl')
        except FileNotFoundError:
            # 엑셀 파일이 없을 경우 빈 DataFrame 생성
            df = pd.DataFrame(columns=['url', 'press', 'title', 'author', 'date_time', 'caption', "captionURL" , 'original_text', 'summary'])  # 열 이름 설정
            
        return df

    
    
    def Bug_excel_setup():
        # 엑셀 파일이 없으면 새로 생성
        try:
            df = pd.read_excel(Bug_file_path, sheet_name="Bug",engine='openpyxl')
        except FileNotFoundError:
            # 엑셀 파일이 없을 경우 빈 DataFrame 생성
            df = pd.DataFrame(columns=['url'])  # 열 이름 설정
            
        return df
        
    def US_excel_operation(df, url, press, title, author, date_time, caption, original_text, summary, captionURL):
        # 새로운 데이터 생성
        new_data = {'url': f'{url}', 'press': f'{press}', 'title': f'{title}','author': f'{author}' ,
                    'date_time': f'{date_time}' ,'caption': f'{caption}', 'captionURL': f'{captionURL}', 'original_text': f'{original_text}', 'summary': f'{summary}'}

        # 가장 밑 행의 인덱스 찾기
        last_index = len(df)

        # 새로운 데이터 추가
        df.loc[last_index] = new_data

        # 수정된 데이터프레임을 엑셀 파일에 저장
        df.to_excel(US_file_path, index=False, sheet_name="US", engine='openpyxl')
    
    def Politics_excel_operation(df, url, press, title, author, date_time, caption, original_text, summary, captionURL):
        # 새로운 데이터 생성
        new_data = {'url': f'{url}', 'press': f'{press}', 'title': f'{title}','author': f'{author}' ,
                    'date_time': f'{date_time}' ,'caption': f'{caption}', 'captionURL': f'{captionURL}', 'original': f'{original_text}','summary': f'{summary}'}

        # 가장 밑 행의 인덱스 찾기
        last_index = len(df)

        # 새로운 데이터 추가
        df.loc[last_index] = new_data

        # 수정된 데이터프레임을 엑셀 파일에 저장
        df.to_excel(Politics_file_path, index=False, sheet_name="Politics", engine='openpyxl')
        
    def World_excel_operation(df, url, press, title, author, date_time, caption, original_text, summary, captionURL):
        # 새로운 데이터 생성
        new_data = {'url': f'{url}', 'press': f'{press}', 'title': f'{title}','author': f'{author}' ,
                    'date_time': f'{date_time}' ,'caption': f'{caption}','captionURL': f'{captionURL}', 'original': f'{original_text}','summary': f'{summary}'}

        # 가장 밑 행의 인덱스 찾기
        last_index = len(df)

        # 새로운 데이터 추가
        df.loc[last_index] = new_data

        # 수정된 데이터프레임을 엑셀 파일에 저장
        df.to_excel(World_file_path, index=False, sheet_name="World", engine='openpyxl')
        
    def Bug_excel_operation(df, url, err):
        # 새로운 데이터 생성
        new_data = {'url': f'{url}', 'err': f'{err}'}

        # 가장 밑 행의 인덱스 찾기
        last_index = len(df)

        # 새로운 데이터 추가
        df.loc[last_index] = new_data

        # 수정된 데이터프레임을 엑셀 파일에 저장
        df.to_excel(Bug_file_path, index=False, sheet_name="Bug", engine='openpyxl')
        
    def save_to_excel(df, url, press, title, author, date_time, caption, original_text, summary, file_path, sheet_name):
        """
        엑셀 파일에 데이터를 추가하는 범용 함수

        Args:
            df: pandas DataFrame (엑셀에 저장할 데이터프레임)
            url, press, title, author, date_time, caption, original_text, summary: 저장할 데이터
            file_path: 엑셀 파일 경로
            sheet_name: 엑셀 시트 이름
        """
        # 새로운 데이터 생성
        new_data = {'url': f'{url}', 'press': f'{press}', 'title': f'{title}', 'author': f'{author}',
                    'date_time': f'{date_time}', 'caption': f'{caption}', 'original_text': f'{original_text}', 'summary': f'{summary}'}

        # 가장 밑 행의 인덱스 찾기
        last_index = len(df)

        # 새로운 데이터 추가
        df.loc[last_index] = new_data

        # 수정된 데이터프레임을 엑셀 파일에 저장
        df.to_excel(file_path, index=False, sheet_name=sheet_name, engine='openpyxl')

