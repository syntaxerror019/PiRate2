    async function loadDownloads() {
      let res = await fetch("/downloads");
      let data = await res.json();
      let container = document.getElementById("downloads");
      container.innerHTML = "";

      data.forEach(d => {
        let row = document.createElement("tr");
        if (d.progress === "100.00%") {
          row.className = "table-success";
          row.innerHTML = `
          <td>${d.name}</td>
          <td>Ready</td>
          <td>100%</td>
          <td>N/A</td>
          <td>N/A</td>
          <td><button class="btn btn-sm btn-success" onclick="watch('${d.name}')">Play</button> <button class="btn btn-sm btn-danger" onclick="remove('${d.hash}')">Delete</button></td>
        `;
        } else {
        row.innerHTML = `
          <td>${d.name}</td>
          <td>${d.status}</td>
          <td>${d.progress}</td>
          <td>${d.speed}</td>
          <td>${d.eta}</td>
          <td>
            <button class="btn btn-sm btn-warning" onclick="pause('${d.hash}')">Pause</button>
            <button class="btn btn-sm btn-info" onclick="resume('${d.hash}')">Resume</button>
            <button class="btn btn-sm btn-danger" onclick="remove('${d.hash}')">Delete</button>
          </td>
        `;
        }
        container.appendChild(row);
      });
      if (data.length === 0) {
        container.innerHTML = `<tr><td colspan="6" class="text-center">No active downloads</td></tr>`;
      }
    }

    async function watch(name) {
      let res = await fetch(`/watch/${name}`);
      if (res.status !== 200) {
        alert(`Failed to watch ${res.error}`);
      } else {
        window.location.href = `/controller`;
      }
    }

    async function remove(hash) {
      let res = await fetch(`/remove/${hash}`, { method: "DELETE" });
      if (res.status !== 200) {
        alert(`Failed to remove ${hash}`);
      } else {
        loadDownloads();
      }
    }

    async function pause(hash) {
      let res = await fetch(`/pause/${hash}`, { method: "POST" });
      if (res.status !== 200) {
        alert(`Failed to pause ${hash}`);
      } else {
        loadDownloads();
      }
    }

    async function resume(hash) {
      let res = await fetch(`/resume/${hash}`, { method: "POST" });
      if (res.status !== 200) {
        alert(`Failed to resume ${hash}`);
      } else {
        loadDownloads();
      }
    }

    setInterval(loadDownloads, 2000); // refresh every 2s
    window.onload = loadDownloads;
