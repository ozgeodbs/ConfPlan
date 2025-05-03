document.addEventListener("DOMContentLoaded", async () => {
    const conferenceId = window.location.pathname.split("/")[1];
    const papersUrl = `/${conferenceId}/speakers/get/all`;  // tek endpoint
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

        const papersByHall = {};
        papers.forEach(p => {
            if (!papersByHall[p.HallId]) {
                papersByHall[p.HallId] = [];
            }
            papersByHall[p.HallId].push(p);
        });

        const container = document.getElementById("schedule-tables");
        container.innerHTML = "";

        halls.forEach(hall => {
            const hallPapers = papersByHall[hall.Id] || [];

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
                        return `
                            <tr>
                                <td>${paper.Title}</td>
                                <td>${speakerName}</td>
                                <td>${paper.StartTime || '-'}</td>
                                <td>${paper.EndTime || '-'}</td>
                            </tr>
                        `;
                    }).join("")}
                </tbody>
            `;
            container.appendChild(table);
        });

    } catch (error) {
        console.error("❌ Error fetching data:", error);
    }
});
