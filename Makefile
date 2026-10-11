# Makefile — Multi-Agents SDLC Developer Automation
# Chạy trên môi trường Google Antigravity 2.0 / macOS / Linux

PYTHON ?= python3
NODE ?= node
PROJECT ?= MotoCare_Upgrade
FILE ?= workspaces/sample_client_brief.md

.PHONY: help dev dev-quick resume sync status test-all test-backend test-frontend run-backend run-frontend clean install

help:
	@echo ""
	@echo "=========================================================================="
	@echo "          🚀 MULTI-AGENTS SDLC DEVELOPER TOOLKIT (ANTIGRAVITY 2.0)        "
	@echo "=========================================================================="
	@echo "  make dev [PROJECT=... FILE=...]      Khởi chạy chu trình SDLC mới từ Brief"
	@echo "  make dev-quick [PROJECT=... FILE=..] Chạy tự động không dừng HITL (CI/CD)"
	@echo "  make resume [PROJECT=...]            Khôi phục chu trình từ Checkpoint"
	@echo "  make sync [PROJECT=...]              Đồng bộ mã nguồn vào SDLC Checkpoint"
	@echo "  make status [PROJECT=...]            Kiểm tra trạng thái Gates & Tests (Read-only)"
	@echo "  make test-all                        Thực thi toàn bộ PyTest & Frontend Jest"
	@echo "  make test-backend                    Chạy PyTest Backend FastAPI"
	@echo "  make test-frontend                   Chạy bộ kiểm thử Frontend Node.js"
	@echo "  make run-backend                     Khởi chạy Uvicorn Backend Server (:8000)"
	@echo "  make run-frontend                    Khởi chạy Frontend Dev Server"
	@echo "  make clean                           Dọn dẹp caches, .pyc và temporary files"
	@echo "  make install                         Cài đặt thư viện phụ thuộc Python"
	@echo "=========================================================================="
	@echo ""

install:
	$(PYTHON) -m pip install -r requirements.txt

dev:
	$(PYTHON) -m orchestrator.runner --project "$(PROJECT)" --input-file "$(FILE)"

dev-quick:
	$(PYTHON) -m orchestrator.runner --project "$(PROJECT)" --input-file "$(FILE)" --no-hitl

resume:
	$(PYTHON) -m orchestrator.runner --project "$(PROJECT)" --resume

sync:
	$(PYTHON) -m orchestrator.sync_state --project "$(PROJECT)"

status:
	$(PYTHON) -m orchestrator.sync_state --project "$(PROJECT)" --check-only

test-backend:
	$(PYTHON) -m pytest workspaces/output_project/backend/tests -v

test-frontend:
	$(NODE) workspaces/output_project/frontend/run_tests.cjs

test-all: test-backend test-frontend

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
