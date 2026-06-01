"""
VinWonders Knowledge Base
Dữ liệu về các khu vui chơi, trò chơi, dịch vụ tại VinWonders Việt Nam
"""

VINWONDERS_DOCUMENTS = [
    # ===================== TỔNG QUAN =====================
    {
        "id": "overview_001",
        "category": "overview",
        "title": "Tổng quan VinWonders",
        "content": """
VinWonders là chuỗi công viên giải trí cao cấp thuộc tập đoàn Vingroup, hiện có mặt tại:
- VinWonders Phú Quốc (đảo Phú Quốc, Kiên Giang) - lớn nhất Đông Nam Á
- VinWonders Nha Trang (Hòn Tre, Khánh Hòa)
- VinWonders Nam Hội An (Quảng Nam)
- VinWonders Hà Nội (Times City, Hai Bà Trưng)

Giờ mở cửa chung: 9:00 - 21:00 hàng ngày.
Giá vé người lớn: từ 550.000đ - 900.000đ tùy địa điểm.
Giá vé trẻ em (dưới 1m): miễn phí. Trẻ từ 1m-1.4m: giảm 50%.
"""
    },

    # ===================== PHÚ QUỐC =====================
    {
        "id": "pq_001",
        "category": "location",
        "location": "Phú Quốc",
        "title": "VinWonders Phú Quốc - Tổng quan",
        "content": """
VinWonders Phú Quốc tọa lạc tại Bãi Dài, phía Bắc đảo Phú Quốc. Đây là công viên giải trí
lớn nhất Đông Nam Á với diện tích hơn 50 hecta. Công viên bao gồm 5 khu chủ đề chính:
1. Khu Khám phá Đại Dương (Ocean Discovery)
2. Khu Phiêu lưu Rừng Rậm (Jungle Adventure)
3. Khu Thế giới Nước (Water World)
4. Khu Lễ hội Ánh sáng (Festival of Lights)
5. Khu Hành trình Khám phá (Discovery Journey)
Địa chỉ: Bãi Dài, xã Gành Dầu, Phú Quốc, Kiên Giang.
Giá vé: 900.000đ/người lớn. Combo với cáp treo Hòn Thơm: 1.200.000đ.
"""
    },
    {
        "id": "pq_002",
        "category": "attraction",
        "location": "Phú Quốc",
        "zone": "Ocean Discovery",
        "title": "Khu Khám phá Đại Dương - Phú Quốc",
        "content": """
Khu Khám phá Đại Dương (Ocean Discovery) tại VinWonders Phú Quốc gồm các điểm hấp dẫn:
- Thủy cung khổng lồ: Tunnel kính dài 90m, hơn 20.000 sinh vật biển.
- Biểu diễn cá heo và sư tử biển: 3 suất/ngày lúc 10:00, 13:00, 16:00.
- Trải nghiệm lặn biển ảo (VR Diving): cảm giác lặn dưới đáy đại dương.
- Khu cá mập: xem cá mập qua vách kính dày 10cm an toàn.
- Touch Pool: chạm tay vào các sinh vật biển như sao biển, nhím biển.
Thời gian tham quan đề xuất: 2-3 tiếng.
"""
    },
    {
        "id": "pq_003",
        "category": "attraction",
        "location": "Phú Quốc",
        "zone": "Water World",
        "title": "Khu Thế giới Nước - Phú Quốc",
        "content": """
Water World tại VinWonders Phú Quốc là khu vui chơi dưới nước lớn nhất Việt Nam:
- Lazy River: dòng sông lười dài 320m, thư giãn trôi theo dòng nước.
- Wave Pool: hồ sóng nhân tạo cao tới 1.5m, cảm giác như đang ở biển.
- Super Bowl: trượt nước nhóm (4-6 người) trong bát xoáy khổng lồ.
- Kamikaze Slides: 5 máng trượt thẳng đứng tốc độ cao.
- Aqua Play: khu nước dành cho trẻ em với vòi phun, xô nước.
- Family Raft Ride: trượt bè theo gia đình, phù hợp mọi lứa tuổi.
Lưu ý: Mang theo đồ bơi. Có thể thuê tại chỗ: 100.000đ/bộ.
Tủ khóa: 50.000đ/tủ. Áo phao miễn phí.
"""
    },
    {
        "id": "pq_004",
        "category": "attraction",
        "location": "Phú Quốc",
        "zone": "Jungle Adventure",
        "title": "Khu Phiêu lưu Rừng Rậm - Phú Quốc",
        "content": """
Jungle Adventure - Khu phiêu lưu rừng nhiệt đới tại VinWonders Phú Quốc:
- Zipline xuyên rừng: 400m trên không, view toàn đảo Phú Quốc.
- Đu dây Tarzan: bộ môn mạo hiểm cho người thích cảm giác mạnh.
- Cầu treo rừng rậm: đi bộ trên cầu treo 200m giữa tán lá rừng.
- Xe địa hình ATV: lái xe off-road trong khu rừng 30 phút.
- Trại thú hoang dã: gặp gỡ các loài thú như nai, thỏ, trĩ, vẹt.
- Rock climbing: leo núi nhân tạo cao 12m với nhiều cấp độ khó.
Yêu cầu: Zipline và ATV: từ 12 tuổi, cao từ 1.4m trở lên.
"""
    },
    {
        "id": "pq_005",
        "category": "attraction",
        "location": "Phú Quốc",
        "zone": "Festival of Lights",
        "title": "Khu Lễ hội Ánh sáng - Phú Quốc",
        "content": """
Festival of Lights - Hoạt động buổi tối không thể bỏ qua tại VinWonders Phú Quốc:
- Lễ hội đèn lồng: thả đèn lồng trên mặt hồ mỗi tối 20:00.
- Show nhạc nước hoành tráng: 3D mapping + vòi phun nước + nhạc sống, 19:30 - 20:30.
- Khu phố đèn lồng châu Á: chụp ảnh check-in cực đẹp.
- Vòng quay ánh sáng: đu quay cao 60m, ngắm hoàng hôn Phú Quốc.
- Food street: phố ẩm thực 50+ gian hàng, đặc sản Phú Quốc và quốc tế.
Tip: Đến trước 18:00 để có chỗ tốt xem show nhạc nước.
"""
    },

    # ===================== NHA TRANG =====================
    {
        "id": "nt_001",
        "category": "location",
        "location": "Nha Trang",
        "title": "VinWonders Nha Trang - Tổng quan",
        "content": """
VinWonders Nha Trang nằm trên đảo Hòn Tre, cách bờ 3km, di chuyển bằng cáp treo hoặc tàu.
Đây là công viên giải trí kết hợp thiên nhiên biển đảo độc đáo với 7 khu chủ đề:
1. Khu Khám phá châu Âu
2. Khu Phiêu lưu Đông Nam Á  
3. Khu Trẻ em Vui vẻ
4. Water Park
5. Khu Văn hóa Việt
6. Khu Ẩm thực Quốc tế
7. Vườn thú bán hoang dã

Cáp treo Nha Trang: dài 3.2km, cao nhất thế giới qua biển.
Giá vé: 800.000đ/người lớn. Vé cáp treo khứ hồi: 250.000đ (riêng).
"""
    },
    {
        "id": "nt_002",
        "category": "attraction",
        "location": "Nha Trang",
        "zone": "Châu Âu",
        "title": "Khu Khám phá Châu Âu - Nha Trang",
        "content": """
Khu Châu Âu tại VinWonders Nha Trang mô phỏng kiến trúc cổ điển châu Âu:
- Tháp Eiffel thu nhỏ: chụp ảnh check-in biểu tượng.
- Đu quay không gian (Space Gyro): xoay 360 độ, cảm giác mất trọng lực.
- Tàu ma (Ghost Train): hành trình 8 phút trong bóng tối với hiệu ứng 4D.
- Nhà cười (Laugh House): mê cung gương và sàn rung cực vui.
- Bumper cars: đua xe điện va chạm, phù hợp mọi lứa tuổi.
- Free Fall Tower: nhảy tự do từ độ cao 45m, giảm tốc trong 2 giây.
Nên đi vào buổi chiều để tránh nắng gắt.
"""
    },
    {
        "id": "nt_003",
        "category": "attraction",
        "location": "Nha Trang",
        "zone": "Vườn thú",
        "title": "Vườn thú bán hoang dã - Nha Trang",
        "content": """
Vườn thú bán hoang dã VinWonders Nha Trang - trải nghiệm thiên nhiên hoang dã:
- Hơn 150 loài động vật từ khắp nơi trên thế giới.
- Safari xe điện: ngồi xe khám phá khu thú ăn cỏ tự do (hươu cao cổ, ngựa vằn, đà điểu).
- Feeding time: cho hươu cao cổ ăn trực tiếp vào 10:00 và 15:00.
- Khu linh trưởng: tinh tinh, khỉ đuôi sóc, vượn tay trắng.
- Bird Park: vườn chim nhiệt đới với 80+ loài chim quý hiếm.
- Reptile House: rắn hổ mang chúa, trăn, kỳ đà khổng lồ.
Thời gian tham quan: 1.5 - 2 tiếng.
"""
    },

    # ===================== NAM HỘI AN =====================
    {
        "id": "ha_001",
        "category": "location",
        "location": "Nam Hội An",
        "title": "VinWonders Nam Hội An - Tổng quan",
        "content": """
VinWonders Nam Hội An nằm tại Thừa Thiên, cách phố cổ Hội An 30 phút.
Đặc trưng: Kết hợp văn hóa Chăm Pa cổ xưa với giải trí hiện đại.
Các khu chính:
1. Khu phố cổ Hội An thu nhỏ
2. Khu văn hóa Chăm Pa
3. Vương quốc Trẻ em
4. Khu Phiêu lưu Đại Dương
5. Water Park Tropic
Nổi bật: Show Ký ức Hội An hàng đêm 19:00-21:00 (vé riêng 600.000đ).
Giá vé: 550.000đ/người lớn.
"""
    },

    # ===================== HÀ NỘI =====================
    {
        "id": "hn_001",
        "category": "location",
        "location": "Hà Nội",
        "title": "VinWonders Hà Nội - Tổng quan",
        "content": """
VinWonders Hà Nội tọa lạc trong khu Times City, quận Hai Bà Trưng.
Là khu vui chơi indoor và outdoor kết hợp, phù hợp gia đình trong thành phố.
Các khu vực:
1. Amazonia (khu phiêu lưu khủng long)
2. Ocean World (thủy cung và bể cá nước mặn)
3. Candy Land (khu trẻ em)
4. Adventure Zone (trò chơi cảm giác mạnh)
5. 4D Cinema & VR Zone
Phù hợp cho: gia đình có trẻ nhỏ, không cần di chuyển xa.
Giá vé: 350.000đ - 450.000đ tùy gói.
"""
    },

    # ===================== DỊCH VỤ CHUNG =====================
    {
        "id": "svc_001",
        "category": "service",
        "title": "Dịch vụ ẩm thực tại VinWonders",
        "content": """
Dịch vụ ăn uống tại VinWonders:
- Mỗi khu có 10-20 nhà hàng và gian hàng ăn uống.
- Đặc sản địa phương: Hải sản Phú Quốc, Bún bò Nha Trang, Cao lầu Hội An.
- Fast food quốc tế: Burger, Pizza, Chicken.
- Buffet BBQ tối: từ 350.000đ/người tại Phú Quốc và Nha Trang.
- Nước giải khát và kem: có tại tất cả các khu vực.
- Không được mang đồ ăn từ bên ngoài vào công viên.
- Khu vực picnic: có tại VinWonders Nam Hội An và Phú Quốc.
"""
    },
    {
        "id": "svc_002",
        "category": "service",
        "title": "Dịch vụ lưu trú và combo VinWonders",
        "content": """
Gói combo lưu trú và vé vào cổng VinWonders:
- Combo Vinpearl Resort + Vé VinWonders: tiết kiệm 20-30%.
- VinHolidays: gói du lịch trọn gói bao gồm khách sạn + vé + ăn sáng.
- Early check-in tại resort để vào công viên từ 8:30 (trước giờ mở cửa).
Tại Phú Quốc: kết nối Vinpearl Land - VinWonders - Safari miễn phí bằng xe bus nội bộ.
Booking: vinwonders.com hoặc app VinWonders.
Đặt vé trước 3 ngày giảm thêm 10%.
"""
    },
    {
        "id": "svc_003",
        "category": "service",
        "title": "Hướng dẫn chuẩn bị trước khi đến VinWonders",
        "content": """
Chuẩn bị trước khi đến VinWonders:
Trang phục:
- Mặc đồ thoải mái, giày thể thao có quai hậu.
- Đồ bơi nếu dự định chơi Water Park.
- Kem chống nắng SPF 50+ (bắt buộc nếu đến Phú Quốc/Nha Trang).

Lưu ý sức khỏe:
- Người cao huyết áp, tim mạch, phụ nữ mang thai: tránh trò chơi cảm giác mạnh.
- Trẻ dưới 3 tuổi: chỉ vào khu kids zone.
- Ăn trước ít nhất 1 tiếng trước khi chơi trò chơi mạo hiểm.

Vật dụng cần mang:
- CMND/CCCD hoặc hộ chiếu để check-in.
- Vé điện tử (QR code từ app hoặc email).
- Thẻ ngân hàng (hầu hết dịch vụ đã hỗ trợ thanh toán không tiền mặt).
"""
    },

    # ===================== LỊCH TRÌNH GỢI Ý =====================
    {
        "id": "itin_001",
        "category": "itinerary",
        "title": "Lịch trình 1 ngày VinWonders Phú Quốc",
        "content": """
Lịch trình gợi ý 1 ngày tại VinWonders Phú Quốc:
08:30 - 09:00: Check-in, nhận vé, bản đồ công viên.
09:00 - 11:00: Thủy cung & Ocean Discovery (mát mẻ buổi sáng).
11:00 - 12:00: Jungle Adventure - Zipline và cầu treo.
12:00 - 13:00: Ăn trưa tại Food Court khu Jungle.
13:00 - 16:00: Water World (giờ này nắng đẹp để chơi nước).
16:00 - 17:00: Nghỉ ngơi, tắm thay đồ, uống nước dừa.
17:00 - 18:30: Discovery Journey - các trò chơi cảm giác mạnh.
18:30 - 19:30: Ăn tối tại Food Street.
19:30 - 20:30: Xem Show nhạc nước Festival of Lights.
20:30 - 21:00: Thả đèn lồng và ra về.

Mẹo: Mua vé combo sunset để xem hoàng hôn trên vòng quay lúc 17:30.
"""
    },
    {
        "id": "itin_002",
        "category": "itinerary",
        "title": "Lịch trình 1 ngày VinWonders Nha Trang",
        "content": """
Lịch trình gợi ý 1 ngày tại VinWonders Nha Trang:
08:00 - 08:30: Đi cáp treo qua biển (view đẹp nhất buổi sáng sớm).
08:30 - 10:00: Vườn thú bán hoang dã + Feeding Time lúc 10:00.
10:00 - 12:00: Khu Châu Âu - Ghost Train, Free Fall, Đu quay.
12:00 - 13:30: Ăn trưa Buffet hải sản Nha Trang tại nhà hàng.
13:30 - 16:30: Water Park - Wave Pool, Lazy River.
16:30 - 17:30: Khu Văn hóa Việt - đồ thủ công, ảnh check-in.
17:30 - 18:30: Xem hoàng hôn từ đỉnh Hòn Tre.
18:30 - 19:30: Ăn tối ẩm thực đường phố.
19:30: Cáp treo về đất liền (chạy đến 20:30).

Lưu ý: Cáp treo cuối 20:30 - không được lỡ!
"""
    },
    {
        "id": "itin_003",
        "category": "itinerary",
        "title": "Lịch trình cho gia đình có trẻ nhỏ",
        "content": """
Lịch trình VinWonders phù hợp gia đình có trẻ nhỏ (5-10 tuổi):
Ưu tiên: VinWonders Hà Nội hoặc khu Candy Land/Kids Zone.

Buổi sáng (9:00-12:00):
- Amazonia: khu khủng long animatronic cực thích cho trẻ em.
- Ocean World: thủy cung mini, cho cá ăn, chạm sao biển.
- Carousel và Ferris wheel mini: an toàn cho mọi lứa tuổi.

Buổi trưa (12:00-13:30): Nghỉ ngơi, ăn nhẹ tại khu trẻ em.

Buổi chiều (13:30-17:00):
- Aqua Play: khu nước nông dành cho trẻ (không sâu quá 60cm).
- 4D Cinema: xem phim hoạt hình 4D (20 phút/suất).
- VR Zone: trải nghiệm thực tế ảo phù hợp trẻ từ 7 tuổi.

Mẹo cho phụ huynh:
- Đặt stroller/xe đẩy thuê trước tại quầy dịch vụ.
- Khu cho con bú và thay tã có ở mọi khu vực.
- Giữ trẻ đeo vòng tay định danh suốt ngày.
"""
    },
    {
        "id": "faq_001",
        "category": "faq",
        "title": "Câu hỏi thường gặp về VinWonders",
        "content": """
FAQ - Câu hỏi thường gặp:

Q: Có được mang thức ăn vào VinWonders không?
A: Không được mang thức ăn từ ngoài vào. Nước uống đóng chai nhỏ được phép mang.

Q: Mất vé điện tử thì làm thế nào?
A: Liên hệ quầy dịch vụ khách hàng với CCCD và email đặt vé để được cấp lại.

Q: Trời mưa thì sao?
A: Hầu hết trò chơi trong nhà vẫn hoạt động. Trò chơi ngoài trời và Water Park tạm dừng khi có sấm sét. Vé không hoàn tiền nhưng có thể đổi lịch.

Q: Có gửi đồ không?
A: Có tủ khóa điện tử tại cổng vào và gần Water Park. Giá 50.000-100.000đ/tủ/ngày.

Q: Xe lăn và người khuyết tật thì thế nào?
A: VinWonders có lối đi riêng cho xe lăn. Thuê xe lăn miễn phí tại quầy dịch vụ. Vé ưu đãi 50% cho người khuyết tật có xác nhận.

Q: Chụp ảnh chuyên nghiệp được không?
A: Được phép mang máy ảnh thông thường. Thiết bị chuyên nghiệp (gimbal, flycam) cần xin phép trước.
"""
    },
]