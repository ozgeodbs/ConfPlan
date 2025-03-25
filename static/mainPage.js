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

document.getElementById('getPapersBtn').addEventListener('click', function () {
    console.log('Get Papers button clicked');
    fetch('/papers')
        .then(response => response.json())
        .then(data => displayData('papersContainer', data))
        .catch(error => console.error('Error:', error));
});

document.getElementById('getHallsBtn').addEventListener('click', function () {
    fetch('/halls')
        .then(response => response.json())
        .then(data => displayData('hallsContainer', data))
        .catch(error => console.error('Error:', error));
});

document.getElementById('getSpeakersBtn').addEventListener('click', function () {
    fetch('/speakers')
        .then(response => response.json())
        .then(data => displayData('speakersContainer', data))
        .catch(error => console.error('Error:', error));
});

document.getElementById('getConferencesBtn').addEventListener('click', function () {
    fetch('/conferences')
        .then(response => response.json())
        .then(data => displayData('conferencesContainer', data))
        .catch(error => console.error('Error:', error));
});

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
    fetch(`/conferences`)
        .then(response => response.json())
        .then(data => {
            console.log("Conferences API Response:", data);
            if (data.length === 0) {
                console.warn("Konferans verisi bulunamadı.");
                return;
            }

            const lastConference = data[data.length - 1]; // Son konferansı al
            console.log("Last Conference:", lastConference);

            // Veriyi kullanarak başlıkları güncelle
            document.getElementById("conference-title").textContent = lastConference.Title; // Veri alanı büyük harfle "Title" olabilir
            document.getElementById("conference-date").textContent = lastConference.StartDate; // Tarih formatı değişmiş olabilir
            document.getElementById("conference-location").textContent = lastConference.Location; // Konum adı farklı olabilir
        })
        .catch(error => console.error("Veri çekme hatası:", error));

});
