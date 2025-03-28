const CONFIG = {
    BASE_URL: "http://127.0.0.1:5000/"
};

function displayData(containerId, data) {
    const container = document.getElementById(containerId);
    container.innerHTML = '';
    if (data.length === 0) {
        container.innerHTML = 'No data found.';
    } else {
        const ul = document.createElement('ul');
        data.forEach(item => {
            const li = document.createElement('li');
            li.textContent = JSON.stringify(item, null, 2);
            ul.appendChild(li);
        });
        container.appendChild(ul);
    }
}

function goToSpeaker(speakerId) {
    // Navigate to the speaker's page based on the speaker's ID
    window.location.href = `/speakers/${speakerId}`;
}

document.addEventListener("DOMContentLoaded", function () {
    // Fetch speakers
    fetch('/speakers')
        .then(response => response.json())
        .then(data => {
            console.log("Speakers API Response:", data);
            const container = document.getElementById('speakers-container');
            container.innerHTML = '';
            const grid = document.createElement('div');
            grid.style.display = "grid";
            grid.style.gridTemplateColumns = "repeat(3, 1fr)";
            grid.style.gap = "20px";
            data.forEach(speaker => {
                console.log("Speaker Object:", speaker);
                const speakerContainer = document.createElement('div');
                speakerContainer.style.textAlign = "center";
                const img = document.createElement('img');
                img.src = speaker.PhotoUrl;
                img.alt = `${speaker.FirstName} ${speaker.LastName}`;
                const button = document.createElement('button');
                button.textContent = `${speaker.FirstName} ${speaker.LastName}`;
                button.onclick = () => window.location.href = `/speakers/${speaker.Id}`;
                speakerContainer.appendChild(img);
                speakerContainer.appendChild(button);
                grid.appendChild(speakerContainer);
            });
            container.appendChild(grid);
        })
        .catch(error => console.error('Error:', error));

    // Fetch conferences
    const conferenceId = window.location.pathname.split("/").pop();

    fetch(`/conferences/${conferenceId}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.warn("Konferans bulunamadı.");
                return;
            }

            // HTML öğelerine API'den gelen veriyi ata
            document.getElementById("conference-title").textContent = data.Title;
            document.getElementById("conference-date").textContent = `${data.StartDate} - ${data.EndDate}`;
            document.getElementById("conference-location").textContent = data.Location;

            // Video varsa göster, yoksa fotoğrafı göster
            const videoContainer = document.getElementById("video-container");
            const videoElement = document.getElementById("background-video");
            const videoSource = document.getElementById("video-source");
            const conferenceImage = document.getElementById("conference-image");

            if (data.VideoUrl && data.VideoUrl.trim() !== "null") {
                // Video varsa
                videoSource.src = data.VideoUrl;
                videoElement.load(); // Yeni video kaynağını yükle
                videoElement.style.display = "block"; // Videoyu göster
                conferenceImage.style.display = "none"; // Fotoğrafı gizle
            } else {
                // Video yoksa
                videoElement.style.display = "none"; // Video konteynerini gizle
                conferenceImage.src = data.PhotoUrl; // Fotoğraf URL'sini ata
                conferenceImage.style.display = "block"; // Fotoğrafı göster
            }
        })
        .catch(error => console.error("Veri çekme hatası:", error));

});

window.onload = function () {
    document.querySelector('.marquee').style.setProperty('--play', 'running');
};

