document.addEventListener("DOMContentLoaded", function () {

    const conferenceId = window.location.pathname.split("/")[1];

    fetch(`/conferences/${conferenceId}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.warn("Conference not found.");
                return;
            }

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

            document.getElementById("title").textContent = data.Title;
            document.getElementById("conference-date").textContent = `${start} - ${end}`;
            document.getElementById("conference-location").textContent = data.Location;
            document.getElementById("conference-organizer").textContent = data.Organizer;

            fetch(`/${conferenceId}/speakers/get/all`)
                .then(response => response.json())
                .then(papers => {
                    const speakersContainer = document.getElementById("speakers-container");
                    speakersContainer.innerHTML = "";

                    papers.sort((a, b) => {
                        const firstNameA = a.Speaker ? a.Speaker.FirstName.toLowerCase() : '';
                        const firstNameB = b.Speaker ? b.Speaker.FirstName.toLowerCase() : '';
                        return firstNameA.localeCompare(firstNameB);
                    });

                    papers.forEach(paper => {
                        const speaker = paper.Speaker;
                        if (!speaker) return;

                        const speakerCard = document.createElement("div");
                        speakerCard.classList.add("speaker-card");
                        speakerCard.innerHTML = `
                            <div class="speaker-info">
                                <h3>${speaker.FirstName} ${speaker.LastName}</h3> 
                                <h3>-</h3>
                                <p>${paper.Title}</p>
                            </div>
                        `;
                        speakersContainer.appendChild(speakerCard);
                    });
                })
                .catch(error => console.error("Failed to fetch speaker data:", error));
        })
        .catch(error => console.error("Failed to fetch conference data:", error));
});

window.onload = function () {
    document.querySelector('.marquee')?.style.setProperty('--play', 'running');
};
