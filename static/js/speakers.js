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
            grid.style.display = "flex";
            grid.style.flexWrap = "wrap";
            grid.style.justifyContent = "center";
            grid.style.gap = "7vw";
            grid.style.width = "100%";
            data.forEach(speaker => {
                console.log("Speaker Object:", speaker);
                const speakerContainer = document.createElement('div');
                speakerContainer.style.textAlign = "center";
                const img = document.createElement('img');
                img.src = speaker.PhotoUrl;
                img.alt = `${speaker.FirstName} ${speaker.LastName}`;
                img.classList.add("speaker-photo");  // Burada sınıf ekleniyor
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

