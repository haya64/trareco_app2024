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

    # デバッグ用メッセージを出力
    print("=== 新しいセッションがスタートしました ===")
    
    return render_template('trarecoapp/index.html')

# 画像の表示
@app.route('/image')
def show_image():
    select = conect.SELECTDATA()
    columns = 'tourist_id, path'
    table = 'tourist_area'
    all_images = select.select(columns, table)

    if 'selected_images' in session:
        # 選択済み画像を除外
        all_images = [img for img in all_images if str(img[0]) not in session['selected_images']]

    # エラー処理: 残り画像が9枚未満の場合
    if len(all_images) < 9:
        print("画像が不足しています")
        return "エラー: 利用可能な画像が不足しています", 500

    # ランダムに9枚選択
    selected_image = random.sample(all_images, 9)
    image_data = [{'id': img[0], 'path': img[1]} for img in selected_image]

    return render_template('trarecoapp/show_image.html', images=image_data)


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
    if request.method == 'POST' or 'selected_images' in session:
        # セッションまたはリクエストから選択された画像のIDを取得
        selected_image_ids = session.get('selected_images', [])
        if not selected_image_ids:
            selected_image_ids = request.form.getlist('image')
        
        if not selected_image_ids:
            print("No images selected")
            return redirect(url_for('index'))
        
        print(f"selected_image_ids: {selected_image_ids}")  # デバッグ用出力

        # SELECTDATA インスタンスを作成
        select = conect.SELECTDATA()

        try:
            # 混雑度の平均値を計算して保存
            average_crowding = calculate_average_crowding(selected_image_ids, select)
            session['average_crowding'] = average_crowding
            print(f"最終セッション内の平均混雑度: {average_crowding}")

            # 天気を判定して保存
            weather_id = determine_weather(selected_image_ids, select)
            session['weather_id'] = weather_id
            print(f"判定された天気ID: {weather_id}")

            # 時間帯を判定
            timezone_id = determine_timezone(selected_image_ids, select)
            session['timezone_id'] = timezone_id
            print(f"判定された時間帯ID: {timezone_id}")
            
            # 色彩ヒストグラムのデータを取得
            color_lists = []
            for image_id in selected_image_ids:
                where = f'tourist_id = {image_id}'
                colors = select.select('*', 'colorhistgram', where)
                if colors:
                    color_lists.append(colors[0][1:])  # ID列を除く
                else:
                    print(f"No colors found for tourist_id: {image_id}")

            # 総合色彩ヒストグラムを生成
            total_histogram = [sum(color) for color in zip(*color_lists)]
            print(f"総合ヒストグラム: {total_histogram}")

            # 正規化
            total_pixels = sum(total_histogram)
            normalized_histogram = [
                value / total_pixels for value in total_histogram
            ] if total_pixels > 0 else total_histogram
            print(f"正規化されたヒストグラム: {normalized_histogram}")

            # 感性と色彩の対応表を取得
            col2imp = select.select('*', 'color2imp')
            print(f"感性と色彩の対応表: {col2imp}")

            # 感性スコアの計算
            mood_scores = calculate_color_to_mood_similarity(normalized_histogram, col2imp)
            sorted_total_scores = sorted(mood_scores.items(), key=lambda x: x[1], reverse=True)
            print("最終的な感性ランキング:")
            for mood, score in sorted_total_scores:
                print(f"{mood}: {score}")

            # 推薦観光地を取得
            recommend_spots = recommend_spot(sorted_total_scores)
            print(f"推薦観光地: {recommend_spots}")

            return render_template('trarecoapp/result.html', ranking=sorted_total_scores, recomend=recommend_spots)

        finally:
            # SELECTDATA の接続をクローズ
            select.close()

    else:
        return redirect(url_for('index'))


# 観光地の推薦関数
def recommend_spot(sorted_total_scores):
    """
    観光地の推薦リストを作成

    Parameters:
        sorted_total_scores (list): ユーザーの感性ベクトルランキング。

    Returns:
        list: 推薦観光地のランキング結果。
    """
    # 必要な観光地情報を取得
    select = conect.SELECTDATA()
    try:
        # 観光地情報を取得
        columns = 'r_tourist_id, r_path, r_area_name, r_longitude, r_latitude, r_season_id, r_timezone_id, r_category_id'
        table = 'return_tourist_area'
        tourist_spots = select.select(columns, table)

        if not tourist_spots:
            print("No tourist spots found in the database.")
            return []

        print(f"tourist_spots: {tourist_spots}")  # デバッグ用出力

        # 観光地情報を辞書形式に変換（キーはr_tourist_id）
        tourist_dict = {spot[0]: spot for spot in tourist_spots}

        # 色彩データを一括取得
        color_histogram_data = select.select('*', 'return_colorhistgram')
        color_dict = {row[0]: row[1:] for row in color_histogram_data}

        print(f"color_histogram_data: {color_dict}")  # デバッグ用

        # 感性ベクトルを取得
        mood_vectors = select.select('*', 'color2imp')

        # ユーザーの感性ベクトル
        user_mood_vector = {mood: score for mood, score in sorted_total_scores}

        # 各観光地の感性ベクトルと類似度を計算
        similarity_scores = {}
        for tourist_id, spot_info in tourist_dict.items():
            # 色彩データを取得
            if tourist_id not in color_dict:
                print(f"No color data found for r_tourist_id: {tourist_id}")
                continue

            color_vector = color_dict[tourist_id]

            # 色彩データから感性ベクトルを生成
            spot_mood_vector = calculate_color_to_mood_similarity(color_vector, mood_vectors)

            # ユーザー感性ベクトルとの類似度を計算
            spot_name = spot_info[2]
            similarity_score = calculate_user_to_spot_similarity(user_mood_vector, spot_mood_vector, spot_name)
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

    finally:
        # データベース接続のクローズ
        select.close()


def calculate_color_to_mood_similarity(color_vector, mood_vectors):
    """
    総合色彩ヒストグラムと色彩と感性語の対応行列を用いて感性ベクトルを生成し、スコアを1以下に正規化。

    Parameters:
        color_vector (list): 正規化された総合色彩ヒストグラム Hₛ。
        mood_vectors (list): 感性データのベクトルリスト [(id, name, *values)]。

    Returns:
        dict: 感性名とスコアの辞書（スコアは1以下に正規化）。
    """
    # 感性スコアを格納する辞書
    mood_scores = {}

    # ヒストグラムを numpy 配列に変換
    histogram = np.array(color_vector)

    # 感性スコアの計算
    for mood_vector in mood_vectors:
        mood_id, mood_name, *mood_weights = mood_vector
        weights = np.array(mood_weights)

        # cₙ = Σ Hₛ(m) * Aₘₙ
        mood_score = np.dot(histogram, weights)

        # 感性名をキーにスコアを格納
        mood_scores[mood_name] = mood_score

    # スコアを1以下に正規化
    total_score = sum(mood_scores.values())
    if total_score > 0:
        mood_scores = {k: v / total_score for k, v in mood_scores.items()}

    return mood_scores


# ユーザー感性ベクトルと観光地感性ベクトルの類似度を測る関数
def calculate_user_to_spot_similarity(user_mood_vector, spot_mood_vector, spot_name='unknown spot'):
    """
    ユーザー感性ベクトルと観光地感性ベクトルの類似度をユークリッド距離で計算。

    Parameters:
        user_mood_vector (dict): ユーザー感性ベクトル（感性名とスコアの辞書）。
        spot_mood_vector (dict): 観光地感性ベクトル（感性名とスコアの辞書）。
        spot_name (str): 観光地名（デバッグ用）。

    Returns:
        float: 類似度スコア（ユークリッド距離を使用）。
    """
    # 共通の感性を使用してベクトル化
    common_keys = set(user_mood_vector.keys()) & set(spot_mood_vector.keys())
    user_array = np.array([user_mood_vector[key] for key in common_keys])
    spot_array = np.array([spot_mood_vector[key] for key in common_keys])

    # デバッグ用出力
    print("=== デバッグ: 感性ベクトル比較 ===")
    print(f"観光地: {spot_name}")
    print(f"ユーザー感性ベクトル (共通): {user_array}")
    print(f"観光地感性ベクトル (共通): {spot_array}")
    print(f"共通の感性キー: {common_keys}")

    # ユークリッド距離の計算
    distance = np.sqrt(np.sum((user_array - spot_array) ** 2))

    # 類似度として距離を返す
    similarity = -distance  # 小さい距離を大きいスコアとして扱う

    # デバッグ用出力
    print(f"計算されたユークリッド距離: {distance}")
    print(f"類似度スコア (負の距離): {similarity}")
    print("================================")

    return similarity


def calculate_average_crowding(selected_image_ids, db_connection):
    """
    選択された画像の混雑度平均を計算し保存。

    Parameters:
        selected_image_ids (list): ユーザーが選択した画像のIDリスト。
        db_connection (object): データベース接続オブジェクト。

    Returns:
        float: 選択された画像の平均混雑度。
    """
    total_crowding = 0.0
    for image_id in selected_image_ids:
        # データベースから混雑度を取得
        where = f'tourist_id = {image_id}'  # 修正
        columns = 'crowding'
        table = 'tourist_area'
        result = db_connection.select(columns, table, where)

        if result and result[0][0] is not None:
            total_crowding += float(result[0][0])  # 混雑度を累積

    # 平均混雑度を計算
    average_crowding = total_crowding / len(selected_image_ids) if selected_image_ids else 0.0
    print(f"計算された平均混雑度: {average_crowding}")
    return average_crowding


def determine_weather(selected_image_ids, db_connection):
    """
    選択された画像の天気を判定。

    Parameters:
        selected_image_ids (list): ユーザーが選択した画像のIDリスト。
        db_connection (object): データベース接続オブジェクト。

    Returns:
        int: 判定された天気ID。または、条件を満たさない場合は None。
    """
    ids = ','.join(map(str, selected_image_ids))
    query = f"""
        SELECT weather, COUNT(*)
        FROM tourist_area
        WHERE tourist_id IN ({ids})
        GROUP BY weather
    """
    result = db_connection.select_raw(query)

    weather_counts = {row[0]: row[1] for row in result}
    total_images = sum(weather_counts.values())

    print(f"天気の出現数: {weather_counts}, 総画像数: {total_images}")  # デバッグ用

    threshold = 0.5
    for weather_id, count in weather_counts.items():
        if count / total_images > threshold:
            print(f"最終的に判定された天気ID: {weather_id}")
            return weather_id

    print("最終的に判定された天気ID: None")
    return None



def determine_timezone(selected_image_ids, db_connection):
    """
    選択された画像の時間帯を判定。

    Parameters:
        selected_image_ids (list): ユーザーが選択した画像のIDリスト。
        db_connection (object): データベース接続オブジェクト。

    Returns:
        int: 判定された時間帯ID。または、条件を満たさない場合は None。
    """
    ids = ','.join(map(str, selected_image_ids))
    query = f"""
        SELECT timezone_id, COUNT(*)
        FROM tourist_area
        WHERE tourist_id IN ({ids})
        GROUP BY timezone_id
    """
    result = db_connection.select_raw(query)

    timezone_counts = {row[0]: row[1] for row in result}
    total_images = sum(timezone_counts.values())

    print(f"時間帯の出現数: {timezone_counts}, 総画像数: {total_images}")  # デバッグ用

    threshold = 0.75
    for timezone_id, count in timezone_counts.items():
        if count / total_images > threshold:
            print(f"最終的に判定された時間帯ID: {timezone_id}")
            return timezone_id

    print("最終的に判定された時間帯ID: None")
    return None