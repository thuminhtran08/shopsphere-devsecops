# 01. Project Overview

## 1. Project là gì?

ShopSphere DevSecOps Platform là một hệ thống E-commerce microservices dùng để thực hành DevOps và DevSecOps end-to-end.

Project mô phỏng một nền tảng thương mại điện tử với các chức năng chính như đăng ký, đăng nhập, xem sản phẩm, thêm sản phẩm vào giỏ hàng, tạo đơn hàng, thanh toán giả lập, quản lý tồn kho, gửi thông báo, đánh giá sản phẩm và quản trị hệ thống.

Điểm quan trọng của project này không chỉ là xây dựng một ứng dụng bán hàng, mà là thực hành toàn bộ quy trình triển khai và vận hành một hệ thống hiện đại: từ chạy local bằng Docker Compose, triển khai lên Kubernetes, đóng gói bằng Helm, triển khai GitOps bằng ArgoCD, xây dựng CI/CD pipeline, giám sát hệ thống, tự động scale, kiểm tra bảo mật và backup dữ liệu.

## 2. Vì sao chọn E-commerce?

E-commerce là một domain quen thuộc, dễ hiểu và có nhiều nghiệp vụ phù hợp để học microservices.

Một hệ thống E-commerce thực tế thường không chỉ có một ứng dụng duy nhất. Nó thường được chia thành nhiều phần như người dùng, sản phẩm, giỏ hàng, đơn hàng, thanh toán, tồn kho, thông báo và quản trị.

Điều này giúp project phù hợp để học các chủ đề DevOps quan trọng như:

* Docker Compose để chạy nhiều service cùng lúc.
* Kubernetes để triển khai từng service độc lập.
* API Gateway để gom điểm truy cập backend.
* PostgreSQL để lưu dữ liệu chính.
* Redis để cache và lưu session.
* RabbitMQ để truyền event giữa các service.
* Helm để quản lý cấu hình triển khai.
* ArgoCD để triển khai theo GitOps.
* CI/CD để tự động kiểm tra, build và deploy.
* Monitoring, logging và tracing để quan sát hệ thống.
* Security scanning để phát hiện lỗi bảo mật sớm.

## 3. Luồng nghiệp vụ chính

Luồng demo chính của hệ thống:

1. Người dùng đăng ký tài khoản.
2. Người dùng đăng nhập.
3. Người dùng xem danh sách sản phẩm.
4. Người dùng xem chi tiết một sản phẩm.
5. Người dùng thêm sản phẩm vào giỏ hàng.
6. Người dùng tạo đơn hàng.
7. Hệ thống xử lý thanh toán giả lập.
8. Hệ thống kiểm tra và trừ tồn kho.
9. Hệ thống gửi thông báo trạng thái đơn hàng.
10. Người dùng đánh giá sản phẩm sau khi mua.
11. Admin theo dõi đơn hàng và trạng thái hệ thống.

## 4. Luồng kỹ thuật chính

Luồng kỹ thuật tổng quan:

User hoặc Admin truy cập vào Frontend Web. Frontend gửi request tới Kong API Gateway. Kong kiểm tra path của request và chuyển tiếp tới backend service phù hợp.

Ví dụ:

* Request `/api/auth` đi tới `auth-service`.
* Request `/api/products` đi tới `product-service`.
* Request `/api/cart` đi tới `cart-service`.
* Request `/api/orders` đi tới `order-service`.
* Request `/api/payments` đi tới `payment-service`.
* Request `/api/inventory` đi tới `inventory-service`.
* Request `/api/notifications` đi tới `notification-service`.
* Request `/api/reviews` đi tới `review-service`.
* Request `/api/admin` đi tới `admin-service`.

Các service sử dụng PostgreSQL để lưu dữ liệu chính, Redis để cache/session và RabbitMQ để truyền sự kiện giữa các service.

## 5. Ví dụ luồng tạo đơn hàng

Khi người dùng tạo một đơn hàng, hệ thống xử lý theo luồng sau:

1. Frontend gửi request tạo đơn hàng tới Kong.
2. Kong route request tới `order-service`.
3. `order-service` kiểm tra thông tin giỏ hàng.
4. `order-service` tạo đơn hàng trong PostgreSQL.
5. `order-service` publish event `OrderCreated` vào RabbitMQ.
6. `payment-service` nhận event và xử lý thanh toán giả lập.
7. `inventory-service` nhận event và trừ tồn kho.
8. `notification-service` nhận event và gửi thông báo cho người dùng.
9. Admin có thể xem đơn hàng trong dashboard quản trị.

## 6. Danh sách service dự kiến

| Service              | Vai trò                               |
| -------------------- | ------------------------------------- |
| frontend             | Giao diện web cho người dùng và admin |
| auth-service         | Đăng ký, đăng nhập và xác thực        |
| user-service         | Quản lý thông tin người dùng          |
| product-service      | Quản lý danh sách sản phẩm            |
| cart-service         | Quản lý giỏ hàng                      |
| order-service        | Tạo và quản lý đơn hàng               |
| payment-service      | Thanh toán giả lập                    |
| inventory-service    | Quản lý tồn kho                       |
| notification-service | Gửi thông báo                         |
| review-service       | Đánh giá sản phẩm                     |
| admin-service        | Dashboard quản trị                    |

## 7. Thành phần hạ tầng chính

| Thành phần     | Vai trò                                                                              |
| -------------- | ------------------------------------------------------------------------------------ |
| PostgreSQL     | Lưu dữ liệu chính như users, products, carts, orders, payments, inventory và reviews |
| Redis          | Cache dữ liệu đọc nhiều, lưu session và dữ liệu tạm                                  |
| RabbitMQ       | Message broker để truyền event giữa các service                                      |
| Kong           | API Gateway, route request tới đúng backend service                                  |
| Docker         | Đóng gói từng service thành container                                                |
| Kubernetes     | Chạy và quản lý container ở môi trường cluster                                       |
| Helm           | Đóng gói Kubernetes manifests thành chart                                            |
| ArgoCD         | Triển khai GitOps từ Git vào Kubernetes                                              |
| Prometheus     | Thu metrics                                                                          |
| Grafana        | Hiển thị dashboard                                                                   |
| Loki           | Lưu log                                                                              |
| Tempo          | Lưu distributed trace                                                                |
| KEDA           | Autoscaling theo metric hoặc queue                                                   |
| GitHub Actions | CI/CD pipeline                                                                       |
| Terraform      | Tạo hạ tầng                                                                          |
| Ansible        | Cấu hình máy chủ và bootstrap môi trường                                             |

## 8. Mục tiêu học tập

Sau khi hoàn thành project, người học có thể:

* Thiết kế một hệ thống microservices ở mức cơ bản đến nâng cao.
* Chạy hệ thống nhiều service bằng Docker Compose.
* Chuyển đổi hệ thống từ Docker Compose sang Kubernetes.
* Viết Kubernetes manifests cho Deployment, Service, StatefulSet, ConfigMap, Secret và Ingress.
* Đóng gói manifests bằng Helm chart.
* Triển khai ứng dụng bằng ArgoCD theo mô hình GitOps.
* Viết CI/CD pipeline bằng GitHub Actions.
* Tích hợp kiểm tra bảo mật bằng Gitleaks, Semgrep và Trivy.
* Theo dõi hệ thống bằng Prometheus, Grafana, Loki và Tempo.
* Tự động scale service bằng KEDA.
* Thực hiện backup và restore dữ liệu PostgreSQL.
* Tự động hóa hạ tầng bằng Terraform và Ansible.

## 9. Lộ trình triển khai

Project được chia thành các phase:

| Phase    | Nội dung                                      |
| -------- | --------------------------------------------- |
| Phase 0  | Khởi tạo repository và tài liệu nền tảng      |
| Phase 1  | Chạy hệ thống local bằng Docker Compose       |
| Phase 2  | Triển khai hệ thống bằng Kubernetes manifests |
| Phase 3  | Đóng gói hệ thống bằng Helm chart             |
| Phase 4  | Triển khai GitOps bằng ArgoCD                 |
| Phase 5  | Xây dựng CI/CD DevSecOps pipeline             |
| Phase 6  | Monitoring, logging và tracing                |
| Phase 7  | Autoscaling bằng KEDA                         |
| Phase 8  | Security hardening                            |
| Phase 9  | Backup và restore                             |
| Phase 10 | Terraform và Ansible cho hạ tầng              |

## 10. Trạng thái hiện tại

Project đang ở Phase 0.

Các phần đã hoàn thành:

* Tạo cấu trúc repository.
* Tạo README.md.
* Tạo .gitignore.
* Tạo thư mục docs.
* Tạo các file tài liệu nền cho từng phase.

Các phần tiếp theo:

* Hoàn thiện tài liệu kiến trúc.
* Tạo Docker Compose bản đầu tiên.
* Tạo các service mock ban đầu.
* Chạy hệ thống local trên máy cá nhân.
