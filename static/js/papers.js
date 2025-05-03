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

        // Hall Map oluşturma: Hall Id'leri ile başlıkları eşleştir
        const hallMap = {};
        halls.forEach(h => {
            hallMap[h.Id] = h.Title;
        });

        // Paper map oluşturma
        const paperMap = {};
        papers.forEach(p => {
            paperMap[p.Id] = {
                ...p,
                HallTitle: hallMap[p.HallId] || '-'  // Her paper için ilgili salon başlığını al
            };
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
                <td>${paper.HallTitle}</td>
            `;
            tableBody.appendChild(tr);
        });

    } catch (error) {
        console.error("❌ Error fetching data:", error);
    }
});
