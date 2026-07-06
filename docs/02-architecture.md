# 02. Architecture

## 1. Mục tiêu kiến trúc

ShopSphere được thiết kế theo kiến trúc microservices để mô phỏng một hệ thống E-commerce hiện đại.

Mục tiêu của kiến trúc này là:

* Tách hệ thống thành nhiều service nhỏ, mỗi service phụ trách một nhóm nghiệp vụ riêng.
* Cho phép từng service có thể build, deploy và scale độc lập.
* Sử dụng API Gateway để gom điểm truy cập backend.
* Sử dụng PostgreSQL để lưu dữ liệu chính.
* Sử dụng Redis để cache và lưu session.
* Sử dụng RabbitMQ để truyền event giữa các service.
* Chuẩn bị nền tảng cho Docker Compose, Kubernetes, Helm, ArgoCD, CI/CD, monitoring và security.

## 2. Kiến trúc tổng quan

Luồng tổng quan của hệ thống:

```text
User / Admin
    |
    v
Frontend Web
    |
    v
Ingress Controller
    |
    v
Kong API Gateway
    |
    +--> auth-service
    +--> user-service
    +--> product-service
    +--> cart-service
    +--> order-service
    +--> payment-service
    +--> inventory-service
    +--> notification-service
    +--> review-service
    +--> admin-service
    |
    +--> PostgreSQL
    +--> Redis
    +--> RabbitMQ
```

Trong giai đoạn chạy local bằng Docker Compose, luồng có thể hiểu đơn giản hơn:

```text
Browser
    |
    v
Frontend
    |
    v
Kong API Gateway
    |
    v
Backend Services
    |
    +--> PostgreSQL
    +--> Redis
    +--> RabbitMQ
```

Khi chuyển sang Kubernetes, bên ngoài hệ thống sẽ đi qua Ingress Controller trước khi vào Kong.

## 3. Vai trò của Frontend

Frontend là giao diện web mà người dùng và admin tương tác trực tiếp.

Frontend chịu trách nhiệm:

* Hiển thị danh sách sản phẩm.
* Hiển thị chi tiết sản phẩm.
* Cho phép người dùng đăng ký, đăng nhập.
* Cho phép thêm sản phẩm vào giỏ hàng.
* Cho phép tạo đơn hàng.
* Hiển thị trạng thái thanh toán, tồn kho và thông báo.
* Hiển thị màn hình quản trị cho admin.

Frontend không gọi trực tiếp từng backend service. Frontend chỉ gọi API thông qua Kong API Gateway.

Ví dụ:

```text
Frontend gọi /api/products
→ Kong nhận request
→ Kong chuyển request đến product-service
```

Cách làm này giúp frontend không cần biết hệ thống phía sau có bao nhiêu service.

## 4. Vai trò của Kong API Gateway

Kong API Gateway là cổng vào trung tâm của toàn bộ backend.

Kong chịu trách nhiệm:

* Nhận request từ frontend.
* Kiểm tra đường dẫn request.
* Route request đến đúng backend service.
* Có thể thêm CORS, rate limiting, logging, authentication và monitoring plugin.
* Giấu cấu trúc backend service khỏi frontend.

Bảng route dự kiến:

| Public path          | Service đích         | Ý nghĩa                        |
| -------------------- | -------------------- | ------------------------------ |
| `/api/auth`          | auth-service         | Đăng ký, đăng nhập             |
| `/api/users`         | user-service         | Hồ sơ người dùng               |
| `/api/products`      | product-service      | Danh sách và chi tiết sản phẩm |
| `/api/cart`          | cart-service         | Giỏ hàng                       |
| `/api/orders`        | order-service        | Đơn hàng                       |
| `/api/payments`      | payment-service      | Thanh toán                     |
| `/api/inventory`     | inventory-service    | Tồn kho                        |
| `/api/notifications` | notification-service | Thông báo                      |
| `/api/reviews`       | review-service       | Đánh giá                       |
| `/api/admin`         | admin-service        | Quản trị                       |

Ví dụ request:

```text
GET /api/products
```

Kong sẽ chuyển tiếp đến:

```text
product-service
```

Ví dụ khác:

```text
POST /api/orders
```

Kong sẽ chuyển tiếp đến:

```text
order-service
```

## 5. Danh sách microservices

### 5.1. auth-service

`auth-service` phụ trách đăng ký, đăng nhập và xác thực người dùng.

Nhiệm vụ chính:

* Đăng ký tài khoản.
* Đăng nhập.
* Tạo token hoặc session.
* Kiểm tra thông tin xác thực.
* Cung cấp endpoint health check.

Dữ liệu liên quan:

* Đọc/ghi user cơ bản trong PostgreSQL.
* Lưu session hoặc token metadata trong Redis nếu cần.

Ví dụ API:

```text
POST /register
POST /login
GET /health
```

### 5.2. user-service

`user-service` phụ trách hồ sơ người dùng.

Nhiệm vụ chính:

* Xem thông tin cá nhân.
* Cập nhật tên, số điện thoại, địa chỉ.
* Quản lý địa chỉ giao hàng.
* Cung cấp dữ liệu người dùng cho các service khác khi cần.

Ví dụ API:

```text
GET /me
PUT /me
GET /addresses
POST /addresses
GET /health
```

### 5.3. product-service

`product-service` phụ trách sản phẩm.

Nhiệm vụ chính:

* Lấy danh sách sản phẩm.
* Xem chi tiết sản phẩm.
* Tìm kiếm sản phẩm.
* Lọc sản phẩm theo danh mục.
* Admin tạo, sửa, xóa sản phẩm.

Dữ liệu liên quan:

* Bảng products.
* Bảng categories.
* Có thể dùng Redis để cache danh sách sản phẩm đọc nhiều.

Ví dụ API:

```text
GET /products
GET /products/{id}
GET /categories
POST /products
PUT /products/{id}
DELETE /products/{id}
GET /health
```

### 5.4. cart-service

`cart-service` phụ trách giỏ hàng.

Nhiệm vụ chính:

* Thêm sản phẩm vào giỏ hàng.
* Cập nhật số lượng.
* Xóa sản phẩm khỏi giỏ.
* Xem giỏ hàng hiện tại.
* Chuẩn bị dữ liệu để tạo đơn hàng.

Dữ liệu liên quan:

* Có thể lưu cart trong PostgreSQL để bền vững.
* Có thể cache cart tạm thời trong Redis.

Ví dụ API:

```text
GET /cart
POST /cart/items
PUT /cart/items/{item_id}
DELETE /cart/items/{item_id}
GET /health
```

### 5.5. order-service

`order-service` phụ trách đơn hàng.

Nhiệm vụ chính:

* Tạo đơn hàng từ giỏ hàng.
* Lưu đơn hàng vào PostgreSQL.
* Cập nhật trạng thái đơn hàng.
* Publish event `OrderCreated` vào RabbitMQ.
* Cung cấp lịch sử đơn hàng cho người dùng.

Dữ liệu liên quan:

* Bảng orders.
* Bảng order_items.
* Event `OrderCreated`.

Ví dụ API:

```text
POST /orders
GET /orders
GET /orders/{id}
PATCH /orders/{id}/status
GET /health
```

### 5.6. payment-service

`payment-service` phụ trách thanh toán giả lập.

Nhiệm vụ chính:

* Nhận event `OrderCreated`.
* Xử lý thanh toán giả lập.
* Cập nhật trạng thái thanh toán.
* Publish event `PaymentSucceeded` hoặc `PaymentFailed`.

Dữ liệu liên quan:

* Bảng payments.
* Event `PaymentSucceeded`.
* Event `PaymentFailed`.

Ví dụ API:

```text
POST /payments/mock
GET /payments/{order_id}
GET /health
```

### 5.7. inventory-service

`inventory-service` phụ trách tồn kho.

Nhiệm vụ chính:

* Quản lý số lượng tồn kho.
* Kiểm tra sản phẩm còn hàng hay không.
* Trừ tồn kho sau khi đơn hàng được thanh toán.
* Publish event `InventoryReserved` hoặc `InventoryFailed`.

Dữ liệu liên quan:

* Bảng inventory.
* Event từ order/payment.
* Event phản hồi về tồn kho.

Ví dụ API:

```text
GET /inventory/{product_id}
PATCH /inventory/{product_id}
GET /health
```

### 5.8. notification-service

`notification-service` phụ trách thông báo.

Nhiệm vụ chính:

* Nhận event từ RabbitMQ.
* Gửi thông báo khi đơn hàng được tạo.
* Gửi thông báo khi thanh toán thành công hoặc thất bại.
* Gửi thông báo khi đơn hàng được giao.
* Có thể hỗ trợ WebSocket ở phase nâng cao.

Dữ liệu liên quan:

* Bảng notifications.
* Event `OrderCreated`.
* Event `PaymentSucceeded`.
* Event `PaymentFailed`.

Ví dụ API:

```text
GET /notifications
PATCH /notifications/{id}/read
GET /health
```

### 5.9. review-service

`review-service` phụ trách đánh giá sản phẩm.

Nhiệm vụ chính:

* Người dùng đánh giá sản phẩm đã mua.
* Hiển thị điểm đánh giá trung bình.
* Hiển thị danh sách review.
* Admin có thể ẩn review không phù hợp.

Dữ liệu liên quan:

* Bảng reviews.
* Bảng review_summary nếu cần tối ưu đọc.

Ví dụ API:

```text
POST /reviews
GET /products/{product_id}/reviews
GET /health
```

### 5.10. admin-service

`admin-service` phụ trách quản trị.

Nhiệm vụ chính:

* Xem tổng số user.
* Xem số đơn hàng.
* Xem doanh thu giả lập.
* Xem trạng thái service.
* Quản lý sản phẩm, đơn hàng và tồn kho ở mức admin.

Ví dụ API:

```text
GET /admin/dashboard
GET /admin/orders
GET /admin/products
GET /health
```

## 6. Data layer

### 6.1. PostgreSQL

PostgreSQL là database chính của hệ thống.

Dữ liệu lưu trong PostgreSQL gồm:

* Users.
* User profiles.
* Products.
* Categories.
* Cart items.
* Orders.
* Order items.
* Payments.
* Inventory.
* Notifications.
* Reviews.

Trong giai đoạn đầu, toàn bộ service có thể dùng chung một PostgreSQL database để đơn giản hóa demo.

Ở giai đoạn nâng cao hơn, có thể tách database theo service.

### 6.2. Redis

Redis được dùng cho dữ liệu tạm thời và dữ liệu cần đọc nhanh.

Redis có thể dùng cho:

* Session.
* Cache danh sách sản phẩm.
* Cache thông tin user.
* Rate limiting nếu kết hợp với gateway.
* Trạng thái online nếu dùng WebSocket.

Ví dụ key Redis:

```text
session:<session_id>
product_cache:<product_id>
user_profile:<user_id>
```

### 6.3. RabbitMQ

RabbitMQ là message broker.

RabbitMQ giúp các service giao tiếp với nhau qua event thay vì gọi trực tiếp quá nhiều.

Ví dụ event:

```text
OrderCreated
PaymentSucceeded
PaymentFailed
InventoryReserved
InventoryFailed
NotificationCreated
```

Ví dụ luồng event:

```text
order-service
→ publish OrderCreated
→ payment-service nhận event
→ inventory-service nhận event
→ notification-service nhận event
```

Cách làm này giúp hệ thống dễ mở rộng hơn vì mỗi service có thể xử lý công việc riêng mà không phụ thuộc quá chặt vào service khác.

## 7. Luồng tạo đơn hàng

Luồng tạo đơn hàng là luồng nghiệp vụ quan trọng nhất của project.

Các bước:

1. User chọn sản phẩm trên frontend.
2. User thêm sản phẩm vào giỏ hàng.
3. User bấm tạo đơn hàng.
4. Frontend gửi request tới `/api/orders`.
5. Kong route request tới `order-service`.
6. `order-service` kiểm tra giỏ hàng.
7. `order-service` tạo bản ghi order trong PostgreSQL.
8. `order-service` publish event `OrderCreated` vào RabbitMQ.
9. `payment-service` nhận event và xử lý thanh toán giả lập.
10. `payment-service` publish event `PaymentSucceeded` hoặc `PaymentFailed`.
11. `inventory-service` nhận event thanh toán thành công và trừ tồn kho.
12. `notification-service` gửi thông báo cho user.
13. Frontend hiển thị trạng thái đơn hàng mới nhất.

Sơ đồ text:

```text
Frontend
  |
  v
Kong
  |
  v
order-service
  |
  +--> PostgreSQL
  |
  +--> RabbitMQ: OrderCreated
            |
            +--> payment-service
            +--> inventory-service
            +--> notification-service
```

## 8. Triển khai local bằng Docker Compose

Ở Phase 1, toàn bộ hệ thống sẽ chạy local bằng Docker Compose.

Các container dự kiến:

* frontend
* kong
* auth-service
* user-service
* product-service
* cart-service
* order-service
* payment-service
* inventory-service
* notification-service
* review-service
* admin-service
* postgres
* redis
* rabbitmq

Mục tiêu của Phase 1 là chạy được:

```bash
docker compose up -d --build
```

Sau đó truy cập được:

```text
Frontend: http://localhost:3000
Kong API Gateway: http://localhost:8000
RabbitMQ UI: http://localhost:15672
```

## 9. Triển khai trên Kubernetes

Ở Phase 2, mỗi thành phần sẽ được chuyển sang Kubernetes.

Mapping dự kiến:

| Thành phần            | Kubernetes resource              |
| --------------------- | -------------------------------- |
| frontend              | Deployment + Service             |
| backend services      | Deployment + Service             |
| kong                  | Deployment + Service + ConfigMap |
| postgres              | StatefulSet + PVC + Service      |
| redis                 | StatefulSet + PVC + Service      |
| rabbitmq              | StatefulSet hoặc Helm chart      |
| environment variables | Secret + ConfigMap               |
| external traffic      | Ingress                          |

## 10. Observability

Hệ thống sẽ có monitoring, logging và tracing.

### Metrics

Metrics dùng để trả lời câu hỏi:

```text
Hệ thống đang chạy như thế nào?
```

Ví dụ metrics:

* Request per second.
* Error rate.
* P95 latency.
* CPU usage.
* Memory usage.
* Pod restart count.
* RabbitMQ queue length.
* PostgreSQL connection count.

### Logs

Logs dùng để trả lời câu hỏi:

```text
Chuyện gì đã xảy ra?
```

Ví dụ log:

```json
{
  "service": "order-service",
  "event": "order_created",
  "order_id": "ORD-1001",
  "user_id": "USER-1",
  "status": "created"
}
```

### Traces

Traces dùng để trả lời câu hỏi:

```text
Một request đã đi qua những service nào và chậm ở đâu?
```

Ví dụ trace tạo đơn hàng:

```text
Kong
→ order-service
→ PostgreSQL
→ RabbitMQ
→ payment-service
→ inventory-service
→ notification-service
```

## 11. Security architecture

Các lớp bảo mật dự kiến:

* API Gateway kiểm soát request đi vào backend.
* CORS cấu hình ở gateway.
* Rate limiting để hạn chế spam request.
* Secret không được commit vào Git.
* Security scanning trong CI/CD.
* Container image scan bằng Trivy.
* Secret scan bằng Gitleaks.
* Source code scan bằng Semgrep.
* Kubernetes NetworkPolicy để giới hạn service nào được gọi service nào.
* SecurityContext để giảm quyền container.
* Sealed Secrets hoặc External Secrets để quản lý secret an toàn.

## 12. Autoscaling

Hệ thống sẽ hỗ trợ autoscaling ở phase nâng cao.

Ví dụ:

* `product-service` scale theo request per second.
* `order-service` scale theo request per second.
* `notification-service` scale theo RabbitMQ queue length.
* `payment-service` scale theo CPU hoặc request rate.

Công cụ chính:

* HPA cho CPU/memory.
* KEDA cho Prometheus metric hoặc RabbitMQ queue length.

## 13. Backup và restore

Dữ liệu quan trọng nhất nằm trong PostgreSQL.

Backup/restore cần chứng minh được:

1. Tạo dữ liệu mẫu.
2. Backup database.
3. Xóa dữ liệu hoặc giả lập mất dữ liệu.
4. Restore database.
5. Kiểm tra dữ liệu quay lại.

Đây là phần giúp project gần với vận hành thực tế hơn.

## 14. Kết luận kiến trúc

ShopSphere được thiết kế như một hệ thống E-commerce microservices đủ phức tạp để thực hành DevOps và DevSecOps.

Kiến trúc này có đủ các thành phần quan trọng:

* Frontend.
* API Gateway.
* Nhiều backend service.
* PostgreSQL.
* Redis.
* RabbitMQ.
* Docker.
* Kubernetes.
* Helm.
* ArgoCD.
* CI/CD.
* Observability.
* Security.
* Autoscaling.
* Backup/restore.

Đây là nền tảng để các phase tiếp theo triển khai từng bước từ local đến Kubernetes và GitOps.
