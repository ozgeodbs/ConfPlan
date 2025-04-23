document.addEventListener("DOMContentLoaded", async () => {
    const conferenceId = window.location.pathname.split("/")[1];
    const papersUrl = `/${conferenceId}/papers/get/all`;
    const similaritiesUrl = `/${conferenceId}/papers/get/similarities`;

    try {
        const [papersRes, similaritiesRes] = await Promise.all([
            fetch(papersUrl),
            fetch(similaritiesUrl)
        ]);

        const papers = await papersRes.json();
        const similarities = await similaritiesRes.json();

        console.log("📄 Papers:", papers);
        console.log("🔁 Similarities:", similarities);

        // Paper map oluşturma
        const paperMap = {};
        papers.forEach(p => {
            paperMap[p.Id] = {
                ...p,
                SimilarPapers: []
            }; // Her paper için benzer papers listesi
        });

        // Similarity data'sını ilişkilendir
        similarities.forEach(sim => {
            if (paperMap[sim.PaperId]) {
                paperMap[sim.PaperId].SimilarPapers.push({
                    title: sim.SimilarPaperTitle,
                    similarity_score: parseFloat(sim.SimilarityScore).toFixed(2)
                });
            }
        });

        // Tabloyu doldur
        const tableBody = document.querySelector("tbody");
        tableBody.innerHTML = "";  // Tabloyu temizle

        // Paperları döngü ile tabloya ekle
        Object.values(paperMap).forEach(paper => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td>${paper.Title}</td>
                <td>${paper.StartTime ? paper.StartTime : '-'}</td>
                <td>${paper.EndTime ? paper.EndTime : '-'}</td>
                <td>
                    <ul>
                        ${paper.SimilarPapers.map(sp => `
                            <li>${sp.title} <br>
                                <small>(Similarity: ${sp.similarity_score})</small>
                            </li>

                        `).join("")}
                    </ul>
                </td>
            `;
            tableBody.appendChild(tr);
        });

    } catch (error) {
        console.error("❌ Error fetching data:", error);
    }
});
