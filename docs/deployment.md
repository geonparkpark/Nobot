# Deployment - 운영 환경 및 배포 구성

---

## 클라우드 인프라 구성

- **플랫폼**: Oracle Cloud Infrastructure (OCI) Free Tier
- **서버 사양**:
  - **Bot Server**: VM.Standard.E2.1.Micro (AMD, OCPU 1/8개, RAM 1GB)
  - **Data Server**: Ampere A1 (ARM, OCPU 1개, RAM 8B)
  - **Proxy Server**: Ampere A1 (ARM, OCPU 1개, RAM 4GB)
  - **Lavalink Server**: Ampere A1 (ARM, OCPU 2개, RAM 8GB)
- **네트워크 구성**:
  - VCN (Virtual Cloud Network) 내 단일 서브넷 사용
  - 각 서버는 고정 프라이빗 IP 할당 및 내부 통신 구성

---

## 컨테이너화 및 배포 방법

- **컨테이너 기술**: `Docker`, `Docker Compose`
- **배포 전략**:
  - **Bot Server**
    - `Dockerfile`을 통해 단독 컨테이너화
    - `.env` 파일 기반 환경변수 설정 후 실행
  
  - **Data Server**
    - `api-server(FastAPI)` 및 `url-updater(Redis PubSub)`, `redis`를 각각 별도 컨테이너로 분리
    - 개별 컨테이너 커스텀 빌드 및 `Docker Compose` 관리 및 배포

  - **Lavalink Server**
    - Lavalink Java 어플리케이션을 `Dockerfile`로 컨테이너화
    - 프록시 서버(Nginx)를 거쳐 YouTube 리소스 스트리밍 요청
    - 서비스 규모 커질 시 간편하게 확장 가능 (**Scale out**)

  - **Proxy Server**
    - `Nginx`, `NordVPN` 컨테이너를 `Docker Compose`로 관리 및 배포
    - 서비스의 모든 외부 요청은 VPN 컨테이너의 네트워크를 통해 외부 통신

- **네트워크 설정**:
  - 모든 컨테이너는 기본적으로 bridge 네트워크 모드 사용
  - 서버 간 통신은 고정 IP + 포트 매핑을 통해 직접 연결

---
