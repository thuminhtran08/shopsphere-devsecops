# Order Service

## 1. Vai trò

`order-service` phụ trách tạo và quản lý đơn hàng trong hệ thống ShopSphere.

Ở giai đoạn đầu, service này sử dụng dữ liệu mock trong RAM để kiểm tra API. Ở các phase sau, đơn hàng sẽ được lưu trong PostgreSQL và service sẽ publish event `OrderCreated` vào RabbitMQ.

## 2. Endpoint hiện tại

| Method | Path | Ý nghĩa |
|---|---|---|
| GET | / | Kiểm tra service chạy |
| GET | /health | Health check |
| GET | /orders | Lấy danh sách đơn hàng |
| GET | /orders/{order_id} | Lấy chi tiết đơn hàng |
| POST | /orders | Tạo đơn hàng |
| PATCH | /orders/{order_id}/status | Cập nhật trạng thái đơn hàng |

## 3. Công nghệ

- Python
- FastAPI
- Uvicorn
- Pydantic

## 4. Trạng thái

Đang ở giai đoạn skeleton/mock API.