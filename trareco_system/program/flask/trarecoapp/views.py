from trarecoapp import app
from flask import render_template, request, session, redirect, url_for
from flask_session import Session
from .db import conect
import random
import numpy as np
from collections import defaultdict
import math
from urllib.parse import unquote  # 追加



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
            # 選択された画像情報を取得
            selected_images_info = []
            for image_id in selected_image_ids:
                where = f'tourist_id = {image_id}'
                columns = 'tourist_id, path'
                table = 'tourist_area'
                result = select.select(columns, table, where)
                if result:
                    decoded_path = f"images/{unquote(result[0][1])}"  # 'images/'ディレクトリを追加
                    selected_images_info.append({'id': result[0][0], 'path': decoded_path})
                    print(f"選択画像パス: {decoded_path}")  # デバッグ用出力
                else:
                    print(f"No image data found for ID: {image_id}")


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

            # 推薦観光地を取得（修正: average_crowding を渡す）
            recommend_spots = recommend_spot(sorted_total_scores, average_crowding, weather_id, timezone_id)
            print(f"推薦観光地: {recommend_spots}")


            return render_template('trarecoapp/result.html',selected_images=selected_images_info, ranking=sorted_total_scores, recomend=recommend_spots)

        finally:
            # SELECTDATA の接続をクローズ
            select.close()

    else:
        return redirect(url_for('index'))


# 推薦観光地のランキングを生成
def recommend_spot(
    sorted_total_scores,
    average_crowding,
    weather_id,
    timezone_id,
    user_lat=35.681236,  # デフォルト値: 東京駅の緯度
    user_lon=139.767125, # デフォルト値: 東京駅の経度
    speed_kmh=60         # デフォルト値: 60km/h
):
    """
    観光地の推薦リストを作成し、混雑度・天気・時間帯・移動時間を考慮。

    Parameters:
        sorted_total_scores (list): ユーザーの感性ベクトルランキング。
        average_crowding (float): ユーザーが選択した画像の平均混雑度。
        weather_id (int): 判定された天気ID。
        timezone_id (int): 判定された時間帯ID。
        user_lat (float): ユーザーの緯度（デフォルト: 東京駅）。
        user_lon (float): ユーザーの経度（デフォルト: 東京駅）。
        speed_kmh (float): 移動速度（km/h、デフォルト: 60）。

    Returns:
        list: 推薦観光地のランキング結果。
    """
    select = conect.SELECTDATA()
    try:
        # 観光地情報を取得
        columns = 'r_tourist_id, r_path, r_area_name, r_longitude, r_latitude, r_season_id, r_timezone_id, r_category_id, r_crowding, r_weather_id'
        table = 'return_tourist_area'
        tourist_spots = select.select(columns, table)

        if not tourist_spots:
            print("No tourist spots found in the database.")
            return []

        # 観光地情報を辞書形式に変換
        tourist_dict = {spot[0]: spot for spot in tourist_spots}

        # 色彩データを一括取得
        color_histogram_data = select.select('*', 'return_colorhistgram')
        color_dict = {row[0]: row[1:] for row in color_histogram_data}

        # 感性ベクトルを取得
        mood_vectors = select.select('*', 'color2imp')

        # ユーザーの感性ベクトル
        user_mood_vector = {mood: score for mood, score in sorted_total_scores}

        # 各観光地の感性ベクトルと類似度を計算
        similarity_scores = {}
        for tourist_id, spot_info in tourist_dict.items():
            if tourist_id not in color_dict:
                print(f"No color data found for r_tourist_id: {tourist_id}")
                continue

            color_vector = color_dict[tourist_id]
            spot_mood_vector = calculate_color_to_mood_similarity(color_vector, mood_vectors)

            similarity_score = calculate_user_to_spot_similarity(
                user_mood_vector, spot_mood_vector, spot_info[2]
            )
            similarity_scores[tourist_id] = similarity_score

        # 類似度スコアを降順にソート
        sorted_scores = sorted(similarity_scores.items(), key=lambda x: x[1], reverse=True)

        # ランキング結果を作成
        ranking_results = [
            {
                'id': tourist_dict[tourist_id][0],
                'name': tourist_dict[tourist_id][2],
                'image_path': tourist_dict[tourist_id][1] + ('.jpg' if not tourist_dict[tourist_id][1].endswith(('.jpg', '.png', '.jpeg')) else ''),
                'longitude': tourist_dict[tourist_id][3],
                'latitude': tourist_dict[tourist_id][4],
                'crowding': tourist_dict[tourist_id][8],  # 混雑度
                'weather': tourist_dict[tourist_id][9],   # 天気ID
                'timezone': tourist_dict[tourist_id][6], # 時間帯ID
                'score': score
            }
            for tourist_id, score in sorted_scores
        ]

        print(f"ランキング結果: {len(ranking_results)} 件生成")

        # 混雑度による絞り込みを実行
        filtered_results = filter_recommendations_by_crowding(ranking_results, average_crowding)

        # 天気による絞り込みを実行
        filtered_results = filter_recommendations_by_weather(filtered_results, weather_id)

        # 時間帯による絞り込みを実行
        filtered_results = filter_recommendations_by_timezone(filtered_results, timezone_id)

        # 移動時間の計算を実行
        final_results = calculate_travel_time((user_lat, user_lon), filtered_results, speed_kmh)

        # デバッグ用に移動時間を出力
        # デバッグ用に移動時間を出力
        print("=== 絞り込まれた観光地とその詳細情報 ===")
        for spot in final_results:
            print(f"観光地名: {spot['name']}")
            print(f"画像パス: {spot['image_path']}")
            print(f"緯度: {spot['latitude']}, 経度: {spot['longitude']}")
            print(f"混雑度: {spot['crowding']}")
            print(f"天気ID: {spot['weather']}")
            print(f"時間帯ID: {spot['timezone']}")
            print(f"類似度スコア: {spot['score']:.2f}")
            print(f"距離: {spot['distance_km']} km")
            print(f"移動時間: {spot['travel_time_hr']} 時間")
            print("-" * 40)


        return final_results

    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return []



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
    # print("=== デバッグ: 感性ベクトル比較 ===")
    # print(f"観光地: {spot_name}")
    # print(f"ユーザー感性ベクトル (共通): {user_array}")
    # print(f"観光地感性ベクトル (共通): {spot_array}")
    # print(f"共通の感性キー: {common_keys}")

    # ユークリッド距離の計算
    distance = np.sqrt(np.sum((user_array - spot_array) ** 2))

    # 類似度として距離を返す
    similarity = -distance  # 小さい距離を大きいスコアとして扱う

    # デバッグ用出力
    # print(f"計算されたユークリッド距離: {distance}")
    # print(f"類似度スコア (負の距離): {similarity}")
    # print("================================")

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


def filter_recommendations_by_crowding(recommendation_spots, average_crowding):
    """
    混雑度に基づいて推薦観光地を絞り込む。

    Parameters:
        recommendation_spots (list): 推薦観光地情報のリスト（各観光地は辞書形式）。
        average_crowding (float): ユーザーが選択した画像の平均混雑度。

    Returns:
        list: 混雑度条件を満たす推薦観光地リスト。
    """
    Tco = 0.02  # 混雑度の閾値

    # 混雑を許容するかどうかを判定
    allow_crowding = average_crowding > Tco
    print(f"混雑許容判定: {'許容する' if allow_crowding else '許容しない'} (平均混雑度: {average_crowding})")

    filtered_spots = []

    for spot in recommendation_spots:
        crowding = spot.get('crowding', 0.0)  # 推薦観光地の混雑度を取得

        if allow_crowding:
            # 混雑を許容する場合、すべての観光地を含める
            filtered_spots.append(spot)
        else:
            # 混雑を許容しない場合、混雑度が閾値以下の観光地を含める
            if crowding <= Tco:
                filtered_spots.append(spot)

    # デバッグ用出力
    print(f"混雑度絞り込み後の推薦観光地数: {len(filtered_spots)} / {len(recommendation_spots)}")
    return filtered_spots

def filter_recommendations_by_weather(recommendations, weather_id):
    """
    天気条件に基づいて推薦観光地を絞り込む。

    Parameters:
        recommendations (list): 推薦観光地リスト。
        weather_id (int): 判定された天気ID。Noneの場合、絞り込みを行わない。

    Returns:
        list: 絞り込み後の推薦観光地リスト。
    """
    if weather_id is None:
        print("天気条件による絞り込みを行いません（任意の天気）。")
        return recommendations  # 絞り込みなし

    # 絞り込み処理
    filtered = [spot for spot in recommendations if spot['weather'] == weather_id]

    print(f"天気条件（ID: {weather_id}）による絞り込み後の推薦観光地数: {len(filtered)} / {len(recommendations)}")
    return filtered

def filter_recommendations_by_timezone(recommendations, timezone_id):
    """
    時間帯条件に基づいて推薦観光地を絞り込む。

    Parameters:
        recommendations (list): 推薦観光地リスト。
        timezone_id (int): 判定された時間帯ID。Noneの場合、絞り込みを行わない。

    Returns:
        list: 絞り込み後の推薦観光地リスト。
    """
    if timezone_id is None:
        print("時間帯条件による絞り込みを行いません（任意の時間帯）。")
        return recommendations  # 絞り込みなし

    # 絞り込み処理
    filtered = [spot for spot in recommendations if spot['timezone'] == timezone_id]

    print(f"時間帯条件（ID: {timezone_id}）による絞り込み後の推薦観光地数: {len(filtered)} / {len(recommendations)}")
    return filtered

# 移動時間計算
def calculate_travel_time(user_location, tourist_spots, speed_kmh=60):
    """
    観光地との移動時間を計算。

    Parameters:
        user_location (tuple): ユーザーの現在地 (latitude, longitude)。
        tourist_spots (list of dict): 観光地情報のリスト。各観光地は辞書形式で含む (id, name, latitude, longitude, ...)。
        speed_kmh (float): 移動速度 (km/h)。

    Returns:
        list: 観光地情報に移動時間と距離を追加したリスト。
    """
    R = 6371  # 地球の半径 (km)
    user_lat, user_lon = map(float, user_location)  # 緯度・経度をfloat型に変換
    user_lat_rad = math.radians(user_lat)
    user_lon_rad = math.radians(user_lon)

    results = []
    for spot in tourist_spots:
        try:
            # 緯度・経度の取得と変換
            spot_lat = float(spot['latitude'])
            spot_lon = float(spot['longitude'])
            spot_lat_rad = math.radians(spot_lat)
            spot_lon_rad = math.radians(spot_lon)

            # 緯度・経度の差を計算
            delta_lat = spot_lat_rad - user_lat_rad
            delta_lon = spot_lon_rad - user_lon_rad

            # 大円距離を計算
            a = (math.sin(delta_lat / 2) ** 2 +
                 math.cos(user_lat_rad) * math.cos(spot_lat_rad) * math.sin(delta_lon / 2) ** 2)
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
            distance = R * c  # 距離 (km)

            # 移動時間を計算
            travel_time = distance / speed_kmh  # 時間 (h)

            # 結果をリストに追加
            results.append({
                **spot,
                'distance_km': round(distance, 2),
                'travel_time_hr': round(travel_time, 2),
            })
        except Exception as e:
            print(f"エラー: 観光地データが不正です: {spot} - {e}")

    return results