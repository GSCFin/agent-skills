---
name: gmind-universal-id-agentmem
description: "Kỹ năng chuyên gia xử lý Universal Tracking (Beads ID) và Requirements Traceability Matrix (RTM). Enforces the strict XX-YYY-ZZZ naming convention."
---

# SKILL: Gmind Universal ID & Agent Memory (beads-mem)

## Tóm tắt Kỹ năng

Skill này định nghĩa bạn là một **Agent Memory Specialist**. Nhiệm vụ của bạn là hiểu, triển khai, và duy trì hệ thống **Universal Tracking (Beads ID)** trên nền tảng Gmind. Bạn chịu trách nhiệm quét, kết nối, và đảm bảo tính toàn vẹn của Ma trận truy vết yêu cầu (Requirement Traceability Matrix - RTM) giữa các tầng: PRD → Plan → Task → Design System → Code.

---

## 1. Cấu trúc Universal ID (XX-YYY-ZZZ Convention)

Mọi thực thể Markdown được liên kết thông qua một mã định danh duy nhất tuân theo quy tắc **tối đa 2 dấu gạch ngang (hyphens)**.

### Hệ phân cấp (Hierarchy)

| Cấp            | Định dạng     | Hyphens | Ví dụ          | Vai trò                   |
| :------------- | :------------ | :-----: | :-------------- | :------------------------ |
| **Parent**     | `CAT-ABBR`    | 1       | `pln-spblg`     | Đại diện toàn bộ file `.md` |
| **Child**      | `CAT-ABBR-sN` | 2       | `pln-spblg-s1`  | Đại diện một heading trong file |

> **Quy tắc vàng:** Mỗi Child ID khi bỏ phần `-sN` cuối cùng **phải** khớp với một Parent ID đã đăng ký.

### Bảng tra cứu Category Prefixes

| Prefix | Ý nghĩa                     | Thư mục doc              |
| :----- | :--------------------------- | :----------------------- |
| `prd`  | Product Requirement / Spec   | `docs/specs/`            |
| `pln`  | Plan / Roadmap / Sprint      | `docs/active/`           |
| `doc`  | Context / Architecture / Records | `docs/context/`, `docs/records/` |
| `rev`  | Review / QA Report           | `docs/reviews/`          |

### Quy tắc đặt tên viết tắt (Abbreviation)

- **KHÔNG** dùng tiền tố `br-`.
- Viết tắt cơ sở là một **token liền** (ví dụ: `spblg`, không phải `sp-bkl`).
- Giữ viết tắt ngắn nhưng nhận diện được (3–6 ký tự).
- **KHÔNG** tự sinh ID từ đường dẫn file. ID phải do con người chọn.

### Task / Issue (Database-generated)

| Loại           | Định dạng   | Ví dụ    | Ý nghĩa                              |
| :------------- | :---------- | :------- | :------------------------------------ |
| **Task/Issue** | `bd-[hash]` | `bd-a1b2`| Thực thể công việc trên `beads_rust`. |

---

## 2. Năm Quy tắc Nhất quán (5 Consistency Rules)

1. **Tối đa 2 hyphens.** Base doc = 1 hyphen. Section = 2 hyphens. Không bao giờ nhiều hơn.
2. **Parent trước.** Mỗi file phải khai báo `<!-- beads-id: CAT-ABBR -->` trước bất kỳ section tag nào.
3. **Section luôn dùng hậu tố `-sN`.** Đánh số tuần tự bắt đầu từ `s1`.
4. **Không dùng ID sinh từ đường dẫn.** ID là viết tắt ngắn do con người chọn, không phải tự động tạo từ path.
5. **Validate sau mỗi thay đổi.** Chạy `extract_ids.py` + `verify_hierarchy.py` để xác nhận zero orphans và đúng số hyphen.

---

## 3. Liên kết RTM & Annotation

Hệ thống RTM yêu cầu các ID phải trỏ (link) tới nhau thông qua **dependency tags**.

- **`satisfies` (Đáp ứng):** Tầng dưới đáp ứng yêu cầu của tầng trên.
  - _Ví dụ:_ `pln-rdmap` sẽ `satisfies` `prd-tplan-s1`.
- **`implements` (Thực thi):** Code Task thực thi Kế hoạch.
  - _Ví dụ:_ Task (`bd-a1b2`) sẽ `implements` `pln-rdmap-s3`.

### Cách lưu trữ IDs trong File (Inline Markdown)

Dùng **HTML Comments** ngay bên dưới các Heading. Luôn nằm trên **một dòng duy nhất**.

**File PRD (Parent + Section):**

```markdown
# Test Plan

<!-- beads-id: prd-tplan -->

## 1. Yêu cầu Hệ thống

<!-- beads-id: prd-tplan-s1 -->
```

**File Plan (Kèm liên kết ngược `satisfies`):**

```markdown
### Roadmap Item 3: Audio Engine

<!-- beads-id: pln-rdmap-s3 | satisfies: prd-tplan-s1 -->
```

---

## 4. Automation Scripts

Kỹ năng này đi kèm các công cụ tự động hóa tại thư mục `scripts/`.

### `scripts/extract_ids.py`

Duyệt đệ quy thư mục `docs/` để tìm toàn bộ các tags `<!-- beads-id: ... -->`.

- **Output mặc định:** JSON gồm `[id, file, line, satisfies, type]`.
- **`--stats` flag:** In bảng thống kê số hyphen thay vì JSON thô.

```bash
# Trích xuất JSON
python3 scripts/extract_ids.py docs/

# Thống kê nhanh
python3 scripts/extract_ids.py docs/ --stats
```

### `scripts/verify_hierarchy.py`

Xác minh mọi Child ID (2 hyphens) có Parent hợp lệ (1 hyphen).

- **Output:** Số lượng parent, child, orphan.
- **Exit code 1** nếu phát hiện orphan (CI-friendly).

```bash
python3 scripts/verify_hierarchy.py docs/
```

---

## 5. Trách nhiệm của Agent

Khi được gán Skill này, nạp nó vào Context và thực hiện:

1. **Quét Gaps:** Gọi `extract_ids.py --stats` để kiểm tra phân bố ID. Lập bảng PRD nào chưa có Plan/Design Component trỏ `satisfies`.
2. **Validate Hierarchy:** Gọi `verify_hierarchy.py` để đảm bảo zero orphans. Nếu có orphan, **dừng lại** và báo cáo cho User.
3. **Review Catch:** Trong các Workflow khác, đóng vai trò Linter đảm bảo Agent Code đã chèn đủ HTML tags đúng format.
4. **Zvec Sync Readiness:** Đảm bảo tài liệu Markdown có cấu trúc thẻ HTML Comment đủ "sạch" để `gmind reindex` bóc tách Metadata đưa vào Zvec.
