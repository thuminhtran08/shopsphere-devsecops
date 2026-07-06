# Auth Service

## 1. Vai trò

`auth-service` phụ trách xác thực người dùng trong hệ thống ShopSphere.

Ở giai đoạn đầu, service này chỉ cung cấp endpoint kiểm tra hoạt động. Ở các bước tiếp theo, service sẽ được mở rộng để hỗ trợ đăng ký, đăng nhập, session/token và phân quyền cơ bản.

## 2. Endpoint hiện tại

| Method | Path | Ý nghĩa |
|---|---|---|
| GET | / | Kiểm tra service chạy |
| GET | /health | Health check cho Docker/Kubernetes |

## 3. Công nghệ

- Python
- FastAPI
- Uvicorn
- Pydantic

## 4. Trạng thái

Đang ở giai đoạn skeleton.