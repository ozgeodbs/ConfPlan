document.addEventListener("DOMContentLoaded", function () {
    // Konferans ID'sini URL'den al
    const conferenceId = window.location.pathname.split("/")[1];

    // Konferans bilgilerini al
    fetch(`/conferences/${conferenceId}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.warn("Konferans bulunamadı.");
                return;
            }

            // Konferans bilgilerini sayfaya ekle
            document.getElementById("conference-title").textContent = data.Title;
            document.getElementById("conference-date").textContent = `${data.StartDate} - ${data.EndDate}`;
            document.getElementById("conference-location").textContent = data.Location;

            // Konuşmacıları al
            fetch(`/${conferenceId}/speakers/get/all`)
                .then(response => response.json())
                .then(speakers => {
                    const speakersContainer = document.getElementById("speakers-container");
                    speakers.forEach(speaker => {
                        const speakerCard = document.createElement("div");
                        speakerCard.classList.add("speaker-card");
                        speakerCard.innerHTML = `
                            <div class="speaker-info">
                                <h3>${speaker.FirstName} ${speaker.LastName}</h3> -
                                <p>${speaker.Bio}</p>
                            </div>
                        `;
                        speakersContainer.appendChild(speakerCard);
                    });
                })
                .catch(error => console.error("Konuşmacılar verisi çekilemedi:", error));

        })
        .catch(error => console.error("Veri çekme hatası:", error));
});

window.onload = function () {
    document.querySelector('.marquee').style.setProperty('--play', 'running');
};
