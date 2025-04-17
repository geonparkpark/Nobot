# 서버 및 모듈 구성 설명

---

## 1. bot_server
- 사용 기술: Python (discord.py), asyncio
- 주요 기능:
  - Discord 명령어 처리
  - API 서버 호출을 통한 URL 요청
  - Lavalink 노드와 WebSocket 연결 및 세션 유지
- 인터페이스:
  - HTTP 요청 (FastAPI API 서버)
  - WebSocket 연결 (Lavalink)

---

## 2. data_server
- 사용 기술: Python (FastAPI, yt-dlp), Redis
- 주요 기능:
  - 검색어를 기반으로 YouTube 영상 검색 및 스트리밍 URL 추출
  - TTL 기반 캐시 관리
  - Redis PubSub 이벤트 리스너(url-updater) 실행
  - 외부 YouTube 요청은 Proxy 서버를 통해 우회 수행
- 인터페이스:
  - HTTP API (봇 서버 호출용)
  - Redis PubSub 채널 구독

---

## 3. lavalink_server
- 사용 기술: Java (Lavalink), Spring Boot 기반 설정
- 주요 기능:
  - Discord 음성 채널로 오디오 스트리밍 전송 (UDP)
  - 봇 서버와의 WebSocket 통신을 통한 트랙 제어
- 인터페이스:
  - WebSocket 세션 유지 (봇 서버)
  - UDP 스트리밍 (Discord 음성 채널)

---

## 4. proxy_server
- 사용 기술: Nginx, NordVPN, iptables
- 주요 기능:
  - YouTube 요청시 VPN을 통한 IP 우회
  - Nginx를 통한 헤더 설정 및 수신 제어
- 인터페이스:
  - HTTP Proxy (데이터 서버 사용)
  - YouTube 스트리밍 요청 (lavalink)

---