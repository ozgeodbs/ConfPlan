document.addEventListener("DOMContentLoaded", async () => {
    const conferenceId = window.location.pathname.split("/")[1];
    const papersUrl = `/${conferenceId}/speakers/get/all`;
    const hallUrl = `/${conferenceId}/halls`;

    try {
        const [papersRes, hallRes] = await Promise.all([
            fetch(papersUrl),
            fetch(hallUrl)
        ]);

        const papers = await papersRes.json();
        const halls = await hallRes.json();

        const hallMap = {};
        halls.forEach(h => {
            hallMap[h.Id] = h.Title;
        });

        // Paperları gün + hall bazında grupla
        const scheduleByDateAndHall = {};
        papers.forEach(paper => {
            if (!paper.StartTime || !paper.HallId) return;

            const dateKey = new Date(paper.StartTime).toISOString().split("T")[0]; // YYYY-MM-DD
            if (!scheduleByDateAndHall[dateKey]) {
                scheduleByDateAndHall[dateKey] = {};
            }
            if (!scheduleByDateAndHall[dateKey][paper.HallId]) {
                scheduleByDateAndHall[dateKey][paper.HallId] = [];
            }
            scheduleByDateAndHall[dateKey][paper.HallId].push(paper);
        });

        const container = document.getElementById("schedule-tables");
        container.innerHTML = "";

        const sortedDates = Object.keys(scheduleByDateAndHall).sort();

        sortedDates.forEach(date => {
            const dateTitle = document.createElement("h2");
            dateTitle.textContent = `${new Date(date).toLocaleDateString()}`;
            container.appendChild(dateTitle);

            const hallsOnThisDay = scheduleByDateAndHall[date];

            halls.forEach(hall => {
                const hallPapers = hallsOnThisDay[hall.Id] || [];
                if (hallPapers.length === 0) return;

                const tableTitle = document.createElement("h3");
                tableTitle.textContent = `Hall: ${hall.Title}`;
                container.appendChild(tableTitle);

                const table = document.createElement("table");
                table.innerHTML = `
                    <thead>
                        <tr>
                            <th>Paper Title</th>
                            <th>Speaker</th>
                            <th>Start Time</th>
                            <th>End Time</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${hallPapers.map(paper => {
                            const speakerName = paper.Speaker
                                ? `${paper.Speaker.FirstName} ${paper.Speaker.LastName}`
                                : "-";
                            const start = new Date(paper.StartTime).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
                            const end = new Date(paper.EndTime).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
                            return `
                                <tr>
                                    <td>${paper.Title}</td>
                                    <td>${speakerName}</td>
                                    <td>${start}</td>
                                    <td>${end}</td>
                                </tr>
                            `;
                        }).join("")}
                    </tbody>
                `;
                container.appendChild(table);
            });
        });

    } catch (error) {
        console.error("❌ Error fetching data:", error);
    }
});
