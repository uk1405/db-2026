# 데이터베이스 2026

# 아키텍처 설계

https://nano5.notion.site/355daf211d42807e8f60ca7eca521f69?source=copy_link


---

# 🚀 db_04_my_assets

아키텍처 설계를 학습하기 위한 Flet 프로젝트

## 🛠️ uv 설치 (최초 1회)
이미 설치되어 있다면 안해도 됨

Windows에 설치
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

macOS/Linux에 설치
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## 🏗️ 의존성 설치
프로젝트 폴더에서 아래 명령어를 실행하면 `.venv` 생성되고 패키지 설치됨

```bash
uv sync
```

## ⚙️ .env 파일 생성
프로젝트 폴더에 있는 .env.example 파일을 복사하여 .env 파일을 생성하고 패스워드 등 DBMS 연결 정보 입력

```bash
cp .env.example .env
```

## ▶️ 실행 및 핫 리로드 (Run & Hot Reload)

실행

```bash
uv run flet run
```

핫 리로드

```bash
uv run flet run -r --ignore data/
```

문제가 있을 경우에는 web browser 모드로 실행

```bash
uv run flet run --web -r --ignore data/
```