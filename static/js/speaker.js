document.addEventListener("DOMContentLoaded", function () {
    const pathSegments = window.location.pathname.split("/");
    const speakerId = pathSegments[pathSegments.length - 1];

    fetch(`/speakers/${speakerId}`)
        .then(response => response.json())
        .then(speaker => {
            if (speaker.message) {
                document.getElementById("speaker-details").innerHTML = "<p>Konuşmacı bulunamadı.</p>";
                return;
            }

            const container = document.getElementById("speaker-details");
            container.innerHTML = `
                        <img class="photo" src="${speaker.PhotoUrl || '/static/default.jpg'}" alt="${speaker.FirstName} ${speaker.LastName}">
                        <h2>${speaker.FirstName} ${speaker.LastName}</h2>
                        <p><strong>Email:</strong> ${speaker.Email}</p>
                        <p><strong>Telefon:</strong> ${speaker.Phone || 'Belirtilmemiş'}</p>
                        <div class="info">
                            <h3>Biyografi</h3>
                            <p>${speaker.Bio || 'Biyografi bulunmamaktadır.'}</p>
                        </div>
                    `;
        })
        .catch(error => {
            console.error("Hata:", error);
            document.getElementById("speaker-details").innerHTML = "<p>Veri alınırken bir hata oluştu.</p>";
        });
});

