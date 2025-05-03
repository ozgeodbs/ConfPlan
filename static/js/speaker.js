document.addEventListener("DOMContentLoaded", function () {
    const pathSegments = window.location.pathname.split("/");
    const speakerId = pathSegments[pathSegments.length - 1];

    fetch(`/speakers/${speakerId}`)
        .then(response => response.json())
        .then(speaker => {
            const container = document.getElementById("speaker-details");

            if (speaker.message) {
                container.innerHTML = "<p>Speaker could not found.</p>";
                return;
            }

            container.innerHTML = `
                <div class="speaker-profile-vertical">
                    <img class="speaker-img-top" src="${speaker.PhotoUrl || '/static/img/default-avatar.png'}" alt="${speaker.FirstName} ${speaker.LastName}">
                    <div class="speaker-info-block">
                        <h2>${speaker.FirstName} ${speaker.LastName}</h2>
                        <p class="bio">${speaker.Bio || 'Undefined'}</p>
                        <div class="speaker-contact">
                            <p><strong>Email:</strong> ${speaker.Email}</p>
                            <p><strong>Telefon:</strong> ${speaker.Phone || 'Undefined'}</p>
                        </div>
                    </div>
                </div>
            `;
        })
        .catch(error => {
            console.error("Hata:", error);
            document.getElementById("speaker-details").innerHTML = "<p>Fetching error.</p>";
        });

    fetch(`/speakers/${speakerId}/conferences`)
        .then(response => response.json())
        .then(data => {
            const section = document.createElement("section");
            section.classList.add("speaker-sessions");

            const list = document.createElement("ul");
            list.classList.add("conference-list");

            data.forEach(item => {
                const li = document.createElement("li");
                li.innerHTML = `<strong>${item.conference_title}</strong>
                                <em>${item.paper_title}</em>`;
                list.appendChild(li);
            });

            section.appendChild(list);

            document.getElementById("speaker-details").appendChild(section);
        })
        .catch(error => console.error("Error fetching data:", error));

});
