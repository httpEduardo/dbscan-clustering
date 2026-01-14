const output = document.getElementById("output") as HTMLPreElement;
const clusterButton = document.getElementById("clusterButton") as HTMLButtonElement;

function pretty(value: unknown): string {
  return JSON.stringify(value, null, 2);
}

clusterButton.addEventListener("click", () => {
  const points = (document.getElementById("pointsInput") as HTMLTextAreaElement).value;
  const eps = parseFloat((document.getElementById("epsInput") as HTMLInputElement).value);
  const min_pts = parseInt((document.getElementById("minInput") as HTMLInputElement).value, 10);
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
