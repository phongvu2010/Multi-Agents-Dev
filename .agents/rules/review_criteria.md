# TIÊU CHÍ ĐÁNH GIÁ VÀ REVIEW MÃ NGUỒN (REVIEW CRITERIA)

Mỗi đoạn mã nguồn sinh ra bởi Dev Agents phải vượt qua 5 tiêu chí sau:

| STT | Tiêu chí | Trọng số | Yêu cầu tối thiểu để Pass |
|---|---|---|---|
| 1 | **Contract Adherence** | Bắt buộc | Request/Response khớp 100% với `openapi.yaml`. |
| 2 | **Security & Guardrails** | Bắt buộc | 0 lỗi bảo mật nghiêm trọng (No hardcoded secrets, No SQLi, Proper Auth). |
| 3 | **Tech Stack Compatibility** | Cao | Tuân thủ quyết định của System Architect (ưu tiên Python/FastAPI, Node.js, React Native). |
| 4 | **Test Coverage & Quality** | Cao | Unit test đạt tối thiểu **80% coverage** và 100% test cases pass. |
| 5 | **Clean Code & Readability** | Trung bình | Code có chú thích rõ ràng, tuân thủ PEP 8 (Python) hoặc ESLint/Prettier (JS/TS). |
