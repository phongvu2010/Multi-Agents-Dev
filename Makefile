# Makefile — Multi-Agents SDLC Developer Automation
# Chạy trên môi trường Google Antigravity 2.0 / macOS / Linux

PYTHON ?= python3
NODE ?= node
PROJECT ?= MotoCare_Upgrade
FILE ?= workspaces/sample_client_brief.md
PLATFORM ?= auto

.PHONY: help dev dev-quick resume sync status test-all test-backend test-frontend test-frontend-unit test-frontend-e2e check-db cov-html run-backend run-frontend clean install

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
	@echo "  make test-all                        Thực thi toàn bộ PyTest (Coverage) & Frontend (Unit+E2E)"
	@echo "  make test-backend                    Chạy PyTest Backend kèm đo độ phủ (Coverage)"
	@echo "  make cov-html                        Xuất báo cáo Code Coverage dạng HTML"
	@echo "  make check-db                        Thẩm định Schema Drift bằng 'alembic check'"
	@echo "  make test-frontend                   Chạy toàn diện kiểm thử Frontend (Unit + E2E)"
	@echo "  make test-frontend-unit              Chạy bộ kiểm thử Unit Tests Frontend"
	@echo "  make test-frontend-e2e               Chạy bộ kiểm thử E2E User Journeys Frontend"
	@echo "  make run-backend                     Khởi chạy Uvicorn Backend Server (:8000)"
	@echo "  make run-frontend                    Khởi chạy Frontend Dev Server"
	@echo "  make clean                           Dọn dẹp caches, .pyc và temporary files"
	@echo "  make install                         Cài đặt thư viện phụ thuộc Python"
	@echo "=========================================================================="
	@echo ""

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
	PYTHONPATH=workspaces/output_project/backend $(PYTHON) -m pytest workspaces/output_project/backend/tests -v --cov=app --cov-report=term-missing

cov-html:
	PYTHONPATH=workspaces/output_project/backend $(PYTHON) -m pytest workspaces/output_project/backend/tests -v --cov=app --cov-report=html:workspaces/artifacts/04_quality/htmlcov
	@echo "✔ Đã xuất báo cáo HTML coverage tại: workspaces/artifacts/04_quality/htmlcov/index.html"

check-db:
	cd workspaces/output_project/backend && $(PYTHON) -m alembic check

test-frontend-unit:
	$(NODE) workspaces/output_project/frontend/run_tests.cjs

test-frontend-e2e:
	$(NODE) workspaces/output_project/frontend/run_e2e_tests.cjs

test-frontend: test-frontend-unit test-frontend-e2e

test-all: test-backend check-db test-frontend

run-backend:
	PYTHONPATH=workspaces/output_project/backend $(PYTHON) -m uvicorn app.main:app --reload --app-dir workspaces/output_project/backend --port 8000

run-frontend:
	@if [ -f workspaces/output_project/frontend/setup_dev.sh ]; then \
		bash workspaces/output_project/frontend/setup_dev.sh; \
	elif [ -f workspaces/output_project/frontend/index.html ]; then \
		cd workspaces/output_project/frontend && npm install && npm run dev; \
	else \
		cd workspaces/output_project/frontend && npm install && npx expo start; \
	fi

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
	find . -name ".DS_Store" -delete 2>/dev/null || true
	@echo "✔ Đã dọn dẹp sạch sẽ caches và temporary files."
