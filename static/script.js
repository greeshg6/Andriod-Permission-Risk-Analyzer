async function searchApp() {

    const appName = document
        .getElementById("appInput")
        .value.trim();

    if (!appName) {
        document.getElementById("result").innerHTML = `
            <div class="empty-state">
                <p>Please enter an app name to begin the analysis.</p>
            </div>
        `;
        return;
    }

    const response = await fetch(
        "/search",
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                app_name: appName
            })
        }
    );

    const data =
        await response.json();

    const result =
        document.getElementById("result");

    if (!data.found) {
        result.innerHTML = `
            <div class="empty-state">
                <p>No app matched your search. Try a different app name.</p>
            </div>
        `;
        return;
    }

    const permissionsHtml = data.permissions.map(permission => `
        <li class="permission-item">${permission.permission} <span class="perm-type">(${permission.type})</span></li>
    `).join("");

    result.innerHTML = `
        <div class="card">
            <div class="result-grid">
                <div>
                    <h2>${data.appName}</h2>
                    <p class="result-label">Package</p>
                    <p class="result-value">${data.appId}</p>
                </div>
                <div class="result-row">
                    <div>
                        <p class="result-label">Risk score</p>
                        <p class="result-value score-box">${data.riskScore}/100</p>
                    </div>
                    <div class="${data.riskLevel.toLowerCase()}">${data.riskLevel} risk</div>
                </div>
            </div>

            <div class="result-meta">
                <div class="result-label">Permissions analyzed</div>
                <ul class="permission-list">
                    ${permissionsHtml}
                </ul>

                <div class="summary">
                    <p>${data.explanation}</p>
                </div>

                <div class="recommendations">
                    <div class="result-label">Security recommendations</div>
                    <ul class="recommendations-list">
                        ${data.recommendations.map(r => `<li class="recommendation-item">${r}</li>`).join("")}
                    </ul>
                </div>
            </div>
        </div>
    `;
}
