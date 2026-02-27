/**
 * 대시보드 메인 스크립트
 */

// 상태 변수
let currentSelectedService = null;
let autoRefreshEnabled = true;
let autoRefreshInterval = null;
const REFRESH_INTERVAL = 2000; // 2초

/**
 * 초기화
 */
document.addEventListener('DOMContentLoaded', async () => {
    // 저장된 토큰 로드
    if (API.loadToken()) {
        try {
            await API.auth.verify();
            showDashboard();
            startAutoRefresh();
        } catch (error) {
            console.error('토큰 검증 실패:', error);
            showLoginPage();
        }
    } else {
        showLoginPage();
    }
});

/**
 * 로그인 처리
 */
async function handleLogin(event) {
    event.preventDefault();
    const password = document.getElementById('password').value;
    const errorDiv = document.getElementById('login-error');

    try {
        errorDiv.style.display = 'none';
        const response = await API.auth.login(password);
        API.setToken(response.token);
        showDashboard();
        startAutoRefresh();
    } catch (error) {
        errorDiv.style.display = 'block';
        errorDiv.textContent = error.message;
    }
}

/**
 * 로그아웃
 */
async function logout() {
    try {
        await API.auth.logout();
        API.clearToken();
        stopAutoRefresh();
        showLoginPage();
        document.getElementById('password').value = '';
    } catch (error) {
        console.error('로그아웃 실패:', error);
        // 로컬 로그아웃 진행
        API.clearToken();
        stopAutoRefresh();
        showLoginPage();
    }
}

/**
 * UI 전환
 */
function showLoginPage() {
    document.getElementById('login-page').style.display = 'block';
    document.getElementById('dashboard-page').style.display = 'none';
}

function showDashboard() {
    document.getElementById('login-page').style.display = 'none';
    document.getElementById('dashboard-page').style.display = 'block';
    loadDashboardData();
}

/**
 * 대시보드 데이터 로드
 */
async function loadDashboardData() {
    try {
        // 병렬로 데이터 로드
        const [dashboardData, servicesData] = await Promise.all([
            API.status.getDashboard(),
            API.services.getAll(),
        ]);

        updateSystemStats(dashboardData.system);
        updateServicesList(dashboardData.services);
        updateServiceSummary(dashboardData.summary);
        updateLogServiceSelect(dashboardData.services);
        loadSelectedServiceLogs();
    } catch (error) {
        console.error('대시보드 데이터 로드 실패:', error);
    }
}

/**
 * 시스템 상태 업데이트
 */
function updateSystemStats(system) {
    const cpuPercent = system.cpu_percent.toFixed(1);
    const memoryPercent = system.memory_percent.toFixed(1);
    const diskPercent = system.disk_percent.toFixed(1);

    document.getElementById('cpu-usage').textContent = `${cpuPercent}%`;
    document.getElementById('memory-usage').textContent = `${memoryPercent}%`;
    document.getElementById('disk-usage').textContent = `${diskPercent}%`;

    document.getElementById('cpu-progress').style.width = cpuPercent + '%';
    document.getElementById('memory-progress').style.width = memoryPercent + '%';
    document.getElementById('disk-progress').style.width = diskPercent + '%';
}

/**
 * 서비스 요약 업데이트
 */
function updateServiceSummary(summary) {
    document.getElementById('running-services').textContent =
        `${summary.running_services}/${summary.total_services}`;
}

/**
 * 서비스 목록 업데이트
 */
function updateServicesList(services) {
    const container = document.getElementById('services-list');

    if (!services || services.length === 0) {
        container.innerHTML = '<div class="empty-message">등록된 서비스가 없습니다</div>';
        return;
    }

    container.innerHTML = services.map(service => {
        const status = service.running ? 'running' : 'stopped';
        const statusText = service.running ? '실행 중' : '중지됨';
        const statusClass = service.running ? 'running' : 'stopped';

        let info = '';
        if (service.running && service.info) {
            info = `
                <div class="service-info">
                    <div><span class="info-label">PID:</span> <span class="info-value">${service.info.pid}</span></div>
                    <div><span class="info-label">CPU:</span> <span class="info-value">${service.info.cpu_percent.toFixed(1)}%</span></div>
                    <div><span class="info-label">메모리:</span> <span class="info-value">${service.info.memory_mb.toFixed(1)} MB</span></div>
                    <div><span class="info-label">시작 시간:</span> <span class="info-value">${new Date(service.info.create_time).toLocaleString('ko-KR')}</span></div>
                </div>
            `;
        }

        return `
            <div class="service-card ${statusClass}">
                <div class="service-header">
                    <div class="service-name">${service.name}</div>
                    <span class="service-status ${statusClass}">${statusText}</span>
                </div>
                <div class="service-description">${service.description}</div>
                ${info}
                <div class="service-controls">
                    ${service.running ?
                        `<button class="btn btn-danger btn-small" onclick="stopService('${service.id}')">중지</button>
                         <button class="btn btn-primary btn-small" onclick="restartService('${service.id}')">재시작</button>` :
                        `<button class="btn btn-success btn-small" onclick="startService('${service.id}')">시작</button>`
                    }
                </div>
            </div>
        `;
    }).join('');
}

/**
 * 로그 서비스 선택 업데이트
 */
function updateLogServiceSelect(services) {
    const select = document.getElementById('log-service-select');
    const currentValue = select.value;

    select.innerHTML = '<option value="">-- 서비스 선택 --</option>';

    if (services && services.length > 0) {
        services.forEach(service => {
            const option = document.createElement('option');
            option.value = service.id;
            option.textContent = service.name;
            select.appendChild(option);
        });

        // 이전 선택값 복원
        if (currentValue) {
            select.value = currentValue;
        }
    }
}

/**
 * 로그 서비스 변경
 */
function changeLogService() {
    currentSelectedService = document.getElementById('log-service-select').value;
    loadSelectedServiceLogs();
}

/**
 * 선택된 서비스 로그 로드
 */
async function loadSelectedServiceLogs() {
    if (!currentSelectedService) {
        document.getElementById('logs-container').innerHTML =
            '<div class="log-line">서비스를 선택하세요</div>';
        return;
    }

    try {
        const response = await API.logs.get(currentSelectedService, 100);
        displayLogs(response.logs);
    } catch (error) {
        console.error('로그 로드 실패:', error);
        document.getElementById('logs-container').innerHTML =
            '<div class="log-line" style="color: #f48771;">로그를 불러올 수 없습니다</div>';
    }
}

/**
 * 로그 표시
 */
function displayLogs(logs) {
    const container = document.getElementById('logs-container');

    if (!logs || logs.length === 0) {
        container.innerHTML = '<div class="log-line">로그가 없습니다</div>';
        return;
    }

    container.innerHTML = logs.map(log => {
        // 로그 형식: [2024-01-01 12:00:00] message
        const logClass = getLogClass(log);
        return `<div class="log-line ${logClass}">${escapeHtml(log)}</div>`;
    }).join('');

    // 자동 스크롤
    container.scrollTop = container.scrollHeight;
}

/**
 * 로그 클래스 결정
 */
function getLogClass(log) {
    if (log.toLowerCase().includes('error')) return 'log-error';
    if (log.toLowerCase().includes('warning')) return 'log-warning';
    if (log.toLowerCase().includes('success')) return 'log-success';
    return '';
}

/**
 * HTML 이스케이프
 */
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

/**
 * 로그 초기화
 */
async function clearLogs() {
    if (!currentSelectedService) {
        alert('서비스를 선택하세요');
        return;
    }

    if (!confirm('로그를 초기화하시겠습니까?')) {
        return;
    }

    try {
        await API.logs.clear(currentSelectedService);
        loadSelectedServiceLogs();
    } catch (error) {
        alert('로그 초기화 실패: ' + error.message);
    }
}

/**
 * 자동 새로고침 토글
 */
function toggleAutoRefresh() {
    autoRefreshEnabled = !autoRefreshEnabled;
    if (autoRefreshEnabled) {
        startAutoRefresh();
        alert('자동 새로고침 활성화됨');
    } else {
        stopAutoRefresh();
        alert('자동 새로고침 비활성화됨');
    }
}

/**
 * 자동 새로고침 시작
 */
function startAutoRefresh() {
    if (autoRefreshInterval) return;

    autoRefreshInterval = setInterval(() => {
        if (autoRefreshEnabled) {
            loadDashboardData();
        }
    }, REFRESH_INTERVAL);
}

/**
 * 자동 새로고침 중지
 */
function stopAutoRefresh() {
    if (autoRefreshInterval) {
        clearInterval(autoRefreshInterval);
        autoRefreshInterval = null;
    }
}

/**
 * 서비스 시작
 */
async function startService(serviceId) {
    try {
        await API.services.start(serviceId);
        loadDashboardData();
    } catch (error) {
        alert('서비스 시작 실패: ' + error.message);
    }
}

/**
 * 서비스 중지
 */
async function stopService(serviceId) {
    if (!confirm('서비스를 중지하시겠습니까?')) {
        return;
    }

    try {
        await API.services.stop(serviceId);
        loadDashboardData();
    } catch (error) {
        alert('서비스 중지 실패: ' + error.message);
    }
}

/**
 * 서비스 재시작
 */
async function restartService(serviceId) {
    if (!confirm('서비스를 재시작하시겠습니까?')) {
        return;
    }

    try {
        await API.services.restart(serviceId);
        loadDashboardData();
    } catch (error) {
        alert('서비스 재시작 실패: ' + error.message);
    }
}
