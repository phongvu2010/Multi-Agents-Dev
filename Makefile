# Makefile — Multi-Agents SDLC Developer Automation
# Chạy trên môi trường Google Antigravity 2.0 / macOS / Linux

PYTHON ?= python3
NODE ?= node
PROJECT ?= MotoCare_Upgrade
FILE ?= workspaces/sample_client_brief.md
PLATFORM ?= auto

.PHONY: help dev dev-quick resume sync status models subteams test-examples test-all test-backend test-frontend test-frontend-unit test-frontend-e2e check-db cov-html run-backend run-frontend docker-build docker-up docker-down docker-logs clean install

help:
	@echo ""
	@echo "=========================================================================="
	@echo "          🚀 MULTI-AGENTS SDLC DEVELOPER TOOLKIT (ANTIGRAVITY 2.0)        "
	@echo "=========================================================================="
	@echo "  make dev [PROJECT=.. FILE=.. PLATFORM=web|mobile] Khởi chạy chu trình SDLC mới từ Brief"
	@echo "  make dev-quick [PROJECT=.. PLATFORM=web|mobile]   Chạy tự động không dừng HITL (CI/CD)"
	@echo "  make resume [PROJECT=...]            Khởi phục chu trình từ Checkpoint"
	@echo "  make sync [PROJECT=...]              Đồng bộ mã nguồn vào SDLC Checkpoint"
	@echo "  make status [PROJECT=...]            Kiểm tra trạng thái Gates & Tests (Read-only)"
	@echo "  make models                          Hiển thị Ma Trận Phân Bổ Mô Hình AI & Chi Phí Token"
	@echo "  make subteams                        Xem danh sách 5 Native Sub-Teams & Kỹ năng"
	@echo "  make test-examples                   Chạy bộ kiểm thử của Dự án Mẫu Tham Khảo (Golden Reference)"
	@echo "  make test-all                        Thực thi toàn bộ PyTest (Coverage) & Frontend (Unit+E2E)"
	@echo "  make test-backend                    Chạy PyTest Backend kèm đo độ phủ (Coverage)"
	@echo "  make cov-html                        Xuất báo cáo Code Coverage dạng HTML"
	@echo "  make check-db                        Thẩm định Schema Drift bằng 'alembic check'"
	@echo "  make test-frontend                   Chạy toàn diện kiểm thử Frontend (Unit + E2E)"
	@echo "  make test-frontend-unit              Chạy bộ kiểm thử Unit Tests Frontend"
	@echo "  make test-frontend-e2e               Chạy bộ kiểm thử E2E User Journeys Frontend"
	@echo "  make run-backend                     Khởi chạy Uvicorn Backend Server (:8000)"
	@echo "  make run-frontend                    Khởi chạy Frontend Dev Server"
	@echo "  make docker-build [PROJECT=...]      Đóng gói Docker Image cho Backend"
	@echo "  make docker-up                       Khởi chạy toàn bộ hệ thống bằng Docker Compose"
	@echo "  make docker-down                     Dừng và gỡ bỏ Docker Compose containers"
	@echo "  make docker-logs                     Xem logs thời gian thực của Docker Compose"
	@echo "  make clean                           Dọn dẹp caches, .pyc và temporary files"
	@echo "  make install                         Cài đặt thư viện phụ thuộc Python"
	@echo "=========================================================================="
	@echo ""

models:
	$(PYTHON) -m orchestrator.agent_factory --models

subteams:
	$(PYTHON) -m orchestrator.agent_factory --list

install:
	$(PYTHON) -m pip install -r requirements.txt

dev:
	$(PYTHON) -m orchestrator.runner --project "$(PROJECT)" --input-file "$(FILE)" --platform "$(PLATFORM)"

dev-quick:
	$(PYTHON) -m orchestrator.runner --project "$(PROJECT)" --input-file "$(FILE)" --platform "$(PLATFORM)" --no-hitl

resume:
	$(PYTHON) -m orchestrator.runner --project "$(PROJECT)" --resume

sync:
	$(PYTHON) -m orchestrator.sync_state --project "$(PROJECT)"

status:
	$(PYTHON) -m orchestrator.sync_state --project "$(PROJECT)" --check-only

test-backend:
	@if [ ! -d "workspaces/output_project/backend/tests" ]; then \
		echo "⚠️  Chưa có mã nguồn Backend trong workspaces/output_project/backend."; \
		echo "👉 Khởi chạy dự án mới bằng: make dev PROJECT=\"Tên_Dự_Án\" (hoặc test mẫu: make test-examples)"; \
	else \
		PYTHONPATH=workspaces/output_project/backend $(PYTHON) -m pytest workspaces/output_project/backend/tests -v --cov=app --cov-report=term-missing; \
	fi

cov-html:
	@if [ ! -d "workspaces/output_project/backend/tests" ]; then \
		echo "⚠️  Chưa có mã nguồn Backend để xuất báo cáo HTML coverage."; \
	else \
		PYTHONPATH=workspaces/output_project/backend $(PYTHON) -m pytest workspaces/output_project/backend/tests -v --cov=app --cov-report=html:workspaces/artifacts/04_quality/htmlcov; \
		echo "✔ Đã xuất báo cáo HTML coverage tại: workspaces/artifacts/04_quality/htmlcov/index.html"; \
	fi

check-db:
	@if [ ! -f "workspaces/output_project/backend/alembic.ini" ]; then \
		echo "⚠️  Chưa có cấu hình Alembic trong workspaces/output_project/backend."; \
	else \
		cd workspaces/output_project/backend && $(PYTHON) -m alembic check; \
	fi

test-frontend-unit:
	@if [ ! -f "workspaces/output_project/frontend/run_tests.cjs" ]; then \
		echo "⚠️  Chưa có mã nguồn Frontend Unit Tests trong workspaces/output_project/frontend."; \
	else \
		$(NODE) workspaces/output_project/frontend/run_tests.cjs; \
	fi

test-frontend-e2e:
	@if [ ! -f "workspaces/output_project/frontend/run_e2e_tests.cjs" ]; then \
		echo "⚠️  Chưa có kịch bản Frontend E2E trong workspaces/output_project/frontend."; \
	else \
		$(NODE) workspaces/output_project/frontend/run_e2e_tests.cjs; \
	fi

test-frontend: test-frontend-unit test-frontend-e2e

test-all: test-backend check-db test-frontend

test-examples:
	@echo "▶ Đang chạy kiểm thử Dự án Mẫu Tham Khảo (examples/motocare_reference)..."
	PYTHONPATH=examples/motocare_reference/output_project/backend $(PYTHON) -m pytest examples/motocare_reference/output_project/backend/tests -v --cov=app --cov-report=term-missing
	cd examples/motocare_reference/output_project/backend && $(PYTHON) -m alembic check
	$(NODE) examples/motocare_reference/output_project/frontend/run_tests.cjs
	$(NODE) examples/motocare_reference/output_project/frontend/run_e2e_tests.cjs
	@echo "✔ Toàn bộ test suite của dự án mẫu Golden Reference ĐÃ PASS 100%!"

run-backend:
	@if [ ! -d "workspaces/output_project/backend/app" ]; then \
		echo "⚠️  Chưa có mã nguồn Backend để khởi chạy."; \
		echo "👉 Khởi chạy dự án mới bằng: make dev PROJECT=\"Tên_Dự_Án\""; \
	else \
		PYTHONPATH=workspaces/output_project/backend $(PYTHON) -m uvicorn app.main:app --reload --app-dir workspaces/output_project/backend --port 8000; \
	fi

run-frontend:
	@if [ -f workspaces/output_project/frontend/setup_dev.sh ]; then \
		bash workspaces/output_project/frontend/setup_dev.sh; \
	elif [ -f workspaces/output_project/frontend/index.html ]; then \
		cd workspaces/output_project/frontend && npm install && npm run dev; \
	elif [ -f workspaces/output_project/frontend/App.tsx ]; then \
		cd workspaces/output_project/frontend && npm install && npx expo start; \
	else \
		echo "⚠️  Chưa có mã nguồn Frontend để khởi chạy."; \
		echo "👉 Khởi chạy dự án mới bằng: make dev PROJECT=\"Tên_Dự_Án\""; \
	fi

docker-build:
	cd workspaces/output_project && docker build -f infra/Dockerfile -t $$(echo $(PROJECT) | tr '[:upper:]' '[:lower:]'):latest .
	@echo "✔ Đã đóng gói thành công Docker image cho $(PROJECT)!"

docker-up:
	cd workspaces/output_project/infra && docker compose up -d
	@echo "✔ Hệ thống multi-container đang chạy ngầm (API :8000, PostgreSQL :5432)!"

docker-down:
	cd workspaces/output_project/infra && docker compose down
	@echo "✔ Đã dừng và gỡ bỏ toàn bộ containers!"

docker-logs:
	cd workspaces/output_project/infra && docker compose logs -f

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
	find . -name ".DS_Store" -delete 2>/dev/null || true
	@echo "✔ Đã dọn dẹp sạch sẽ caches và temporary files."
