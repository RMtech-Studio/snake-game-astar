# 🐍 Snake Game AI - Thuật Toán Tìm Đường A* (A-Star Search)

> **Mã nguồn chính thức đi kèm Video Tập 02 của Kênh [RMtech (@rmt-20)](https://www.youtube.com/@rmt-20)**  
> *Series: Lập Trình Game Python Từ Con Số 0 • Tập 02: A-Star Search*

---

## 🌟 Điểm Nổi Bật Của Dự Án

Ở [Tập 01 (Thuật toán BFS)](https://github.com/RMtech-Studio/snake-game-bfs), chú rắn đã biết tự tìm đường ngắn nhất. Tuy nhiên, BFS là thuật toán tìm kiếm mù (Uninformed Search), nó duyệt lan tỏa ra mọi hướng xung quanh như một gợn sóng nước, gây lãng phí CPU.

Trong **Tập 02 này**, chúng ta nâng cấp lên **Thuật toán A\* (A-Star)**:
- 🎯 **Hàm Heuristic Manhattan**: $h(n) = |x_1 - x_2| + |y_1 - y_2|$ định hướng trực tiếp tới mục tiêu.
- ⚡ **Hàng đợi ưu tiên `heapq`**: Bốc ra node có $f(n) = g(n) + h(n)$ nhỏ nhất với độ phức tạp $O(\log N)$.
- 🚀 **Tiết kiệm 75% tài nguyên**: Số ô duyệt thử giảm từ ~65 ô (BFS) xuống chỉ còn ~12-14 ô (A\*)!
- 🛡️ **Tự động né thân**: Khi đường thẳng bị thân rắn chặn, hàm $f$ tự động điều hướng rắn đi đường vòng an toàn.

---

## 🚀 Cài Đặt & Chạy Trực Tiếp

### 1. Cài đặt thư viện:
```bash
pip install -r requirements.txt
```

### 2. Chạy Game:
```bash
python main.py
```

---

## 🎮 Điều Khiển & Phím Tắt

- **ESC**: Thoát game.
- Các chấm **Vàng Hổ Phách (Amber)**: Đường đi tối ưu do A\* tính toán.
- Các ô vuông **Xanh Mờ**: Vùng không gian A\* đã duyệt qua để tìm đường.
- **Thanh HUD**: Theo dõi điểm số (`SCORE`) và số ô A\* đã đánh giá (`NODES EVALUATED`).

---

## 📺 Video Hướng Dẫn Chi Tiết

Xem video phân tích từng dòng code và kiểm chứng thuật toán tại kênh YouTube chính thức:
👉 **[RMtech Channel: Code Game Rắn Săn Mồi Bằng Python](https://www.youtube.com/@rmt-20)**

---
*Mã nguồn mở phát hành theo giấy phép MIT. Bản quyền © 2026 RMtech Studio.*
