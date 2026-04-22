/**
 * API 调用模块
 * 封装所有后端 API 调用
 */

const API_BASE = 'http://localhost:5001/api';

// 游戏控制
export async function newGame(companyName = 'AI 创业公司') {
    const resp = await fetch(`${API_BASE}/game/new`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({company_name: companyName})
    });
    return await resp.json();
}

export async function loadGame(saveName = 'autosave') {
    const resp = await fetch(`${API_BASE}/game/load`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({save_name: saveName})
    });
    return await resp.json();
}

export async function saveGame(saveName = 'autosave') {
    const resp = await fetch(`${API_BASE}/game/save`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({save_name: saveName})
    });
    return await resp.json();
}

export async function nextDay() {
    const resp = await fetch(`${API_BASE}/game/next-day`, {
        method: 'POST'
    });
    return await resp.json();
}

export async function getGameStatus() {
    const resp = await fetch(`${API_BASE}/game/status`);
    return await resp.json();
}

// Agent 管理
export async function listAgents() {
    const resp = await fetch(`${API_BASE}/agents`);
    return await resp.json();
}

export async function hireAgent(role, name = null) {
    const resp = await fetch(`${API_BASE}/agents/hire`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({role, name})
    });
    return await resp.json();
}

export async function fireAgent(agentId) {
    const resp = await fetch(`${API_BASE}/agents/fire`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({agent_id: agentId})
    });
    return await resp.json();
}

export async function trainAgent(agentId) {
    const resp = await fetch(`${API_BASE}/agents/train`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({agent_id: agentId})
    });
    return await resp.json();
}

// 项目管理
export async function listProjects(status = null) {
    const url = status 
        ? `${API_BASE}/projects?status=${status}`
        : `${API_BASE}/projects`;
    const resp = await fetch(url);
    return await resp.json();
}

export async function acceptProject(projectId) {
    const resp = await fetch(`${API_BASE}/projects/accept`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({project_id: projectId})
    });
    return await resp.json();
}

export async function assignAgent(agentId, projectId) {
    const resp = await fetch(`${API_BASE}/projects/assign`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({agent_id: agentId, project_id: projectId})
    });
    return await resp.json();
}

export async function completeProject(projectId) {
    const resp = await fetch(`${API_BASE}/projects/complete`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({project_id: projectId})
    });
    return await resp.json();
}

// 公司管理
export async function getCompany() {
    const resp = await fetch(`${API_BASE}/company`);
    return await resp.json();
}

export async function upgradeOffice() {
    const resp = await fetch(`${API_BASE}/company/upgrade-office`, {
        method: 'POST'
    });
    return await resp.json();
}

export async function researchTechnology(techName) {
    const resp = await fetch(`${API_BASE}/company/research`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({tech_name: techName})
    });
    return await resp.json();
}

// 导出到 window (避免命名冲突)
window.nextDayAPI = nextDay;
window.newGameAPI = newGame;
window.loadGameAPI = loadGame;
window.upgradeOfficeAPI = upgradeOffice;
window.hireAgentAPI = hireAgent;
window.listAgentsAPI = listAgents;
window.listProjectsAPI = listProjects;
window.acceptProjectAPI = acceptProject;
window.completeProjectAPI = completeProject;
window.researchTechnologyAPI = researchTechnology;
