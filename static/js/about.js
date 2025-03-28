const CONFIG = {
    BASE_URL: "http://127.0.0.1:5000/"
};


document.addEventListener("DOMContentLoaded", function () {
    // Fetch conferences
    const conferenceId = window.location.pathname.split("/")[1];

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

