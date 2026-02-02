/**
 * Incodeks Task Sync Dashboard JavaScript
 * Handles API interactions and UI updates
 */

(function () {
  'use strict';

  // DOM elements
  const rawOut = document.getElementById("raw-out");
  const statusOut = document.getElementById("status-out");
  const tasksBody = document.getElementById("tasks-body");

  /**
   * Get CSRF token from hidden form
   * @returns {string} CSRF token
   */
  function csrfToken() {
    const el = document.querySelector('[name=csrfmiddlewaretoken]');
    return el ? el.value : "";
  }

  /**
   * Safely parse JSON response, fallback to raw text
   * @param {Response} resp - Fetch response object
   * @returns {Promise<Object>} Parsed JSON or raw text object
   */
  async function safeJson(resp) {
    const text = await resp.text();
    try {
      return JSON.parse(text);
    } catch (e) {
      return { raw: text };
    }
  }

  /**
   * Trigger sync operation
   */
  async function postSync() {
    rawOut.textContent = "Triggering sync...";
    try {
      const resp = await fetch("/api/sync/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken(),
        },
        body: JSON.stringify({}),
      });
      const data = await safeJson(resp);
      rawOut.textContent = JSON.stringify({ status: resp.status, data }, null, 2);
    } catch (error) {
      rawOut.textContent = JSON.stringify({ error: error.message }, null, 2);
    }
  }

  /**
   * Fetch and display last sync status
   */
  async function getStatus() {
    rawOut.textContent = "Loading status...";
    try {
      const resp = await fetch("/api/sync/status/");
      const data = await safeJson(resp);
      statusOut.textContent = JSON.stringify(data, null, 2);
      rawOut.textContent = JSON.stringify({ status: resp.status, data }, null, 2);
    } catch (error) {
      rawOut.textContent = JSON.stringify({ error: error.message }, null, 2);
      statusOut.textContent = JSON.stringify({ error: error.message }, null, 2);
    }
  }

  /**
   * Render tasks table
   * @param {Array} items - Array of task objects
   */
  function renderTasks(items) {
    tasksBody.innerHTML = "";
    if (!items || items.length === 0) {
      const tr = document.createElement("tr");
      tr.innerHTML = '<td colspan="4" style="text-align: center; color: #999;">No tasks found</td>';
      tasksBody.appendChild(tr);
      return;
    }

    items.forEach(t => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${escapeHtml(t.external_id || "")}</td>
        <td>${escapeHtml(t.title || "")}</td>
        <td>${escapeHtml(t.status || "")}</td>
        <td>${escapeHtml(t.updated_at || "")}</td>
      `;
      tasksBody.appendChild(tr);
    });
  }

  /**
   * Escape HTML to prevent XSS
   * @param {string} text - Text to escape
   * @returns {string} Escaped HTML
   */
  function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
  }

  /**
   * Fetch and display tasks
   */
  async function getTasks() {
    rawOut.textContent = "Loading tasks...";
    try {
      const resp = await fetch("/api/tasks/");
      const data = await safeJson(resp);
      const tasks = Array.isArray(data) ? data : (data.results || []);
      renderTasks(tasks);
      rawOut.textContent = JSON.stringify(
        { 
          status: resp.status, 
          dataPreview: Array.isArray(data) ? data.slice(0, 3) : data 
        }, 
        null, 
        2
      );
    } catch (error) {
      rawOut.textContent = JSON.stringify({ error: error.message }, null, 2);
      renderTasks([]);
    }
  }

  // Event listeners
  document.getElementById("btn-sync").addEventListener("click", (e) => {
    e.preventDefault();
    postSync();
  });

  document.getElementById("btn-status").addEventListener("click", (e) => {
    e.preventDefault();
    getStatus();
  });

  document.getElementById("btn-tasks").addEventListener("click", (e) => {
    e.preventDefault();
    getTasks();
  });

  // Initial load
  getStatus();
  getTasks();
})();
