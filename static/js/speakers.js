function goToSpeaker(speakerId, conferenceId) {
    window.location.href = `/${conferenceId}/speakers/${speakerId}`;
}

document.addEventListener("DOMContentLoaded", function () {
    const pathSegments = window.location.pathname.split("/");
    const conferenceId = pathSegments[1];

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
                img.src = speaker.PhotoUrl || '/static/defaultImage.png';
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
});

window.onload = function () {
    document.querySelector('.marquee').style.setProperty('--play', 'running');
};
