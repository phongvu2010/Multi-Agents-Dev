from pathlib import Path
from rich.console import Console
from orchestrator.state import SDLCState, SDLCPhase
from orchestrator.agent_factory import AgentFactory

console = Console()


async def run_engineering_phase(
    state: SDLCState,
    factory: AgentFactory,
    project_workspace: Path,
    review_feedback: str = ""
) -> SDLCState:
    """Thực thi Sub-Team 3: Core Engineering (Backend, Frontend, DevOps)."""
    console.print("\n[bold cyan]▶ ĐANG CHẠY SUB-TEAM 3: CORE ENGINEERING & IMPLEMENTATION[/bold cyan]")
    
    project_workspace.mkdir(parents=True, exist_ok=True)
    backend_dir = project_workspace / "backend"
    frontend_dir = project_workspace / "frontend"
    devops_dir = project_workspace / "infra"
    
    backend_dir.mkdir(parents=True, exist_ok=True)
    frontend_dir.mkdir(parents=True, exist_ok=True)
    devops_dir.mkdir(parents=True, exist_ok=True)
    
    agent = factory.create_engineering_team(state.selected_tech_stack)
    
    prompt = f"""
Hãy triển khai mã nguồn hoàn chỉnh cho dự án '{state.project_name}'.
Tech Stack đã duyệt:
- Backend: {state.selected_tech_stack.get('backend', 'Python (FastAPI)')}
- Frontend/Mobile: {state.selected_tech_stack.get('frontend_mobile', 'React Native')}

{"GÓP Ý CHỈNH SỬA TỪ CODE REVIEW / QA (FIX BUG): " + review_feedback if review_feedback else ""}

Yêu cầu kỹ thuật:
1. Viết code sạch, phân tầng (Controller -> Service -> Repository).
2. Viết type annotations đầy đủ, tuân thủ PEP 8 và TypeScript Strict.
3. Cung cấp file docker-compose.yml và hướng dẫn chạy.
"""
    console.print("  [dim]• Đang kích hoạt Backend Engineer, Frontend Engineer và DevOps Agents...[/dim]")
    async with agent:
        response = await agent.chat(prompt)
        await response.text()

    # 1. Sinh mã nguồn Backend (FastAPI mẫu)
    backend_main = """from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import uvicorn

app = FastAPI(
    title="Core Service API",
    description="Hệ thống tự động sinh bởi AI Multi-Agent SDLC",
    version="1.0.0"
)

class HealthResponse(BaseModel):
    status: str
    version: str

@app.get("/api/v1/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    \"\"\"Kiểm tra trạng thái sẵn sàng của dịch vụ.\"\"\"
    return HealthResponse(status="healthy", version="1.0.0")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
"""
    (backend_dir / "main.py").write_text(backend_main, encoding="utf-8")
    (backend_dir / "requirements.txt").write_text("fastapi>=0.110.0\nuvicorn>=0.28.0\npydantic>=2.6.0\n", encoding="utf-8")

    # 2. Sinh mã nguồn Frontend / Mobile (React Native mẫu)
    frontend_app = """import React from 'react';
import { StyleSheet, Text, View, SafeAreaView } from 'react-native';

export default function App() {
  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.card}>
        <Text style={styles.title}>Multi-Agents Mobile App</Text>
        <Text style={styles.subtitle}>Sản phẩm sinh tự động bởi AI Multi-Agent System</Text>
        <Text style={styles.status}>Backend Status: Connected (FastAPI)</Text>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0f172a',
    alignItems: 'center',
    justifyContent: 'center',
  },
  card: {
    padding: 24,
    borderRadius: 12,
    backgroundColor: '#1e293b',
    alignItems: 'center',
  },
  title: {
    fontSize: 22,
    fontWeight: 'bold',
    color: '#38bdf8',
  },
  subtitle: {
    fontSize: 14,
    color: '#94a3b8',
    marginTop: 8,
  },
  status: {
    fontSize: 12,
    color: '#4ade80',
    marginTop: 16,
  },
});
"""
    (frontend_dir / "App.tsx").write_text(frontend_app, encoding="utf-8")
    (frontend_dir / "package.json").write_text('{"name": "mobile-app", "version": "1.0.0", "private": true}', encoding="utf-8")

    # 3. Sinh cấu hình DevOps
    docker_compose = """version: '3.8'

services:
  backend:
    build:
      context: ../backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=production
    restart: unless-stopped
"""
    (devops_dir / "docker-compose.yml").write_text(docker_compose, encoding="utf-8")
    
    backend_dockerfile = """FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
"""
    (backend_dir / "Dockerfile").write_text(backend_dockerfile, encoding="utf-8")

    state.artifacts["backend_source"] = str(backend_dir)
    state.artifacts["frontend_source"] = str(frontend_dir)
    state.artifacts["infra_source"] = str(devops_dir)
    state.current_phase = SDLCPhase.QA_VERIFICATION
    
    console.print(f"  [bold green]✓ Hoàn thành Sub-Team 3. Mã nguồn đã được sinh tại:[/bold green] {project_workspace}")
    return state
