function goToSpeaker(speakerId, conferenceId) {
    // Yeni URL'yi oluştur ve yönlendir
    window.location.href = `/${conferenceId}/speakers/${speakerId}`;
}

document.addEventListener("DOMContentLoaded", function () {

    const pathSegments = window.location.pathname.split("/");
    const conferenceId = pathSegments[1];
    // Fetch speakers
    fetch(`/${conferenceId}/speakers/get/all`)
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
                button.textContent = `${speaker.FirstName} ${speaker.LastName} `;
                button.onclick = () => window.location.href = `/${conferenceId}/speakers/${speaker.Id}`;
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

