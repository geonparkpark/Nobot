# 노봇 프로젝트

> YOUTUBE 재생 기반 디스코드 노래 봇

---

## 프로젝트 개요

- Discord 음성 채널에서 사용자의 명령으로 YouTube의 음악을 재생합니다.
- 구성: 프록시 서버(Proxy), 데이터 서버(Data), 봇 서버(Bot), 라바링크 서버(Lavalink)

_본 프로젝트는 학습 및 테스트 목적의 비공개 실험용 환경에서만 사용되었으며,<br>
실제 콘텐츠 다운로드 및 제3자 제공은 포함하지 않음._

---

## 기술 스택

- Python(yt-dlp + Discord.py + FastAPI)
- Redis (TTL 관리 + PubSub)
- Lavalink
- Nginx + NordVPN
- OS / Infra: Linux(Ubuntu), Oracle Cloud, Docker

---

## 주요 기능

- `/play <검색어>` 명령으로 YouTube 영상 검색 및 스트리밍 URL 추출
- 추출된 URL은 Redis에 저장 (중복 추출 방지, TTL: 6 ~ 24시간)
- 저장된 URL이 유효하면 즉시 재생, 없으면 yt-dlp로 새로 추출
- Redis TTL 만료 시, PubSub 이벤트를 통해 자동으로 URL 갱신
- Lavalink를 통해 URL 기반 오디오를 Discord 음성 채널로 스트리밍
- YouTube 요청은 NordVPN을 통해 IP 우회

> ⚙️ 서버 별 책임:
> - **bot_server**: Discord 명령 처리, 음성 채널과 라바링크 노드 연결, 재생 요청 전달
> - **data_server**: URL 추출, TTL 이벤트 처리, redis 캐싱
> - **proxy_server**: IP 우회 경로 제공
> - **lavalink_server**: 음악 재생 담당 (Java 기반)

---

## 사용 방법

- ~~디스코드 봇 초대~~
- 재생: '/play'
- 일시정지: '/pause'
- 재개: '/resume'
- 종료: '/stop'
- 재생목록보기: '/queue'
- 건너뛰기: '/skip'

---

## 세부 정보

- [docs/architecture.md](./docs/architecture.md): 시스템 아키텍처 개요
- [docs/problem_solutions.md](./docs/problem_solutions.md): 문제 해결사례
- [docs/modules.md](./docs/modules.md): 서버 및 모듈 설명

---

## 의의 및 한계

- YouTube 접속 및 통신 문제, URL TTL 문제, IP 차단 문제 등을 구조적으로 해결
- yt-dlp 내부 동작을 직접 분석하여 공식 문서에 없는 설정을 찾아냄
- 클라우드 환경에서 서버 간 기능 분산, 프록시 우회, 캐싱 최적화 구성

> ⚠️ 한계:
> - YouTube 자체의 정책 변경이나 Lavalink 의존도에 따라 유지보수 필요
> - 잦은 봇 차단 현상으로 인해 아키텍처 개선이 요구됨 (개인 프로젝트로서의 한계)
> - 추천 알고리즘 및 사용자 맞춤형 기능 부재 (후속 과제로 예정)

