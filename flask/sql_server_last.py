from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

PER_PAGE = 20  # 한 페이지당 표시할 기사 개수

# DB 파일에 따라 시트 이름을 하드코딩으로 지정하는 딕셔너리 사용
db_to_sheet = {
    '/home/llmproject/Desktop/llmproject/databases/Politics.db': 'Politics',
    '/home/llmproject/Desktop/llmproject/databases/Us.db': 'Us',
    '/home/llmproject/Desktop/llmproject/databases/World.db': 'World',
}

# 데이터베이스에서 기사 제목 가져오기
def get_article_titles_from_db(db_file, offset=0, limit=10):
    """지정된 DB에서 기사 제목을 가져오는 함수"""
    try:
        con = sqlite3.connect(db_file)
        cursor = con.cursor()

        # 테이블 이름을 자동으로 가져오기 위해 조회
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        if not tables:
            return []

        table_name = tables[0][0]  # 첫 번째 테이블 사용 (예: 'politics_articles')

        # 기사 제목을 페이징하여 가져오기
        cursor.execute(f'''
            SELECT id, title FROM {table_name} 
            ORDER BY id DESC 
            LIMIT ? OFFSET ?;
        ''', (limit, offset))

        articles = [{'id': row[0], 'title': row[1]} for row in cursor.fetchall()]
        return articles

    except sqlite3.Error as error:
        print("DB 오류 발생:", error)
        return []
    finally:
        if con:
            con.close()


# 데이터베이스에서 기사 제목 가져오기
def get_article_titles_from_db(db_file, offset=0, limit=10):
    """지정된 DB에서 기사 제목을 가져오는 함수"""
    con = None  # con을 초기화
    try:
        con = sqlite3.connect(db_file)
        cursor = con.cursor()

        # 테이블 이름을 자동으로 가져오기 위해 조회
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        if not tables:
            return []

        table_name = tables[0][0]  # 첫 번째 테이블 사용 (예: 'politics_articles')

        # 기사 제목을 페이징하여 가져오기
        cursor.execute(f'''
            SELECT id, title FROM {table_name} 
            ORDER BY id DESC 
            LIMIT ? OFFSET ?;
        ''', (limit, offset))

        articles = [{'id': row[0], 'title': row[1]} for row in cursor.fetchall()]
        return articles

    except sqlite3.Error as error:
        print("DB 오류 발생:", error)
        return []
    finally:
        if con:
            con.close()  # con이 None이 아니면 close 호출

# 데이터베이스에서 기사 요약 가져오기
def get_article_details_from_db(db_file, article_id):
    sheet_name = db_to_sheet.get(db_file)
    
    if not sheet_name:
        raise ValueError("Invalid DB file selected")

    con = None  # con을 초기화
    try:
        con = sqlite3.connect(db_file)
        cursor = con.cursor()
        
        table_name = f"{sheet_name}_articles"
        cursor.execute(f"""
            SELECT title, press, author, date_time, image_url, original_text, summary, original_caption, generated_caption
            FROM {table_name}
            WHERE id = ?;
        """, (article_id,))
        
        article = cursor.fetchone()
        if article:
            return {
                "title": article[0],
                "press": article[1],
                "author": article[2],
                "date_time": article[3],
                "image_url": article[4],
                "original_text": article[5],
                "summary": article[6],
                "original_caption": article[7],
                "generated_caption": article[8],
            }
        return None
    
    except sqlite3.Error as error:
        print("DB 오류 발생:", error)
        return None
    finally:
        if con:
            con.close()  # con이 None이 아니면 close 호출

# 전체 기사 개수 가져오기
def get_total_articles_from_db(db_file):
    sheet_name = db_to_sheet.get(db_file)
    
    if not sheet_name:
        print(f"Invalid DB file: {db_file}")  # 디버깅: db_file과 sheet_name 확인
        raise ValueError("Invalid DB file selected")
    
    con = None  # con을 초기화
    try:
        con = sqlite3.connect(db_file)
        c = con.cursor()
        table_name = f"{sheet_name}_articles"
        c.execute(f"SELECT COUNT(*) FROM {table_name}")
        total = c.fetchone()[0]
        return total
    except sqlite3.Error as error:
        print(f"Error accessing database: {error}")
        raise
    finally:
        if con:
            con.close()  # con이 None이 아니면 close 호출


@app.route('/')
def home():
    db_file = request.args.get('db_file', '/home/llmproject/Desktop/llmproject/databases/Politics.db')  # 기본 DB
    page = int(request.args.get('page', 1))  # 기본 페이지 1
    offset = (page - 1) * PER_PAGE  # 페이징 처리

    # 수정된 함수 호출
    titles = get_article_titles_from_db(db_file, offset, PER_PAGE)

    # 총 기사 개수 가져오기
    total_articles = get_total_articles_from_db(db_file)
    total_pages = (total_articles + PER_PAGE - 1) // PER_PAGE  # 전체 페이지 수 계산

    return render_template('titles.html', titles=titles, page=page, total_pages=total_pages, db_file=db_file)


@app.route('/article/<int:article_id>')
def article_detail(article_id):
    print(f"Request args: {request.args}")  # GET 파라미터 전체 출력

    db_file = request.args.get('db_file', '/home/llmproject/Desktop/llmproject/databases/Politics.db')  # 기본값 설정

    if db_file not in db_to_sheet:
        print(f"Invalid DB file requested: {db_file}")  # 오류 원인 출력
        return "Invalid database file", 400  # 400 Bad Request 반환
    
    article = get_article_details_from_db(db_file, article_id)
    
    if article:
        return render_template('summary.html', article=article, db_file=db_file)
    else:
        return "Article not found", 404



if __name__ == '__main__':
    app.run(host="0.0.0.0", port="3050", debug=True)  # 외부 포트 포워딩