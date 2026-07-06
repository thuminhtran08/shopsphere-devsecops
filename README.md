# ShopSphere DevSecOps Platform

## 1. Giới thiệu

ShopSphere DevSecOps Platform là một bài lab E-commerce microservices được xây dựng để thực hành toàn bộ quy trình DevOps và DevSecOps hiện đại.

Project mô phỏng một hệ thống thương mại điện tử gồm các chức năng chính như đăng ký, đăng nhập, quản lý sản phẩm, giỏ hàng, đặt đơn, thanh toán giả lập, quản lý tồn kho, thông báo, đánh giá sản phẩm và dashboard quản trị.

Project không chỉ tập trung vào việc viết ứng dụng, mà còn tập trung vào toàn bộ vòng đời triển khai và vận hành hệ thống: từ Docker Compose, Kubernetes, Helm, ArgoCD, CI/CD, monitoring, autoscaling, security scanning cho đến backup và tự động hóa hạ tầng.

## 2. Mục tiêu project

Mục tiêu của project là xây dựng một hệ thống E-commerce đủ phức tạp để thực hành các kỹ năng DevOps thực tế.

Sau khi hoàn thành project, người học có thể:

- Chạy hệ thống microservices bằng Docker Compose.
- Triển khai hệ thống lên Kubernetes.
- Quản lý manifest bằng Helm chart.
- Triển khai theo mô hình GitOps bằng ArgoCD.
- Xây dựng CI/CD pipeline bằng GitHub Actions.
- Tích hợp kiểm tra bảo mật vào pipeline.
- Theo dõi hệ thống bằng Prometheus, Grafana, Loki và Tempo.
- Tự động scale service bằng KEDA.
- Thực hiện backup và restore dữ liệu.
- Tự động hóa hạ tầng bằng Terraform và Ansible.

## 3. Kiến trúc tổng quan

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