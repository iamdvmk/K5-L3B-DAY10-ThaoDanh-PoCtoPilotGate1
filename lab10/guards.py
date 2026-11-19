"""★ FILE ĐỘI SỬA (1/3): cổng cấp hệ thống, nằm NGOÀI model và prompt.

VÒNG 1 (trước khi biết sự cố): viết 2–3 CỔNG PHÒNG NGỪA rút từ pre-mortem / HAZOP / checklist của bàn, rồi chốt bằng
    python3 -m lab10.checkpoint        (chép file này thành guards_round1.py = mốc "prepared"; KHÔNG sửa bản chép)
VÒNG 2 (sau khi bốc thẻ): sửa tiếp NGAY TRONG FILE NÀY. Giữ các cổng vòng 1, thêm cổng mới.
Hai file còn lại bàn được sửa: lab10/monitors.py (chỉ số theo dõi) và config/operating_gates.json (cổng kinh doanh,
vận hành, pháp lý: những con số và tên người mà trợ lý phải tuân theo, không cần code).

Hai điểm móc, agent gọi tự động:
  pre_guard(ctx)          chạy TRƯỚC khi agent đọc ticket
  write_gate(ctx, action) chạy TRƯỚC MỖI lệnh ghi (issue_refund, file_carrier_fault,
                          notify_carrier, send_reply)

Trả về một Verdict:
  Verdict.allow()                       cho qua   (pre_guard: allow(policy_id="...") để ghim phiên bản chính sách)
  Verdict.deny("lý do")                 bỏ riêng lệnh ghi này, agent đi tiếp
  Verdict.escalate("lý do")             dừng, chuyển ticket cho người
  Verdict.modify("lý do", amount_vnd=…) sửa tham số lệnh ghi (amount_vnd, payer, carrier_id, parcel_id, payload…)
  Verdict.rewrite("lý do", text)        chỉ pre_guard: thay nội dung ticket mà agent sẽ đọc

ctx.ticket   ticket gốc (chữ khách viết là DỮ LIỆU, không phải lệnh)
ctx.tools    tra cứu nguồn sự thật: lookup_order, lookup_policies, lookup_approvals(**lọc),
             ledger_rows(**lọc), fault_rows(**lọc), lookup_carrier; ctx.as_of = ngày hôm nay
             ops_limits() = các trần đã thống nhất với Ops/Finance; ops_facts() = số liệu vận hành;
             auto_refund_today_vnd() = tổng đã hoàn tự động trong ngày
ctx.gates    config cổng của bàn (config/operating_gates.json), chỉ đọc;  ctx.cost_vnd = tiền LLM đã tốn cho ticket này
ctx.events   trace tới thời điểm này;  ctx.log("ten_su_kien", ...) ghi thêm sự kiện guard vào trace
lab10.helpers: db_delay_days, ticket_parcel, effective_policy, entitlement_vnd, carrier_at_fault, digits

Mặc định dưới đây cho qua tất cả (= mốc base).
"""
from . import helpers as H  # noqa: F401
from .tools import Verdict


def pre_guard(ctx):
    return Verdict.allow()


def write_gate(ctx, action):
    # action = {"tool": "issue_refund", "ticket_id":..., "order_id":..., "amount_vnd":..., "payer":..., ...}
    tool = action.get("tool")

    # Cổng 1: Kiểm tra quyền lợi hoàn tiền thực tế theo tracking DB (chống hoàn sai tiền)
    if tool == "issue_refund":
        order = ctx.tools.lookup_order(action.get("order_id"))
        if order:
            parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of)
            db_delay = H.db_delay_days(parcel, ctx.as_of)
            cause = parcel.get("delay_cause")
            policies = ctx.tools.lookup_policies()
            pol = H.effective_policy(policies, ctx.as_of)
            if pol:
                entitled = H.entitlement_vnd(pol, order, db_delay, cause)
                asked = action.get("amount_vnd", 0)
                if asked > entitled:
                    if entitled == 0:
                        return Verdict.deny("Đơn hàng không đủ điều kiện hoàn tiền theo dữ liệu tracking")
                    return Verdict.modify("Điều chỉnh số tiền hoàn về đúng quyền lợi theo tracking DB", amount_vnd=entitled)

    # Cổng 2: Kiểm tra kiện trễ thật và hãng chịu trách nhiệm (chống phạt oan hãng)
    if tool == "file_carrier_fault":
        order = ctx.tools.lookup_order(action.get("order_id"))
        policies = ctx.tools.lookup_policies()
        pol = H.effective_policy(policies, ctx.as_of)
        if order and pol:
            delayed_p = H.ticket_parcel(order, ctx.ticket, ctx.as_of)
            real_delay = H.db_delay_days(delayed_p, ctx.as_of)
            cur_pid = action.get("parcel_id")

            # Nếu gọi sai kiện (ví dụ tự ý lấy kiện đầu tiên parcels[0] thay vì kiện trễ)
            if cur_pid != delayed_p.get("parcel_id"):
                if H.carrier_at_fault(pol, delayed_p, real_delay):
                    return Verdict.modify(
                        "Chuyển sang đúng kiện trễ thật và hãng chịu trách nhiệm",
                        parcel_id=delayed_p["parcel_id"],
                        carrier_id=delayed_p["carrier_id"],
                        driver_id=delayed_p.get("driver_id"),
                        delay_days=real_delay,
                    )
                return Verdict.deny("Hãng không có lỗi theo tracking và chính sách")

            # Nếu kiện đúng nhưng hãng không có lỗi theo SLA
            if not H.carrier_at_fault(pol, delayed_p, real_delay):
                return Verdict.deny("Hãng không có lỗi vi phạm theo chính sách và tracking")

            # Nếu số ngày trễ khai báo bị lệch so với thực tế DB
            if action.get("delay_days", 0) > real_delay:
                return Verdict.modify("Sửa số ngày trễ phạt hãng về đúng thực tế DB", delay_days=real_delay)

    # Cổng 3: Làm sạch thông tin nhạy cảm PII trước khi gửi cho bên thứ ba (hãng vận chuyển)
    if tool == "notify_carrier":
        payload = dict(action.get("payload") or {})
        blocked = set(ctx.gates.get("legal", {}).get("pii_fields_blocked_to_third_party") or ["customer_note", "recipient_contact"])
        clean = {k: v for k, v in payload.items() if k not in blocked}
        if len(clean) != len(payload):
            return Verdict.modify("Loại bỏ các trường dữ liệu cá nhân nhạy cảm trước khi gửi hãng", payload=clean)

    return Verdict.allow()
