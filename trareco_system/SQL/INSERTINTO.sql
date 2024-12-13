-- 感性推定のためにユーザに選んでもらう観光地情報
INSERT INTO tourist_area (path, area_name, longitude, latitude, season_id, timezone_id, category_id, crowding, weather) VALUES
	('山_1_冬_夜.jpg', '立山', '36.584550', '137.614098', '4', '2', '1', '0', '1'),
	('山_1_冬_昼.jpg', '立山', '36.584550', '137.614098', '4', '1', '1', '0', '2'),
	('山_1_夏_夜.jpg', '立山', '36.584550', '137.614098', '2', '2', '1', '0', '1'),
	('山_1_夏_昼.jpg', '立山', '36.584550', '137.614098', '2', '1', '1', '0', '2'),
	('山_1_春_夜.jpg', '立山', '36.584550', '137.614098', '1', '2', '1', '0', '1'),
	('山_1_春_昼.jpg', '立山', '36.584550', '137.614098', '1', '1', '1', '0', '2'),
	('山_1_秋_夜.jpg', '立山', '36.584550', '137.614098', '3', '2', '1', '0', '1'),
	('山_1_秋_昼.jpg', '立山', '36.584550', '137.614098', '3', '1', '1', '0', '1'),
	('山_2_冬_夜.jpg', '伊吹山', '35.419295', '136.406172', '4', '2', '1', '0', '1'),
	('山_2_冬_昼.jpg', '伊吹山', '35.419295', '136.406172', '4', '1', '1', '0.03', '2'),
	('山_2_夏_夜.jpg', '伊吹山', '35.419295', '136.406172', '2', '2', '1', '0', '1'),
	('山_2_夏_昼.jpg', '伊吹山', '35.419295', '136.406172', '2', '1', '1', '0', '2'),
	('山_2_春_夜.jpg', '伊吹山', '35.419295', '136.406172', '1', '2', '1', '0', '1'),
	('山_2_春_昼.jpg', '伊吹山', '35.419295', '136.406172', '1', '1', '1', '0', '1'),
	('山_2_秋_夜.jpg', '伊吹山', '35.419295', '136.406172', '3', '2', '1', '0', '1'),
	('山_2_秋_昼.jpg', '伊吹山', '35.419295', '136.406172', '3', '1', '1', '0', '2'),
	('温泉_1_冬_夜.jpg', '草津温泉', '36.683360', '138.555817', '4', '2', '2', '0.01', '1'),
	('温泉_1_冬_昼.jpg', '草津温泉', '36.683360', '138.555817', '4', '1', '2', '0', '1'),
	('温泉_1_夏_夜.jpg', '草津温泉', '36.683360', '138.555817', '2', '2', '2', '0', '1'),
	('温泉_1_夏_昼.jpg', '草津温泉', '36.683360', '138.555817', '2', '1', '2', '0', '1'),
	('温泉_1_春_夜.jpg', '草津温泉', '36.683360', '138.555817', '1', '2', '2', '0', '2'),
	('温泉_1_春_昼.jpg', '草津温泉', '36.683360', '138.555817', '1', '1', '2', '0', '1'),
	('温泉_1_秋_夜.jpg', '草津温泉', '36.683360', '138.555817', '3', '2', '2', '0', '1'),
	('温泉_1_秋_昼.jpg', '草津温泉', '36.683360', '138.555817', '3', '1', '2', '0', '1'),
	('温泉_2_冬_夜.jpg', '別府温泉', '33.297844', '131.484086', '4', '2', '2', '0', '1'),
	('温泉_2_冬_昼.jpg', '別府温泉', '33.297844', '131.484086', '4', '1', '2', '0', '1'),
	('温泉_2_夏_夜.jpg', '別府温泉', '33.297844', '131.484086', '2', '2', '2', '0', '2'),
	('温泉_2_夏_昼.jpg', '別府温泉', '33.297844', '131.484086', '2', '1', '2', '0', '1'),
	('温泉_2_春_夜.jpg', '別府温泉', '33.297844', '131.484086', '1', '2', '2', '0', '1'),
	('温泉_2_春_昼.jpg', '別府温泉', '33.297844', '131.484086', '1', '1', '2', '0', '1'),
	('温泉_2_秋_夜.jpg', '別府温泉', '33.297844', '131.484086', '3', '2', '2', '0', '2'),
	('温泉_2_秋_昼.jpg', '別府温泉', '33.297844', '131.484086', '3', '1', '2', '0.01', '2'),
	('神社_1_冬_夜.jpg', '伊勢神宮', '34.454992', '136.725447', '4', '2', '3', '0.02', '1'),
	('神社_1_冬_昼.jpg', '伊勢神宮', '34.454992', '136.725447', '4', '1', '3', '0', '4'),
	('神社_1_夏_夜.jpg', '伊勢神宮', '34.454992', '136.725447', '2', '2', '3', '0.05', '2'),
	('神社_1_夏_昼.jpg', '伊勢神宮', '34.454992', '136.725447', '2', '1', '3', '0.02', '1'),
	('神社_1_春_夜.jpg', '伊勢神宮', '34.454992', '136.725447', '1', '2', '3', '0.03', '1'),
	('神社_1_春_昼.jpg', '伊勢神宮', '34.454992', '136.725447', '1', '1', '3', '0', '2'),
	('神社_1_秋_夜.jpg', '伊勢神宮', '34.454992', '136.725447', '3', '2', '3', '0', '1'),
	('神社_1_秋_昼.jpg', '伊勢神宮', '34.454992', '136.725447', '3', '1', '3', '0', '2'),
	('神社_2_冬_夜.jpg', '金閣寺', '35.039628', '135.729288', '4', '2', '3', '0', '4'),
	('神社_2_冬_昼.jpg', '金閣寺', '35.039628', '135.729288', '4', '1', '3', '0', '1'),
	('神社_2_夏_夜.jpg', '金閣寺', '35.039628', '135.729288', '2', '2', '3', '0', '1'),
	('神社_2_夏_昼.jpg', '金閣寺', '35.039628', '135.729288', '2', '1', '3', '0', '2'),
	('神社_2_春_夜.jpg', '金閣寺', '35.039628', '135.729288', '1', '2', '3', '0', '1'),
	('神社_2_春_昼.jpg', '金閣寺', '35.039628', '135.729288', '1', '1', '3', '0', '1'),
	('神社_2_秋_夜.jpg', '金閣寺', '35.039628', '135.729288', '3', '2', '3', '0', '2'),
	('神社_2_秋_昼.jpg', '金閣寺', '35.039628', '135.729288', '3', '1', '3', '0', '2');
	
	
-- それぞれの観光地の色彩ヒストグラム
INSERT INTO colorhistgram (red, orange, yellow, green, blue, indigo, purple, black, gray, white) VALUES
	('0', '81', '0', '0', '2', '65421', '6312', '15086', '153063', '35'),
	('0', '132581', '0', '0', '0', '9686', '63012', '10330', '24073', '318'),
	('0', '54', '1', '0', '0', '2748', '278', '119065', '117839', '15'),
	('5174', '86853', '0', '0', '0', '9771', '11138', '8017', '93915', '25132'),
	('0', '0', '0', '0', '0', '1', '1', '233003', '6995', '0'),
	('0', '132581', '0', '0', '0', '9686', '63012', '10330', '24073', '318'),
	('367', '33275', '219', '3', '891', '20879', '69491', '59285', '53624', '1966'),
	('34107', '42221', '294', '0', '4334', '22183', '64074', '18994', '45066', '8727'),
	('0', '166', '0', '0', '0', '8477', '5166', '103846', '122345', '0'),
	('4', '174063', '0', '0', '1', '4758', '29293', '9055', '22623', '203'),
	('0', '4898', '0', '0', '0', '19842', '12154', '76547', '125726', '833'),
	('0', '39770', '111', '2', '187', '34581', '57620', '12286', '73135', '22308'),
	('0', '675', '23', '0', '0', '24261', '28667', '94537', '91597', '240'),
	('222', '118975', '0', '4', '39', '14115', '78216', '2472', '18691', '7266'),
	('0', '6', '0', '0', '0', '47454', '3934', '68564', '120040', '2'),
	('124241', '27490', '353', '15', '3500', '11873', '36474', '2346', '8875', '24833'),
	('1', '35027', '307', '0', '10201', '13536', '37517', '72977', '32146', '38288'),
	('0', '45903', '0', '0', '0', '45800', '82437', '8894', '48496', '8470'),
	('0', '13364', '0', '0', '40', '28901', '47021', '24298', '123169', '3207'),
	('3', '26548', '0', '0', '0', '19458', '43786', '87698', '59140', '3367'),
	('7', '11716', '5558', '1', '1362', '36715', '38151', '32129', '107109', '7252'),
	('0', '40306', '0', '0', '0', '22592', '62789', '39547', '63408', '11358'),
	('13910', '52229', '25', '0', '4696', '14566', '38134', '63013', '40164', '13263'),
	('183', '18767', '6', '0', '6051', '15218', '21651', '52386', '99268', '26470'),
	('0', '41583', '0', '0', '670', '19034', '32311', '60557', '67455', '18390'),
	('0', '41794', '0', '0', '0', '27207', '59218', '21404', '71759', '18618'),
	('802', '17313', '24', '29', '4170', '28769', '36757', '64541', '85431', '2164'),
	('0', '14691', '725', '0', '23', '30335', '38394', '62549', '89540', '3743'),
	('4', '10151', '2', '25', '400', '22560', '37630', '71264', '95289', '2675'),
	('0', '38970', '21', '0', '62', '17649', '48950', '68775', '57275', '8298'),
	('2861', '6314', '574', '0', '848', '12243', '10283', '66461', '117418', '22998'),
	('16', '49024', '93', '0', '777', '30257', '61163', '22481', '66059', '10130'),
	('0', '5044', '0', '0', '0', '6868', '11062', '178557', '36375', '2094'),
	('0', '93395', '0', '0', '0', '9625', '39203', '25441', '67893', '4443'),
	('3', '3049', '0', '0', '1424', '9012', '12282', '175312', '37798', '1120'),
	('0', '22134', '25', '0', '0', '19247', '32001', '67178', '88415', '11000'),
	('7', '16137', '0', '0', '2', '17808', '45145', '124208', '36115', '578'),
	('0', '74738', '0', '0', '0', '18455', '66766', '11328', '24425', '44288'),
	('119', '13661', '7114', '0', '893', '49645', '43781', '29501', '90540', '4746'),
	('0', '66576', '0', '0', '0', '19073', '74817', '30527', '47482', '1525'),
	('0', '13263', '0', '0', '0', '48790', '79500', '36204', '60386', '1857'),
	('6908', '43403', '0', '0', '307', '27641', '64436', '21361', '60109', '15835'),
	('0', '8564', '0', '0', '2', '3960', '11783', '202046', '13489', '156'),
	('0', '29817', '1', '0', '22', '20233', '23297', '46066', '89193', '31371'),
	('0', '11999', '0', '0', '0', '6627', '14848', '177598', '24866', '4062'),
	('0', '56449', '150', '0', '15', '23947', '58656', '16804', '80994', '2985'),
	('0', '5041', '10', '0', '173', '4770', '6670', '194061', '28679', '596'),
	('68', '48256', '3', '0', '991', '27932', '51367', '16366', '79450', '15567');

-- 観光地の季節
INSERT INTO season (season_id, season) 
VALUES
(1, '春'),
(2, '夏'),
(3, '秋'),
(4, '冬');

-- 観光地の時間帯
INSERT INTO timezone (timezone_id, timezone) 
VALUES
(1, '朝昼'),
(2, '夜');

-- 観光地のカテゴリー
INSERT INTO category (category_id, category) 
VALUES
(1, '山'),
(2, '温泉'),
(3, '神社');

-- 天気
INSERT INTO weather (weather_id, weather) VALUES
	('1', '晴'),
	('2', '曇'),
	('3', '雨'),
	('4', '雪');

-- 感性語と色彩の対応表
INSERT INTO color2imp (imp_name, red, orange, yellow, green, blue, indigo, purple, black, gray, white) VALUES
	('楽しい', '8', '10', '9', '6', '5', '3', '4', '1', '2', '7'),
	('賑やかな', '10', '9', '8', '3', '5', '4', '6', '1', '2', '7'),
	('ゆっくり', '1', '2', '3', '10', '9', '5', '4', '6', '7', '8'),
	('気が晴れる', '4', '5', '6', '10', '8', '7', '3', '1', '2', '9'),
	('面白い', '8', '10', '9', '1', '2', '3', '6', '4', '5', '7'),
	('わいわい', '8', '9', '10', '4', '5', '3', '6', '1', '2', '7'),
	('はしゃぐ', '6', '8', '7', '3', '5', '2', '9', '1', '4', '10'),
	('のんびり', '1', '3', '2', '10', '9', '8', '4', '7', '6', '5'),
	('うきうき', '7', '10', '9', '1', '6', '2', '8', '3', '4', '5'),
	('落ち着いた', '1', '5', '3', '7', '6', '4', '2', '8', '10', '9'),
	('田舎', '1', '2', '3', '10', '9', '5', '4', '6', '7', '8'),
	('わくわく', '10', '9', '8', '1', '3', '2', '7', '4', '5', '6'),
	('きれい', '1', '8', '2', '10', '9', '5', '6', '4', '3', '7'),
	('癒される', '1', '2', '3', '9', '10', '7', '4', '6', '5', '8'),
	('まったり', '1', '2', '3', '10', '4', '5', '6', '9', '8', '7');
	


-- その他の感性による重みづけ
INSERT INTO imp_weight (season_spring, season_summer, season_fall, season_winter, time_morning2noon, time_night, category_mountain, category_hotspring, category_temple) VALUES
	('1', '2', '1', '1', '2', '1', '1', '2', '1'),
	('2', '2', '1', '1', '2', '1', '1', '2', '1'),
	('1', '1', '2', '2', '1', '2', '2', '1', '2'),
	('1', '1', '1', '1', '2', '1', '2', '1', '1'),
	('1', '2', '1', '1', '2', '1', '1', '2', '1'),
	('1', '2', '1', '1', '1', '1', '1', '2', '1'),
	('1', '1', '1', '1', '2', '1', '1', '2', '1'),
	('1', '1', '2', '1', '1', '2', '2', '2', '1'),
	('2', '1', '1', '1', '2', '1', '1', '2', '1'),
	('1', '1', '2', '2', '1', '2', '2', '1', '2'),
	('1', '1', '2', '2', '1', '1', '1', '1', '2'),
	('2', '1', '1', '1', '2', '1', '2', '1', '1'),
	('2', '1', '2', '2', '1', '1', '2', '1', '1'),
	('1', '1', '2', '1', '1', '1', '2', '2', '1'),
	('1', '1', '2', '2', '1', '1', '1', '2', '1');

-- 推薦用の観光地情報
INSERT INTO return_tourist_area (r_path, r_area_name, r_longitude, r_latitude, r_season_id, r_timezone_id, r_category_id, r_crowding, r_weather) VALUES
	('下呂温泉.jpg', '下呂温泉', '35.361393', '138.727191', '1', '2', '2', '0', '1'),
	('道後温泉.jpg', '道後温泉', '35.714875', '139.796507', '3', '2', '2', '0', '2'),
	('厳島神社.jpg', '厳島神社', '36.226062', '140.106977', '4', '1', '3', '0', '1'),
	('浅草寺.jpg', '浅草寺', '33.852041', '132.786631', '4', '2', '3', '0', '1'),
	('富士山.jpg', '富士山', '35.809520', '137.238344', '4', '1', '1', '0', '1'),
	('筑波山.jpg', '筑波山', '34.332482', '132.351163', '2', '1', '1', '0.05', '1');

-- 推薦用の観光地情報の色彩ヒストグラム
INSERT INTO return_colorhistgram (r_red, r_orange, r_yellow, r_green, r_blue, r_indigo, r_purple, r_black, r_gray, r_white) VALUES
	('1', '10067', '17', '2', '227', '21129', '38863', '81402', '87402', '890'),
	('195', '20310', '566', '15', '6804', '23618', '68042', '52934', '67087', '429'),
	('5', '80319', '0', '0', '804', '19414', '93101', '1826', '24299', '20232'),
	('1664', '14127', '2', '0', '174', '7676', '15005', '176248', '22970', '2134'),
	('0', '136404', '0', '0', '0', '34568', '61994', '1167', '4618', '1249'),
	('0', '102385', '1', '0', '0', '23994', '44299', '1833', '66429', '1059');