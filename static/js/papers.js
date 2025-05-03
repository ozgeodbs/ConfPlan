document.addEventListener("DOMContentLoaded", async () => {
    const conferenceId = window.location.pathname.split("/")[1];
    const papersUrl = `/${conferenceId}/papers/get/all`;
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

        // Paper'ları salonlara göre grupla
        const papersByHall = {};
        papers.forEach(p => {
            if (!papersByHall[p.HallId]) {
                papersByHall[p.HallId] = [];
            }
            papersByHall[p.HallId].push(p);
        });

        // HTML'e tablo ekle
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
                        <th>Start Time</th>
                        <th>End Time</th>
                    </tr>
                </thead>
                <tbody>
                    ${hallPapers.map(paper => `
                        <tr>
                            <td>${paper.Title}</td>
                            <td>${paper.StartTime || '-'}</td>
                            <td>${paper.EndTime || '-'}</td>
                        </tr>
                    `).join("")}
                </tbody>
            `;
            container.appendChild(table);
        });

    } catch (error) {
        console.error("❌ Error fetching data:", error);
    }
});
