"use strict";
const output = document.getElementById("output");
const clusterButton = document.getElementById("clusterButton");
function pretty(value) {
    return JSON.stringify(value, null, 2);
}
clusterButton.addEventListener("click", () => {
    const points = document.getElementById("pointsInput").value;
    const eps = parseFloat(document.getElementById("epsInput").value);
    const min_pts = parseInt(document.getElementById("minInput").value, 10);
    fetch("/api/cluster", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ points, eps, min_pts }),
    })
        .then((res) => res.json())
        .then((data) => {
        output.textContent = pretty(data.clusters || data);
    });
});
