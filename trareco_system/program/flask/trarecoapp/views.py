from trarecoapp import app
from flask import render_template, request, session, redirect, url_for
from .db import conect
import random
import numpy as np
from collections import defaultdict

# セッションに使用するシークレットキーを設定
app.secret_key = 'a_random_string_with_symbols_12345!@#$%'

@app.route('/')
def index():
    # セッション情報のクリア
    session.pop('selected_images', None)
    session.pop('selection_count', None)
    
    return render_template('trarecoapp/index.html')

# 画像の表示
@app.route('/image')
def show_image():
    select = conect.SELECTDATA()
    columns = 'tourist_id, path'
    table = 'tourist_area'
    all_images = select.select(columns, table)

    # セッションに保存された画像を除外
    if 'selected_images' in session:
        all_images = [img for img in all_images if str(img[0]) not in session['selected_images']]

    selected_image = random.sample(all_images, 9) #画像枚数
    image_data = [{'id': img[0], 'path': img[1]} for img in selected_image]

    return render_template('trarecoapp/show_image.html', images=image_data)

    # images = select.select(columns, table)
    # selected_image = random.sample(images, 9) #画像枚数
    # # 画像のIDとパスを分離
    # image_data = [{'id': img[0], 'path': img[1]} for img in selected_image]
    # return render_template('trarecoapp/show_image.html', images=image_data)


#　選択された画像のIDをセッションに保存
@app.route('/submit_selection_save', methods=['POST'])
def submit_selection_save():
    selected_images = request.form.getlist('image')
    if 'selected_images' not in session:
        session['selected_images'] = selected_images
    else:
        session['selected_images'].extend(selected_images)
    
    # 選択回数をカウント
    if 'selection_count' not in session:
        session['selection_count'] = 1
    else:
        session['selection_count'] += 1

    # デバッグ用にセッション情報を出力
    print(f"選択回数: {session['selection_count']}")

    # 3回選択したらsubmit_selectionにリダイレクト
    if session['selection_count'] >= 3:
        # デバッグメッセージで選択された画像IDを全て出力
        print(f"選択された画像ID: {session['selected_images']}")
        # POSTリクエストを送信
        return '''
        <form id="redirectForm" method="POST" action="/submit_selection">
            <input type="hidden" name="redirect" value="true">
        </form>
        <script type="text/javascript">
            document.getElementById("redirectForm").submit();
        </script>
        '''
    else:
        return redirect(url_for('show_image'))




@app.route('/submit_selection', methods=['GET', 'POST'])
def submit_selection():
    if request.method == 'POST':
        # 選択した画像の色彩を抽出
        selected_image_ids = request.form.getlist('image')
        print(f"selected_image_ids: {selected_image_ids}")  # デバッグ用出力

        color_lists = []  # 入力ベクトル

        select = conect.SELECTDATA()
        columns = '*'
        table = 'colorhistgram'
        for id in selected_image_ids:
            where = f'tourist_id = {id}'
            colors = select.select(columns, table, where)
            colors = colors[0][1:]
            color_lists.append(colors)

        # 感性と色彩の対応表を取得
        columns = '*'
        table = 'color2imp'
        col2imp = select.select(columns, table)  # 感性ベクトル

        print('color_list', color_lists)
        print('col2imp', col2imp)

        total_scores = {}
        for color_list in color_lists:
            for mood, score in calculate_similarity(color_list, col2imp):
                if mood not in total_scores:
                    total_scores[mood] = 0
                total_scores[mood] += score

        # 総類似度ランキング
        sorted_total_scores = sorted(total_scores.items(), key=lambda x: x[1], reverse=True)

        print("最終的な類似度ランキング:")
        for mood, score in sorted_total_scores:
            print(f"{mood}: {score}")

        recommend_spots = recommend_spot(sorted_total_scores)
        print(recommend_spots)

        return render_template('trarecoapp/result.html', ranking=sorted_total_scores, recomend=recommend_spots)
    else:
        return redirect(url_for('index'))
    
def recommend_spot(sorted_total_scores):
    # レコメンド観光地を取得
    select = conect.SELECTDATA()
    columns = '*'
    table = 'return_tourist_area'  # 正しいテーブル名を使用
    tourist_spots = select.select(columns, table)

    # 類似度計算
    similarity_scores = {}
    for mood, score in sorted_total_scores:
        for tourist_id, tourist_info in tourist_spots:
            if tourist_id not in similarity_scores:
                similarity_scores[tourist_id] = 0
            similarity_scores[tourist_id] += score

    # 最終ランキングの生成
    sorted_scores = sorted(similarity_scores.items(), key=lambda item: item[1], reverse=True)

    # ランキング結果をリスト形式で作成
    ranking_results = []
    for tourist_id, score in sorted_scores:
        spot_info = next((spot for spot in tourist_spots if spot[0] == tourist_id), None)
        if spot_info is not None:
            spot_name = spot_info[2]
            image_path = spot_info[1]
            ranking_results.append([spot_name, image_path, score])
        else:
            print(f"No tourist spot found for tourist_id: {tourist_id}")

    # デバッグ用出力
    print(f"ランキング結果: {ranking_results}")

    return ranking_results

def calculate_similarity(input_vector, mood_vectors):
    # 入力ベクトルのNumPy配列
    input_array = np.array(input_vector)

    # 結果を保存するリスト
    similarity_scores = []

    # 各感性ベクトルとの内積を計算
    for mood_vector in mood_vectors:
        mood_id, mood_name, *mood_values = mood_vector
        mood_array = np.array(mood_values)
        similarity = np.dot(input_array, mood_array)
        similarity_scores.append((mood_name, similarity))
    return similarity_scores

'''
@app.route('/submit_selection', methods=['GET', 'POST'])
def submit_selection():
    if request.method == 'POST' or 'selected_images' in session:
        # 選択した画像の色彩を抽出
        selected_image_ids = session.get('selected_images', [])
        print(f"selected_image_ids: {selected_image_ids}")  # デバッグ用出力

        color_lists = get_color_lists(selected_image_ids)
        print(f"color_lists: {color_lists}")  # デバッグ用出力

        sensibility_scores = get_sensibility_scores(color_lists)

        # 類似度計算
        user_vectors = list(zip(sensibility_scores.keys(), sensibility_scores.values()))
        print(f"user_vectors: {user_vectors}")  # デバッグ用出力

        # 推薦結果を取得
        ranking_results = recommend_spot(user_vectors)

        return render_template('trarecoapp/result.html', recommended_spots=ranking_results)
    else:
        return redirect(url_for('index'))

def recommend_spot(user_vectors):
    # レコメンド観光地を取得
    select = conect.SELECTDATA()
    columns = '*'
    table = 'return_tourist_area'  # 正しいテーブル名を使用
    tourist_spots = select.select(columns, table)

    # レコメンド観光地の色彩を取得
    columns = '*'
    table = 'colorhistgram'
    tourist_colors = select.select(columns, table)

    # 感性と色彩のスコア計算
    sensibility_scores = get_sensibility_scores(tourist_colors)

    # 類似度計算
    similarity_scores = {}
    for tourist_id, scores in sensibility_scores.items():
        similarity = 0
        for sensibility, user_score in user_vectors:
            if isinstance(scores, dict):
                similarity += user_score * scores.get(sensibility, 0)
            else:
                similarity += user_score * scores
        similarity_scores[tourist_id] = similarity

        # デバッグ用出力
        print(f"観光地ID: {tourist_id}, 類似度スコア: {similarity}")

    # 最終ランキングの生成
    sorted_scores = sorted(similarity_scores.items(), key=lambda item: item[1], reverse=True)

    # ランキング結果をリスト形式で作成
    ranking_results = []
    for tourist_id, score in sorted_scores:
        spot_info = next((spot for spot in tourist_spots if spot[0] == tourist_id), None)
        if spot_info is not None:
            spot_name = spot_info[2]
            image_path = spot_info[1]
            ranking_results.append([spot_name, image_path, score])
        else:
            print(f"No tourist spot found for tourist_id: {tourist_id}")

    # デバッグ用出力
    print(f"ランキング結果: {ranking_results}")

    return ranking_results

# 内積計算とソートを行う関数
def calculate_similarity(input_vector, mood_vectors):
    # 入力ベクトルのNumPy配列
    input_array = np.array(input_vector)

    # 結果を保存するリスト
    similarity_scores = []

    # 各感性ベクトルとの内積を計算
    for mood_vector in mood_vectors:
        mood_id, mood_name, *mood_values = mood_vector
        mood_array = np.array(mood_values)
        similarity = np.dot(input_array, mood_array)
        similarity_scores.append((mood_name, similarity))
    return similarity_scores

# 画像の色彩データを取得
def get_color_lists(selected_image_ids):
    color_lists = []  # 入力ベクトル
    select = conect.SELECTDATA()
    columns = '*'
    table = 'colorhistgram'
    for id in selected_image_ids:
        where = f'tourist_id = {id}'
        colors = select.select(columns, table, where)
        print(f"colors for tourist_id {id}: {colors}")  # デバッグ用出力
        if colors:
            colors = colors[0][1:]
            color_lists.append(colors)
        else:
            print(f"No colors found for tourist_id: {id}")  # デバッグ用出力
    return color_lists

# 画像と感性のスコアを計算
def get_sensibility_scores(color_lists):
    select = conect.SELECTDATA()
    columns = '*'
    table = 'color2imp'
    sensibility_weights = select.select(columns, table)

    sensibility_scores = defaultdict(dict)
    for colors in color_lists:
        for sensibility in sensibility_weights:
            sensibility_name = sensibility[1]
            weights = sensibility[2:]
            score = sum(c * w for c, w in zip(colors, weights))
            sensibility_scores[sensibility_name] = score

    print(f"sensibility_scores: {sensibility_scores}")  # デバッグ用出力
    return sensibility_scores
'''

'''
# 選択された画像IDから感性を推定し、観光地を推薦
@app.route('/submit_selection', methods=['GET','POST'])
def submit_selection():

    # 選択した画像の色彩を抽出
    selected_image_ids = request.form.getlist('image')
    print(f"selected_image_ids: {selected_image_ids}")  # デバッグ用出力

    color_lists = [] # 入力ベクトル

    select = conect.SELECTDATA()
    columns = '*'
    table = 'colorhistgram'
    for id in selected_image_ids:
        where = f'tourist_id = {id}'
        colors = select.select(columns, table, where)
        colors = colors[0][1:]
        color_lists.append(colors)

    # 感性と色彩の対応表を取得
    select = conect.SELECTDATA()
    columns = '*'
    table = 'color2imp'
    col2imp = select.select(columns, table) # 感性ベクトル

    
    
    
    print('color_list', color_lists)
    print('col2imp', col2imp)

    total_scores = {}
    for color_list in color_lists:
        for mood, score in calculate_similarity(color_list, col2imp):
            if mood not in total_scores:
                total_scores[mood] = 0
            total_scores[mood] += score

    # 総類似度ランキング
    sorted_total_scores = sorted(total_scores.items(), key=lambda x: x[1], reverse=True)

    print("最終的な類似度ランキング:")
    for mood, score in sorted_total_scores:
        print(f"{mood}: {score}")

    
    recommend_spots = recommend_spot(sorted_total_scores)
    print(recommend_spots)


    return render_template('trarecoapp/ranking.html', ranking=sorted_total_scores, recomend=recommend_spots)
'''