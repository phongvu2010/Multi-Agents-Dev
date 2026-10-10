---
name: gherkin-generator
description: "Chuyển đổi User Stories thành bộ kịch bản kiểm thử hành vi (Behavior-Driven Development - BDD) theo chuẩn cú pháp Gherkin (Feature, Scenario, Given, When, Then, And, But)."
---

# Gherkin Generator Skill

## Mục đích
Hỗ trợ Business Analyst Agent và QA Agent chuẩn hóa mọi Acceptance Criteria (AC) của User Stories thành kịch bản kiểm thử có thể tự động hóa (testable specification).

## Cấu trúc chuẩn:
```gherkin
Feature: [Tên tính năng lớn]
  As a [Vai trò người dùng]
  I want to [Hành động mong muốn]
  So that [Mục tiêu kinh doanh đạt được]

  Background:
    Given [Điều kiện nền tảng áp dụng cho mọi kịch bản]

  Scenario: [Kịch bản thành công - Happy Path]
    Given [Tiền điều kiện xác thực]
    When [Hành động của người dùng kích hoạt]
    Then [Hệ thống phản hồi thành công]
    And [Dữ liệu được cập nhật chính xác]

  Scenario Outline: [Kịch bản kiểm thử biên / Dữ liệu sai - Edge/Error Path]
    Given [Tiền điều kiện]
    When [Người dùng nhập <input>]
    Then [Hệ thống từ chối và trả về mã lỗi <error_code>]
    Examples:
      | input | error_code |
      | ...   | ...        |
```

## Quy tắc bắt buộc:
1. Mỗi User Story phải có tối thiểu 1 Happy Path và 2 Unhappy/Edge Path (vd: dữ liệu rỗng, sai định dạng, token hết hạn).
2. Không viết câu mơ hồ như "hệ thống xử lý nhanh chóng" — phải viết cụ thể: "hệ thống trả về HTTP 200 trong vòng 200ms".
