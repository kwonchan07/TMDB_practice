import os
import requests
from flask import Flask, render_template, request, redirect, url_for, session
from dotenv import load_dotenv

# .env 파일에서 환경변수 로드
load_dotenv()

app = Flask(__name__)
# 세션 사용을 위한 비밀키 설정
app.secret_key = os.getenv("FLASK_SECRET_KEY", "default_secret_key")
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

# 1. 메인 페이지 (영화 검색 및 찜 목록 출력)
@app.route('/')
def index():
    query = request.args.get('query', '')
    movies = []

    if query:
        # TMDB API 호출
        url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={query}&language=ko-KR"
        response = requests.get(url)
        if response.status_code == 200:
            movies = response.json().get('results', [])

    # 세션에서 찜 목록 가져오기 (없으면 빈 리스트)
    wishlist = session.get('wishlist', [])
    
    return render_template('index.html', movies=movies, wishlist=wishlist, query=query)

# 2. 찜 목록 추가 라우트
@app.route('/add_to_wishlist', methods=['POST'])
def add_to_wishlist():
    movie_id = request.form.get('id')
    title = request.form.get('title')
    poster_path = request.form.get('poster_path')

    if 'wishlist' not in session:
        session['wishlist'] = []

    wishlist = session['wishlist']
    
    # 중복 추가 방지
    if not any(item['id'] == movie_id for item in wishlist):
        wishlist.append({
            'id': movie_id,
            'title': title,
            'poster_path': poster_path
        })
        session['wishlist'] = wishlist # 세션 데이터 업데이트 명시
        session.modified = True

    return redirect(url_for('index'))