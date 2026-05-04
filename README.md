# 데이터베이스 2026

# Flet 기초

https://nano5.notion.site/Flet-34fdaf211d428077aec0f5d2cff2c1a9?source=copy_link


---

# 🚀 db_01_flet (Flet + uv)

uv를 사용하여 관리되는 Flet 프로젝트입니다.

## 🛠️ 설치 및 설정 (Install)

이 프로젝트는 `uv`를 사용하여 가상환경과 패키지를 관리합니다.

1. **uv 설치** (최초 1회)
   - Windows: `powershell -c "irm https://astral.sh/uv/install.ps1 | iex"`
   - macOS/Linux: `curl -LsSf https://astral.sh/uv/install.sh | sh`

2. **의존성 설치**
   프로젝트 폴더에서 아래 명령어를 실행하면 `.venv` 생성과 패키지 설치가 완료됩니다.
   ```bash
   uv sync
   ```

## ▶️ 실행 및 핫 리로드 (Run & Hot Reload)

### 1. 일반 실행
```bash
uv run main.py
```

### 2. 핫 리로드 실행 (추천)
개발 중에 코드를 수정하면 자동으로 앱이 재시작됩니다. 
```bash
uv run flet run main.py -d
```
*(명령어 뒤의 `-d` 또는 `--development` 옵션이 핫 리로드를 활성화합니다.)*

---
