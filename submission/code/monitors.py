"""★ FILE ĐỘI SỬA (2/3): chỉ số theo dõi (monitor). Thêm ÍT NHẤT MỘT chỉ số bắt được sự cố của bàn.

Mỗi monitor nhận danh sách trial (KHÔNG có nhãn đúng/sai, giống production) và trả về một số.
Một trial = {"ticket_id", "seed", "day", "status", "amount_vnd", "ticket", "events", "ledger", "faults", "outbound",
             "arrive_min", "warehouse", "cost_vnd", "review_kind", "queue_wait_min", "queue_stuck"}
  "day"            một ngày vận hành giả lập: các ticket cùng "day" và cùng "seed" chạy nối nhau trên cùng một sổ cái
  "arrive_min"     phút ticket tới trong ca (0..480)          "warehouse"   kho của đơn
  "cost_vnd"       tiền LLM + nền tảng đã tốn cho ticket      "review_kind" None / "escalated" (trợ lý chuyển người) /
  "queue_wait_min" số phút chờ người duyệt (None nếu không vào hàng chờ)     "recheck" (nhân viên tự kiểm lại)
Chỉ số có thể là kỹ thuật (tỉ lệ model đè số trong ticket lên DB), vận hành (số ca cần người trong giờ đông nhất),
hay kinh doanh (tỉ lệ ticket trợ lý đọc xong vẫn phải chuyển người).

lab10.grade kiểm: monitor chạy không lỗi, và giá trị trên gói sự cố khác giá trị trên bộ nền,
tức là monitor "sáng đèn" khi sự cố xảy ra.
"""


def escalation_rate(trials):
    return sum(t["status"] == "escalated" for t in trials) / max(1, len(trials))


def carrier_strikes_per_carrier_max(trials):
    """Số lỗi phạt tối đa tự động ghi cho cùng một hãng vận chuyển trong một ngày vận hành."""
    by_day_carrier = {}
    for t in trials:
        day = t.get("day", 1)
        for f in t.get("faults", []):
            cid = f.get("carrier_id")
            if cid:
                key = (day, cid)
                by_day_carrier[key] = by_day_carrier.get(key, 0) + 1
    return max(by_day_carrier.values(), default=0)


def claim_discrepancy_rate(trials):
    """Tỉ lệ ticket có sự kiện model_override do chênh lệch giữa ngày khách khai và tracking DB."""
    overrides = 0
    for t in trials:
        if any(e.get("type") == "model_override" for e in t.get("events", [])):
            overrides += 1
    return round(overrides / max(1, len(trials)), 4)


MONITORS = {
    "escalation_rate": escalation_rate,     # có sẵn; KHÔNG tính là metric mới của đội
    "carrier_strikes_per_carrier_max": carrier_strikes_per_carrier_max,
    "claim_discrepancy_rate": claim_discrepancy_rate,
}
STARTER_MONITORS = ("escalation_rate",)
