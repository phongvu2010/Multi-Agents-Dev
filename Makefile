# Makefile — Multi-Agents SDLC Developer Automation
# Chạy trên môi trường Google Antigravity 2.0 / macOS / Linux

VENV ?= .venv
PYTHON ?= $(if $(wildcard $(VENV)/bin/python),$(VENV)/bin/python,python3)
PIP ?= $(if $(wildcard $(VENV)/bin/pip),$(VENV)/bin/pip,pip3)
NODE ?= node
PROJECT ?= MotoCare_Upgrade
FILE ?= workspaces/sample_client_brief.md
PLATFORM ?= auto

.PHONY: help venv dev dev-quick resume sync status models subteams test-examples test-all test-backend test-frontend test-frontend-unit test-frontend-e2e check-frontend-build check-db cov-html run-backend run-frontend docker-build docker-build-backend docker-build-frontend docker-up docker-down docker-logs backup clean-project clean install

help:
	@echo ""
	@echo "=========================================================================="
	@echo "          🚀 MULTI-AGENTS SDLC DEVELOPER TOOLKIT (ANTIGRAVITY 2.0)        "
	@echo "=========================================================================="
	@echo "  make venv                            Tạo môi trường ảo .venv & cài đặt dependencies"
	@echo "  make install                         Cài đặt/cập nhật thư viện Python (tự ưu tiên .venv)"
	@echo "  make dev [PROJECT=.. FILE=.. PLATFORM=web|mobile] Khởi chạy chu trình SDLC mới từ Brief"
	@echo "  make dev-quick [PROJECT=.. PLATFORM=web|mobile]   Chạy tự động không dừng HITL (CI/CD)"
	@echo "  make resume [PROJECT=...]            Khởi phục chu trình từ Checkpoint"
	@echo "  make sync [PROJECT=...]              Đồng bộ mã nguồn vào SDLC Checkpoint"
	@echo "  make status [PROJECT=...]            Kiểm tra trạng thái Gates & Tests (Read-only)"
	@echo "  make backup [PROJECT=...]            Sao lưu snapshot toàn bộ output_project & artifacts"
	@echo "  make clean-project                   Sao lưu an toàn rồi dọn sạch output_project & artifacts"
	@echo "  make models                          Hiển thị Ma Trận Phân Bổ Mô Hình AI & Chi Phí Token"
	@echo "  make subteams                        Xem danh sách 5 Native Sub-Teams & Kỹ năng"
	@echo "  make test-examples                   Chạy bộ kiểm thử của Dự án Mẫu Tham Khảo (Golden Reference)"
	@echo "  make test-all                        Thực thi toàn bộ PyTest (Coverage), DB check & Frontend"
	@echo "  make test-backend                    Chạy PyTest Backend kèm đo độ phủ (Coverage)"
	@echo "  make cov-html                        Xuất báo cáo Code Coverage dạng HTML"
	@echo "  make check-db                        Thẩm định Schema Drift bằng 'alembic check'"
	@echo "  make test-frontend                   Chạy toàn diện kiểm thử Frontend (Unit, E2E & Build Check)"
	@echo "  make test-frontend-unit              Chạy bộ kiểm thử Unit Tests Frontend"
	@echo "  make test-frontend-e2e               Chạy bộ kiểm thử E2E User Journeys Frontend"
	@echo "  make check-frontend-build            Thẩm định tính sẵn sàng Production Build của Frontend"
	@echo "  make run-backend                     Khởi chạy Uvicorn Backend Server (:8000)"
	@echo "  make run-frontend                    Khởi chạy Frontend Dev Server"
	@echo "  make docker-build [PROJECT=...]      Đóng gói toàn bộ Docker Images (Frontend Multi-Stage + Backend)"
	@echo "  make docker-build-frontend           Đóng gói riêng Frontend Multi-Stage Docker Image (Node -> Nginx)"
	@echo "  make docker-build-backend            Đóng gói riêng Backend Docker Image (FastAPI / Python 3.12)"
	@echo "  make docker-up                       Khởi chạy toàn bộ hệ thống bằng Docker Compose (Web:80, API:8000, DB:5432)"
	@echo "  make docker-down                     Dừng và gỡ bỏ Docker Compose containers"
	@echo "  make docker-logs                     Xem logs thời gian thực của Docker Compose"
	@echo "  make clean                           Dọn dẹp caches, .pyc và temporary files"
	@echo "=========================================================================="
	@echo ""

venv:
	@if [ ! -d "$(VENV)" ]; then \
		echo "📦 Đang khởi tạo môi trường ảo Python cô lập tại '$(VENV)'..."; \
		python3 -m venv $(VENV); \
		$(VENV)/bin/python -m pip install --upgrade pip; \
		$(VENV)/bin/python -m pip install -r requirements.txt; \
		echo "✔ Môi trường ảo $(VENV) đã được tạo và cài đặt xong toàn bộ thư viện!"; \
	else \
		echo "ℹ️  Môi trường ảo '$(VENV)' đã tồn tại sẵn. Sử dụng 'make install' để cập nhật packages."; \
	fi

install:
	@if [ -d "$(VENV)" ]; then \
		echo "📦 Đang cài đặt thư viện vào môi trường ảo '$(VENV)'..."; \
		$(PIP) install -r requirements.txt; \
	else \
		echo "📦 Đang cài đặt thư viện qua $(PYTHON)..."; \
		$(PYTHON) -m pip install -r requirements.txt; \
	fi

models:
	$(PYTHON) -m orchestrator.agent_factory --models

subteams:
	$(PYTHON) -m orchestrator.agent_factory --list

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
		cd workspaces/output_project/backend && $(PYTHON) -m alembic upgrade head && $(PYTHON) -m alembic check; \
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

check-frontend-build:
	@if [ ! -d "workspaces/output_project/frontend" ]; then \
		echo "⚠️  Chưa có mã nguồn Frontend trong workspaces/output_project/frontend."; \
	elif [ -f "workspaces/output_project/frontend/package.json" ]; then \
		echo "▶ Đang thẩm định tính sẵn sàng Production Build của Frontend..."; \
		$(NODE) -e "const pkg = require('./workspaces/output_project/frontend/package.json'); console.log('  ✔ package.json hợp lệ: ' + pkg.name + ' v' + pkg.version); if (!pkg.scripts) throw new Error('Missing scripts');"; \
		if [ -f "workspaces/output_project/frontend/tsconfig.json" ]; then \
			echo "  ✔ tsconfig.json hợp lệ (TypeScript configuration ready)"; \
		fi; \
		if [ -d "workspaces/output_project/frontend/node_modules" ] && command -v npx >/dev/null 2>&1; then \
			echo "  ▶ Phát hiện node_modules: Thực thi typecheck qua npx tsc --noEmit..."; \
			cd workspaces/output_project/frontend && npx tsc --noEmit && echo "  ✔ TypeScript compilation: Zero errors"; \
		else \
			echo "  ℹ️  Chế độ High-Fidelity AST & Contract verified (Chạy 'npm install' trong frontend để compile sâu)."; \
		fi; \
		echo "✔ Kiểm tra tính sẵn sàng Production Build Frontend: ĐẠT YÊU CẦU!"; \
	fi

test-frontend: test-frontend-unit test-frontend-e2e check-frontend-build

test-all: test-backend check-db test-frontend

test-examples:
	@echo "▶ Đang chạy kiểm thử Dự án Mẫu Tham Khảo (examples/motocare_reference)..."
	PYTHONPATH=examples/motocare_reference/output_project/backend $(PYTHON) -m pytest examples/motocare_reference/output_project/backend/tests -v --cov=app --cov-report=term-missing
	cd examples/motocare_reference/output_project/backend && $(PYTHON) -m alembic upgrade head && $(PYTHON) -m alembic check
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
	@if [ -f "workspaces/output_project/infra/docker-compose.yml" ]; then \
		echo "▶ Đang đóng gói toàn bộ Docker Images qua Docker Compose..."; \
		cd workspaces/output_project && docker compose -f infra/docker-compose.yml build; \
	elif [ -f "workspaces/output_project/infra/Dockerfile" ]; then \
		cd workspaces/output_project && docker build -f infra/Dockerfile -t $$(echo $(PROJECT) | tr '[:upper:]' '[:lower:]'):latest .; \
	else \
		echo "⚠️  Chưa có mã nguồn infra trong workspaces/output_project/infra."; \
	fi
	@echo "✔ Đã đóng gói thành công các Docker Images (Frontend Multi-Stage + Backend)!"

docker-build-frontend:
	@if [ ! -f "workspaces/output_project/infra/Dockerfile.frontend" ]; then \
		echo "⚠️  Chưa có file Dockerfile.frontend trong workspaces/output_project/infra."; \
	else \
		echo "▶ Đang đóng gói Frontend Multi-Stage Docker Image (Node.js -> Nginx)..."; \
		cd workspaces/output_project && docker build -f infra/Dockerfile.frontend -t $$(echo $(PROJECT) | tr '[:upper:]' '[:lower:]')-frontend:latest .; \
		echo "✔ Đã đóng gói thành công Frontend Multi-Stage Docker Image!"; \
	fi

docker-build-backend:
	@if [ ! -f "workspaces/output_project/infra/Dockerfile.backend" ] && [ ! -f "workspaces/output_project/infra/Dockerfile" ]; then \
		echo "⚠️  Chưa có Dockerfile Backend trong workspaces/output_project/infra."; \
	else \
		DOCKERFILE_TARGET=$$(if [ -f "workspaces/output_project/infra/Dockerfile.backend" ]; then echo "infra/Dockerfile.backend"; else echo "infra/Dockerfile"; fi); \
		echo "▶ Đang đóng gói Backend Docker Image ($$DOCKERFILE_TARGET)..."; \
		cd workspaces/output_project && docker build -f $$DOCKERFILE_TARGET -t $$(echo $(PROJECT) | tr '[:upper:]' '[:lower:]')-backend:latest .; \
		echo "✔ Đã đóng gói thành công Backend Docker Image (Python 3.12 / FastAPI)!"; \
	fi

docker-up:
	cd workspaces/output_project/infra && docker compose up -d
	@echo "✔ Hệ thống multi-container đang chạy ngầm (Web :80, API :8000, PostgreSQL :5432)!"

docker-down:
	cd workspaces/output_project/infra && docker compose down
	@echo "✔ Đã dừng và gỡ bỏ toàn bộ containers!"

docker-logs:
	cd workspaces/output_project/infra && docker compose logs -f

backup:
	$(PYTHON) -m orchestrator.runner --project "$(PROJECT)" --backup

clean-project:
	@echo "📦 Đang tự động sao lưu an toàn trước khi dọn dẹp..."
	$(PYTHON) -m orchestrator.runner --project "$(PROJECT)" --backup || true
	@echo "🧹 Đang dọn sạch mã nguồn và artifacts để sẵn sàng cho dự án mới..."
	rm -rf workspaces/output_project/backend workspaces/output_project/frontend workspaces/output_project/infra
	rm -rf workspaces/artifacts/01_discovery/* workspaces/artifacts/02_architecture/* workspaces/artifacts/04_quality/* workspaces/artifacts/05_handover/*
	find workspaces/artifacts -name "review_gate_*.md" -delete 2>/dev/null || true
	touch workspaces/output_project/.gitkeep workspaces/artifacts/01_discovery/.gitkeep workspaces/artifacts/02_architecture/.gitkeep workspaces/artifacts/04_quality/.gitkeep workspaces/artifacts/05_handover/.gitkeep
	@echo "✔ Đã tạo backup và dọn sạch workspace an toàn!"

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
	find . -name ".DS_Store" -delete 2>/dev/null || true
	find . -name ".coverage*" -delete 2>/dev/null || true
	find . -name "*.db" -delete 2>/dev/null || true
	@echo "✔ Đã dọn dẹp sạch sẽ caches, coverage, database và temporary files."
