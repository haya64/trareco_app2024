from trarecoapp import app
from flask import render_template, request, session, redirect, url_for
from flask_session import Session
from .db import conect
import random
import numpy as np
from collections import defaultdict

# セッションに使用するシークレットキーを設定
app.secret_key = 'a_random_string_with_symbols_12345!@#$%'

# セッションの設定
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

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

    print(f"POSTデータ: {request.form}")  # POSTデータを確認
    print(f"選択された画像: {selected_images}")  # デバッグ用
    print(f"セッション: {session}")  # セッション全体を確認


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
        selected_images_html = ''.join(
            f'<input type="hidden" name="image" value="{image}">' for image in session['selected_images']
        )
        return f'''
        <form id="redirectForm" method="POST" action="/submit_selection">
            {selected_images_html}
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

        if not selected_image_ids:
            print("No images selected")
            return redirect(url_for('index'))

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
        # 色彩ベクトルから感性ベクトルを生成し、感性スコアを累積
        for color_list in color_lists:
            mood_scores = calculate_color_to_mood_similarity(color_list, col2imp)
            for mood, score in mood_scores.items():
                if mood not in total_scores:
                    total_scores[mood] = 0
                total_scores[mood] += score

        # 感性ランキング
        sorted_total_scores = sorted(total_scores.items(), key=lambda x: x[1], reverse=True)

        print("最終的な感性ランキング:")
        for mood, score in sorted_total_scores:
            print(f"{mood}: {score}")

        recommend_spots = recommend_spot(sorted_total_scores)
        # print(recommend_spots)

        return render_template('trarecoapp/result.html', ranking=sorted_total_scores, recomend=recommend_spots)
    else:
        return redirect(url_for('index'))
    
# 観光地の推薦関数
def recommend_spot(sorted_total_scores):
    # 必要な観光地情報を取得
    select = conect.SELECTDATA()
    columns = 'r_tourist_id, r_path, r_area_name, r_longitude, r_latitude, r_season_id, r_timezone_id, r_category_id'
    table = 'return_tourist_area'
    tourist_spots = select.select(columns, table)

    print(f"tourist_spots: {tourist_spots}")  # デバッグ用出力

    # 観光地情報を辞書形式に変換（キーはr_tourist_id）
    tourist_dict = {spot[0]: spot for spot in tourist_spots}

    # ユーザーの感性ベクトル
    user_mood_vector = {mood: score for mood, score in sorted_total_scores}

    # 各観光地の感性ベクトルと類似度を計算
    similarity_scores = {}
    for tourist_id, spot_info in tourist_dict.items():
        # 色彩データを取得
        where = f'tourist_id = {tourist_id}'
        columns = '*'
        table = 'colorhistgram'
        color_data = select.select(columns, table, where)

        if not color_data:
            print(f"No color data found for tourist_id: {tourist_id}")
            continue

        # 色彩データを基に観光地の感性ベクトルを生成
        color_vector = color_data[0][1:]  # 色彩データ (最初の列はIDなので除外)
        columns = '*'
        table = 'color2imp'
        mood_vectors = select.select(columns, table)
        spot_mood_vector = calculate_color_to_mood_similarity(color_vector, mood_vectors)

        # ユーザー感性ベクトルとの類似度を計算
        similarity_score = calculate_user_to_spot_similarity(user_mood_vector, spot_mood_vector)
        similarity_scores[tourist_id] = similarity_score

    # 類似度スコアを降順にソート
    sorted_scores = sorted(similarity_scores.items(), key=lambda x: x[1], reverse=True)

    # ランキング結果を作成
    ranking_results = []
    for tourist_id, score in sorted_scores:
        if tourist_id in tourist_dict:
            spot_info = tourist_dict[tourist_id]
            ranking_results.append({
                'id': spot_info[0],
                'name': spot_info[2],
                'image_path': spot_info[1],
                'longitude': spot_info[3],
                'latitude': spot_info[4],
                'score': score
            })

    # ランキング結果のデバッグ出力
    print("ランキング結果（ID、名前、スコア）:")
    for spot in ranking_results:
        print(f"ID: {spot['id']}, 名前: {spot['name']}, スコア: {spot['score']}")
    return ranking_results


# 色彩と感性の関連度を計算する関数
def calculate_color_to_mood_similarity(color_vector, mood_vectors):
    """
    色彩ベクトルと感性ベクトルの関連度を計算。

    Parameters:
        color_vector (list): 色彩データのベクトル。
        mood_vectors (list): 感性データのベクトルリスト [(id, name, *values)]。

    Returns:
        dict: 感性名とスコアの辞書。
    """
    input_array = np.array(color_vector)
    similarity_scores = {}
    for mood_vector in mood_vectors:
        mood_id, mood_name, *mood_values = mood_vector
        mood_array = np.array(mood_values)
        similarity = np.dot(input_array, mood_array)
        similarity_scores[mood_name] = similarity
    return similarity_scores


# ユーザー感性ベクトルと観光地感性ベクトルの類似度を測る関数
def calculate_user_to_spot_similarity(user_mood_vector, spot_mood_vector):
    """
    ユーザー感性ベクトルと観光地感性ベクトルの類似度を計算。

    Parameters:
        user_mood_vector (dict): ユーザー感性ベクトル（感性名とスコアの辞書）。
        spot_mood_vector (dict): 観光地感性ベクトル（感性名とスコアの辞書）。

    Returns:
        float: 類似度スコア（例: コサイン類似度）。
    """
    # 共通の感性を使用してベクトル化
    common_keys = set(user_mood_vector.keys()) & set(spot_mood_vector.keys())
    user_array = np.array([user_mood_vector[key] for key in common_keys])
    spot_array = np.array([spot_mood_vector[key] for key in common_keys])

    # デバッグ用出力
    print("=== デバッグ: 感性ベクトル比較 ===")
    print(f"ユーザー感性ベクトル (共通): {user_array}")
    print(f"観光地感性ベクトル (共通): {spot_array}")
    print(f"共通の感性キー: {common_keys}")

    # コサイン類似度の計算
    norm_user = np.linalg.norm(user_array)
    norm_spot = np.linalg.norm(spot_array)
    if norm_user == 0 or norm_spot == 0:
        return 0.0
    similarity = np.dot(user_array, spot_array) / (norm_user * norm_spot)

    # デバッグ用出力
    print(f"計算された類似度スコア: {similarity}")
    print("================================")

    return similarity

