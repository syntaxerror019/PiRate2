async function searchTorrents() {
      let loader = document.createElement("div");
      let container = document.getElementById("results");
      loader.className = "d-flex justify-content-center my-2";
      loader.innerHTML = `<div id="loader" class="spinner-border text-primary" role="status">
                            <span class="visually-hidden">Loading...</span>
                          </div>`
      container.appendChild(loader);

      let q = document.getElementById("searchInput").value;
      let res = await fetch(`/search?q=${encodeURIComponent(q)}`);
      let data = await res.json();

      console.log(data);

      
      container.innerHTML = "";

      data.forEach((t, i) => {
        let card = document.createElement("div");
        card.className = "card my-2";

        card.innerHTML = `
          <div class="card-body">
            <h5 class="card-title">${t.title}</h5>
            <p class="card-text">
              <strong>Seeds:</strong> ${t.seeds} |
              <strong>Leeches:</strong> ${t.leeches} |
              <strong>Size:</strong> ${t.filesize}
            </p>
            <button class="btn btn-sm btn-outline-primary" type="button" 
              data-bs-toggle="collapse" data-bs-target="#details${i}">
              Details
            </button>
            <button class="btn btn-sm btn-success" onclick='download("${t.magnetlink}")'>
              Download
            </button>
            <div class="collapse mt-2" id="details${i}">
              <ul class="list-group list-group-flush">
                <li class="list-group-item"><b>Uploader:</b> ${t.uploader}</li>
                <li class="list-group-item"><b>Uploaded:</b> ${t.upload_date}</li>
                <li class="list-group-item"><b>Bytes:</b> ${t.byte_size}</li>
                <li class="list-group-item"><b>Trusted:</b> ${t.is_trusted}</li>
                <li class="list-group-item"><b>VIP:</b> ${t.is_vip}</li>
                <li class="list-group-item"><b>Category:</b> ${t.category}</li>
                <li class="list-group-item"><b>Infohash:</b> ${t.infohash}</li>
                <li class="list-group-item"><a href="${t.url}" target="_blank">TPB Page</a></li>
                <li class="list-group-item"><a href="${t.magnetlink}">Magnet Link</a></li>
              </ul>
            </div>
          </div>
        `;
        container.appendChild(card);
      });
      container.removeChild(loader);
    }

    async function download(magnet) {
      await fetch("/download", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({magnetlink: magnet})
      });
      let notification = document.createElement("div");
      notification.className = "position-fixed top-0 end-0 p-3";
      notification.innerHTML = `<div class="toast align-items-center text-white bg-primary border-0" role="alert" aria-live="assertive" aria-atomic="true">
                                  <div class="d-flex">
                                    <div class="toast-body">Starting download...</div>
                                    <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
                                  </div>
                                </div>`;
      document.body.appendChild(notification);
      let toast = new bootstrap.Toast(notification.firstChild);
      toast.show();
      setTimeout(() => {
        toast.hide();
        document.body.removeChild(notification);
      }, 3000);
    }

    async function searchTorrentKey() {
      if (event.key === "Enter") {
        await searchTorrents();
      }
    }