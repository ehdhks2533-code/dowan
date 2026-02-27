/**
 * API 통신 모듈
 */
const API = {
    baseURL: '/api',
    token: null,

    /**
     * API 호출
     */
    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const config = {
            headers: {
                'Content-Type': 'application/json',
            },
            ...options,
        };

        if (this.token) {
            config.headers['Authorization'] = `Bearer ${this.token}`;
        }

        try {
            const response = await fetch(url, config);
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.message || `API 오류: ${response.status}`);
            }

            return data;
        } catch (error) {
            console.error(`API 요청 실패 (${endpoint}):`, error);
            throw error;
        }
    },

    /**
     * 토큰 저장
     */
    setToken(token) {
        this.token = token;
        localStorage.setItem('auth_token', token);
    },

    /**
     * 저장된 토큰 로드
     */
    loadToken() {
        this.token = localStorage.getItem('auth_token');
        return this.token;
    },

    /**
     * 토큰 제거
     */
    clearToken() {
        this.token = null;
        localStorage.removeItem('auth_token');
    },

    /**
     * 인증
     */
    auth: {
        login: (password) => API.request('/auth/login', {
            method: 'POST',
            body: JSON.stringify({ password }),
        }),

        logout: () => API.request('/auth/logout', {
            method: 'POST',
        }),

        verify: () => API.request('/auth/verify', {
            method: 'GET',
        }),
    },

    /**
     * 서비스 관리
     */
    services: {
        getAll: () => API.request('/services', { method: 'GET' }),

        get: (serviceId) => API.request(`/services/${serviceId}`, { method: 'GET' }),

        start: (serviceId) => API.request(`/services/${serviceId}/start`, {
            method: 'POST',
        }),

        stop: (serviceId) => API.request(`/services/${serviceId}/stop`, {
            method: 'POST',
        }),

        restart: (serviceId) => API.request(`/services/${serviceId}/restart`, {
            method: 'POST',
        }),
    },

    /**
     * 로그 관리
     */
    logs: {
        get: (serviceId, limit = 100) => API.request(`/logs/${serviceId}?limit=${limit}`, {
            method: 'GET',
        }),

        clear: (serviceId) => API.request(`/logs/${serviceId}/clear`, {
            method: 'POST',
        }),

        getSize: (serviceId) => API.request(`/logs/${serviceId}/size`, {
            method: 'GET',
        }),
    },

    /**
     * 상태 조회
     */
    status: {
        getSystem: () => API.request('/status/system', { method: 'GET' }),

        getDashboard: () => API.request('/status/dashboard', { method: 'GET' }),
    },
};
