# Team

## Thông tin nhóm

- Tên nhóm (`TenNhom`, không dấu, không khoảng trắng): ThaoDanh
- Lớp: `L3B`
- Repo của bàn: `K5-L3B-DAY10-ThaoDanh-PoCtoPilotGate1`
- Thẻ sự cố đã bốc (S1–S8): S1

## Thành viên

Họ tên đầy đủ và MSSV của **mọi** thành viên; bàn 3 người thì để trống dòng 4. Vai: Kỹ sư cổng · Sản phẩm và kinh doanh · Vận hành và pháp lý (README mục 3, phút 0–15).

| STT | Họ và tên | MSSV | Vai | Trưởng nhóm |
| --: | --------- | ---- | --- | :---------: |
|   1 | Đào Vũ Minh Khánh | 2A202603878 | Vận hành và pháp lý | x |
|   2 | Đào Nguyễn Quang Thành | 2A202603754 | Kỹ sư cổng | |
|   3 | Trương Đức Phát | 2A202603757 | Sản phẩm và kinh doanh | |

Ghi `members` trong `submission/submission.json` theo dạng `"HoVaTen-MSSV"`, khớp bảng trên.

## Cá nhân

Mỗi thành viên tự viết một mục bên dưới (chép mẫu, đổi tiêu đề thành họ tên không dấu và MSSV, ví dụ `## NguyenVanAn-20241234`).

## DaoNguyenQuangThanh-2A202603754

### Phần việc phụ trách

- Vai trong bàn: Kỹ sư cổng (Gate Engineer).
- Phụ trách chính các file mã nguồn logic cổng và giám sát: `lab10/guards.py`, `lab10/monitors.py`, cấu hình `config/operating_gates.json`, kiểm tra tính toàn vẹn và regression.
- Phụ trách các mục trong phiếu:
  - Phiếu B: Mục B2 (bảng soát lỗi `T-002`), B7.1–B7.4 (thiết kế và lập trình cổng vòng 1).
  - Phiếu C: Mục C0 (dòng 2-4 nhật ký lần chạy vòng 2), C2 (bảng soát lỗi 3 tầng sự cố thẻ S1), C7 (bảng sửa logic 3 nhánh cổng), C8 (đặc tả và lập trình chỉ số theo dõi mới).

### Đóng góp cụ thể

- Vòng 1: Thiết kế cổng so khớp quyền lợi hoàn tiền theo DB (`issue_refund`) và cổng kiểm tra nguyên nhân trễ (`file_carrier_fault`), chốt hash vòng 1 `622e141c`.
- Vòng 2 (Sự cố thẻ S1 - GHSH bị phạt oan dồn dập):
  - Phân tích và sửa triệt để 3 nhánh sự cố trong `lab10/guards.py`:
    1. Nhánh [1]: Chặn trợ lý từ chối oan khi khách khai ngày trễ thấp hơn DB trong `write_gate` (`tool == "send_reply"`), kích hoạt `escalate` bảo vệ quyền lợi khách và phạt đúng lỗi hãng.
    2. Nhánh [2]: Bắt lỗi dữ liệu `status == "DELIVERED"` nhưng thiếu `delivered_date` trong `pre_guard` và `write_gate` (`tool == "issue_refund"`), chuyển người duyệt thay vì để helper tính nhầm trễ theo ngày hiện tại.
    3. Nhánh [3]: Cài đặt cổng thẩm quyền khống chế trần phạt đối tác trong `write_gate` (`tool == "file_carrier_fault"`), kiểm tra `fault_rows()` và từ chối (`deny`) ngay khi hãng chạm trần 2 lỗi/ngày, dập tắt nguy cơ đình công.
  - Thiết kế và đăng ký 2 chỉ số giám sát mới trong `lab10/monitors.py`: `carrier_strikes_per_carrier_max` (sáng đèn đỏ 20.0 khi dồn dập lỗi) và `claim_discrepancy_rate`.
  - Giữ vững 100% pass_rate cho cả bộ nền 110 ca (không regression) và 100% visible pass cho gói sự cố S1 (hoàn sai về 0đ, lỗi phạt oan về 0).

### Bằng chứng

- Mã lần chạy: `R-S1-grade-20261119-190921-a8bbc2` (PASS-VISIBLE ✅), `R-S1-after-20261119-190413-a8bbc2`, `R-base-after-20261119-190419-a8bbc2`.
- File sửa: `lab10/guards.py`, `lab10/monitors.py`, `templates/form-c-incident.md` (mục C0, C2, C7, C8).

### Exit ticket

- Một điều học được: Guardrail không chỉ dừng ở việc bảo vệ ví tiền của công ty (ngăn hoàn dư) mà còn đóng vai trò sống còn trong việc bảo vệ đối tác thứ ba (hãng vận chuyển) trước sự dồn dập lỗi của hệ thống tự động để tránh rủi ro pháp lý và đứt gãy chuỗi cung ứng.
- Một điều còn chưa chắc: Khi cổng chặn lệnh phạt tự động thứ 3 trở đi để bảo vệ trần ngày của hãng, quy trình đối soát thủ công ngày hôm sau cần cơ chế đồng bộ thế nào để nếu hãng thực sự vi phạm nhiều ca thì vẫn có bằng chứng xử lý mà không bị sót việc.

## TruongDucPhat-2A202603757

### Phần việc phụ trách

- Vai trong bàn: Sản phẩm và kinh doanh.
- Phiếu C, thẻ S1: C3.5 (mở lại bản đồ dữ liệu) và C5 (specification, giả định môi trường).

### Đóng góp cụ thể

- Bổ sung đối chiếu từng trường của `parcel`, phân biệt dữ liệu chuẩn với dữ liệu đầy đủ/đã được xác minh; làm rõ tác động tới quyền lợi khách, tiền hoàn và lỗi hãng.
- Viết điều kiện chuyển người khi kiện đã giao nhưng thiếu ngày giao và cách kiểm bằng cổng/nhãn S1; nêu giả định về việc cập nhật tracking của hãng.
- Sử dụng trợ lý AI để đọc dữ liệu/code trong repo, đối chiếu Phiếu B mục B3 và soạn nội dung C3.5, C5. Không chạy lại đánh giá trong phần việc này.

### Bằng chứng

- `templates/form-c-incident.md`: mục C3.5 và C5.
- Nguồn đối chiếu: `incidents/S1/card.md`, `world_patch.json`, `tickets.jsonl`; `lab10/helpers.py`, `lab10/guards.py`; Phiếu B mục B3.

### Exit ticket (dự thảo để Phát rà lại)

- Một điều học được: nguồn dữ liệu chuẩn vẫn có thể thiếu hoặc mâu thuẫn; cần kiểm tính đầy đủ trước khi dùng dữ liệu để quyết định tiền và trách nhiệm của hãng.
- Một điều còn chưa chắc: trong pilot thật, làm sao phát hiện ngày giao đã điền nhưng sai, và lấy bằng chứng giao nhận nào để xác minh kịp thời.

## HoVaTen-MSSV

### Phần việc phụ trách

Vai trong bàn; câu nào của đề, mục nào của phiếu A/B/C, file nào (`lab10/guards.py`, `config/operating_gates.json`, …).

### Đóng góp cụ thể

...

### Bằng chứng

Mã commit, mã lần chạy (`runs/<mã>`), dòng trong phiếu.

### Exit ticket

Một điều học được, một điều còn chưa chắc.
