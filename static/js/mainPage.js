document.addEventListener("DOMContentLoaded", function () {
    // Konferans ID'yi URL'den al
    const conferenceId = window.location.pathname.split("/").pop();

    // Konuşmacıları getir
    fetch('/speakers')
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('speakers-container');
            container.innerHTML = '';

            const grid = document.createElement('div');
            grid.style.display = "grid";
            grid.style.gridTemplateColumns = "repeat(auto-fit, minmax(220px, 1fr))";
            grid.style.gap = "30px";
            grid.style.padding = "30px";

            data.forEach(speaker => {
                const card = document.createElement('div');
                card.className = "speaker-card";

                const img = document.createElement('img');
                img.src = speaker.PhotoUrl;
                img.alt = `${speaker.FirstName} ${speaker.LastName}`;
                img.className = "speaker-photo";

                const nameBtn = document.createElement('button');
                nameBtn.textContent = `${speaker.FirstName} ${speaker.LastName}`;
                nameBtn.onclick = () => window.location.href = `/${conferenceId}/speakers/${speaker.Id}`;

                card.appendChild(img);
                card.appendChild(nameBtn);
                grid.appendChild(card);
            });

            container.appendChild(grid);
        })
        .catch(error => console.error('Konuşmacı verileri alınamadı:', error));

    // Konferans bilgilerini getir
    fetch(`/conferences/${conferenceId}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.warn("Konferans bulunamadı.");
                return;
            }

            document.getElementById("conference-title").textContent = data.Title;
            document.getElementById("conference-date").textContent = `${data.StartDate} - ${data.EndDate}`;
            document.getElementById("conference-location").textContent = data.Location;

            const videoElement = document.getElementById("background-video");
            const videoSource = document.getElementById("video-source");
            const conferenceImage = document.getElementById("conference-image");

            if (data.VideoUrl && data.VideoUrl.trim() !== "null") {
                videoSource.src = data.VideoUrl;
                videoElement.load();
                videoElement.style.display = "block";
                conferenceImage.style.display = "none";
            } else {
                videoElement.style.display = "none";
                conferenceImage.src = data.PhotoUrl || '/static/background.jpg';
                conferenceImage.style.display = "block";
            }
        })
        .catch(error => console.error("Konferans verisi çekme hatası:", error));
});
