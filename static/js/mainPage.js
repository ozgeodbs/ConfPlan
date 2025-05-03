document.addEventListener("DOMContentLoaded", function () {
    const conferenceId = window.location.pathname.split("/").pop();

    fetch(`/${conferenceId}/speakers/get/all`)
        .then(response => response.json())
        .then(data => {
            console.log("Speakers API Response:", data);
            const container = document.getElementById('speakers-container');
            container.innerHTML = '';
            const grid = document.createElement('div');
            grid.style.display = "flex";
            grid.style.flexWrap = "wrap";
            grid.style.justifyContent = "center";
            grid.style.gap = "30px";
            grid.style.width = "100%";

            const displayedSpeakerIds = new Set();
            data.forEach(paper => {
                const speaker = paper.Speaker;
                if (!speaker || displayedSpeakerIds.has(speaker.Id)) return;

                displayedSpeakerIds.add(speaker.Id);

                const speakerContainer = document.createElement('div');
                speakerContainer.classList.add("speaker-card");

                const img = document.createElement('img');
                img.src = speaker.PhotoUrl || '/static/defaultImage.png'; // Default avatar if no photo
                img.alt = `${speaker.FirstName} ${speaker.LastName}`;
                img.classList.add("speaker-photo");

                const button = document.createElement('button');
                button.textContent = `${speaker.FirstName} ${speaker.LastName}`;
                button.onclick = () => goToSpeaker(speaker.Id, conferenceId);

                speakerContainer.appendChild(img);
                speakerContainer.appendChild(button);
                grid.appendChild(speakerContainer);
            });

            container.appendChild(grid);
        })
        .catch(error => console.error('Error:', error));

    // Konferans verilerini getir
    fetch(`/conferences/${conferenceId}`)
        .then(res => res.json())
        .then(data => {
            if (data.error) {
                return console.warn("Konferans bulunamadı.");
            }

            document.getElementById("conference-title").textContent = data.Title;

            const start = new Date(data.StartDate).toLocaleDateString(undefined, {
                year: "numeric",
                month: "short",
                day: "numeric"
            });
            const end = new Date(data.EndDate).toLocaleDateString(undefined, {
                year: "numeric",
                month: "short",
                day: "numeric"
            });

            document.getElementById("conference-date").textContent = `${start} - ${end}`;
            document.getElementById("conference-location").textContent = data.Location;

            const video = document.getElementById("background-video");
            const videoSource = document.getElementById("video-source");
            const image = document.getElementById("conference-image");

            if (data.VideoUrl && data.VideoUrl.trim() !== "null") {
                videoSource.src = data.VideoUrl;
                video.load();
                video.style.display = "block";
                image.style.display = "none";
            } else {
                video.style.display = "none";
                image.src = data.PhotoUrl || '/static/background.jpeg';
                image.style.display = "block";
            }
        })
        .catch(err => console.error("Konferans verisi alınamadı:", err));
});
