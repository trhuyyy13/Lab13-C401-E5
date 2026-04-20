# 3 Kịch Bản Tấn Công Mô Phỏng (Incident Injection)

Tài liệu này mô tả 3 kiểu "tấn công mô phỏng" trong bài lab observability. Mục tiêu là kiểm thử khả năng giám sát, cảnh báo và ứng phó sự cố, không phải hướng dẫn tấn công thực tế.

## Cách Chạy Chung

1. Khởi động app:

```bash
python -m uvicorn app.main:app --reload
```

2. Mở dashboard:

```text
http://127.0.0.1:8000/dashboard
```

3. Tạo tải lượng để thay đổi metrics:

```bash
python scripts/load_test.py --concurrency 5
```

---

## 1) rag_slow - Làm Chậm Lớp Truy Xuất (RAG)

### Ý nghĩa
- Mô phỏng backend truy xuất tài liệu bị chậm.
- Dùng để kiểm thử SLO độ trễ (latency) và cảnh báo P95.

### Lệnh chạy

Bật sự cố:

```bash
python scripts/inject_incident.py --scenario rag_slow
```

Tắt sự cố:

```bash
python scripts/inject_incident.py --scenario rag_slow --disable
```

### Kết quả kỳ vọng
- Dashboard panel latency tăng rõ, đặc biệt P95/P99.
- Có thể vượt ngưỡng cảnh báo latency (theo docs alerts).
- Error rate thường không tăng mạnh (hệ thống vẫn trả lời, nhưng chậm).

---

## 2) tool_fail - Lỗi Công Cụ/Nguồn Dữ Liệu

### Ý nghĩa
- Mô phỏng thành phần RAG/tool bị timeout hoặc lỗi runtime.
- Dùng để kiểm thử cảnh báo tỷ lệ lỗi và runbook xử lý sự cố.

### Lệnh chạy

Bật sự cố:

```bash
python scripts/inject_incident.py --scenario tool_fail
```

Tắt sự cố:

```bash
python scripts/inject_incident.py --scenario tool_fail --disable
```

### Kết quả kỳ vọng
- Error rate tăng cao và dễ kích hoạt cảnh báo P1.
- Error breakdown xuất hiện nhóm lỗi liên quan đến tool/RAG timeout.
- Chat có thể trả lời thất bại ở một phần hoặc nhiều request.

---

## 3) cost_spike - Đột Biến Chi Phí

### Ý nghĩa
- Mô phỏng token output tăng mạnh, dẫn đến chi phí tăng nhanh.
- Dùng để kiểm thử cảnh báo ngân sách (burn rate).

### Lệnh chạy

Bật sự cố:

```bash
python scripts/inject_incident.py --scenario cost_spike
```

Tắt sự cố:

```bash
python scripts/inject_incident.py --scenario cost_spike --disable
```

### Kết quả kỳ vọng
- Panel cost tăng nhanh theo thời gian.
- Tokens out tăng rõ rệt so với bình thường.
- Có thể kích hoạt cảnh báo "cost budget spike" (P2).

---

## Kiểm Tra Nhanh Sau Khi Bật Sự Cố

1. Bật 1 scenario bằng `inject_incident.py`.
2. Chạy load test để tạo dữ liệu:

```bash
python scripts/load_test.py --concurrency 5
```

3. Quan sát dashboard trong 15-60 giây (auto refresh).
4. Tắt scenario để hệ thống quay lại trạng thái ổn định.

## Lưu Ý
- Đây là cơ chế "incident injection" phục vụ học observability.
- Không sử dụng cho mục đích tấn công hệ thống thật.
