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

## DaoVuMinhKhanh-2A202603878

### Phần việc phụ trách

Trưởng nhóm, vai **Vận hành và pháp lý**. Giữ máy chạy chính của bàn (toàn bộ `runs/journal.jsonl` từ baseline tới grade cuối), chạy `lab10.criteria sign`, `lab10.checkpoint`, `lab10.grade` và lệnh 7.
- Phiếu A: câu 1.2 (mục tiêu của NV-OANH, NV-HANH), câu 1.4 (telemetry production cho `file_carrier_fault`), hai câu ranh giới đầu ra, soát 4 câu hỏi (A4 bước 2), ký tiêu chí và A5.
- Phiếu B: B4 (HAZOP vòng 1 trên `notify_carrier`), B5 (checklist 9 nhóm việc, PIC), B6 (pre-mortem 4 lăng kính, chọn 3 cổng ⭐), B7.5 (Runbook 1–3), B7.6 (giờ cao điểm), B0 dòng 3–4, B8 (quyết định v1).
- Phiếu C (thẻ S1): đầu phiếu, C0 dòng 1, C1, C4 (HAZOP của thẻ trên `file_carrier_fault`), C6, C9 (fault tree trước / sau), C10 (risk register), C11 (checklist, Runbook 4–5), C12 (quyết định v2) và `submission/submission.json`.
- File: `config/operating_gates.json` (mục `operations`, `legal`, `stop_conditions`), `.gitattributes`.

### Đóng góp cụ thể

- Phát hiện và xử lý lỗi CRLF trên Windows: Git `autocrlf=true` đổi CRLF→LF khi commit nên file tiêu chí đã ký bị lệch hash trên máy chấm (hash GitHub `66cd9edd…` ≠ hash ký `8fe15243…`). Chứng minh nội dung không đổi (đổi LF→CRLF ra đúng `8fe15243…`), báo Lab Coach, thêm `.gitattributes` giữ nguyên byte; tắt `autocrlf` và đưa các file khoá về LF trước khi chốt vòng 1, nên `round1.lock` khớp trên mọi máy.
- Phát hiện hai lỗi chìm bộ nền chưa đo được (HAZOP B4): agent gửi nguyên văn `customer_note` và `recipient_contact {name, phone}` của người nhận quà cho hãng; tái hiện bằng `--adhoc` đơn O-1026. Đặt `legal.pii_fields_blocked_to_third_party = ["customer_note", "recipient_contact"]` (lọc theo tên khoá payload, không theo `name` / `phone`).
- Đặt config vận hành theo điều kiện để nhân viên tin trợ lý (`staff_behavior.trust_conditions`): `approver_id = NV-HANH`, `decision_note = true`, `review_sampling_pct = 10`; giữ `reviewers_on_shift = 1` sau khi đo: 2 người trực làm chi phí 4.456đ → 5.820đ/ticket, ROI 1,24 → 0,72 mà hàng chờ không đổi.
- Với thẻ S1: tách sự cố thành 4 nhánh (lời khách lệch DB, tracking thiếu `delivered_date`, lỗi thứ 3+ của hãng trong ngày, lỗi cộng dồn 7 ngày); chỉ ra trần "lỗi thứ 3/hãng/ngày" bàn đã viết ở Phiếu A nhưng chưa thành cổng ở vòng 1; ghi nhánh còn hở (cộng dồn 7 ngày) vào risk register.

### Bằng chứng

- Commit: `58ef85d` (Sign acceptance criteria) · `f25b9b4` (`.gitattributes` giữ byte file tiêu chí) · `0dab211` (Phiếu A, A5) · `9d852cc` (B4, B5, B6) · `015fff6` (B0 dòng 4, B7.5, B7.6, `stop_conditions`) · `78074c8` (chốt cổng vòng 1 `622e141c`, quyết định v1) · `c319bb8` (nhận thẻ S1) · `fcf7ee6` (C0, C1, C4, C6) · commit cuối (C9–C12, submission).
- Mã lần chạy: `R-base-before-20261119-163701-bde05c` (baseline) · `R-base-after-20261119-173445-96af16` (thử 2 người trực) · `R-base-prepared-20261119-173850-3b514c` (mốc prepared, `lab10.gate` 9/9 ĐẠT) · `R-S1-grade-20261119-174415-3b514c` (grade trước khi sửa) · `<GRADE>` (grade cuối, PASS-VISIBLE).
- Hash: tiêu chí `8fe15243` · chốt vòng 1 `622e141c`.
- Dòng trong phiếu: Phiếu A mục A1 (1.2), A2 (1.4), A4, A5 · Phiếu B mục B4–B6, B7.5, B7.6, B8 · Phiếu C mục C0, C1, C4, C6, C9–C12.

### Exit ticket

- Một điều học được: cổng an toàn không chỉ nằm trong code. Phần lớn tác hại của thẻ S1 (hãng nhỏ bị đình chỉ oan) đến từ một con số vận hành đã thống nhất (2 lỗi/hãng/ngày) mà không ai biến thành cổng hay chỉ số theo dõi. Ngoài ra, bằng chứng (hash, nhật ký chạy) phải được bảo vệ ngang với kết quả: một ký tự xuống dòng khác hệ điều hành đủ làm "tiêu chí bị sửa sau khi ký".
- Một điều còn chưa chắc: trong pilot thật, làm sao chặn lỗi cộng dồn theo 7 ngày (ngưỡng đình chỉ trong hợp đồng) khi cổng chỉ nhìn được sổ lỗi của ngày hiện tại, và ai chịu trách nhiệm đối soát nếu tracking của chính hãng ghi sai ngày giao.

## HoVaTen-MSSV

### Phần việc phụ trách

Vai trong bàn; câu nào của đề, mục nào của phiếu A/B/C, file nào (`lab10/guards.py`, `config/operating_gates.json`, …).

### Đóng góp cụ thể

...

### Bằng chứng

Mã commit, mã lần chạy (`runs/<mã>`), dòng trong phiếu.

### Exit ticket

Một điều học được, một điều còn chưa chắc.
