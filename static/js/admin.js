const token = '60a5e082-f4d2-4284-91f6-7478a797f0ac';
const baseUrl = 'http://127.0.0.1:5000';

function calculateSimilarities() {
    const conferenceId = prompt("Please enter the Conference ID:");
        if (!conferenceId) return;{
        fetch(`${baseUrl}/${conferenceId}/papers/save_similarities`, {
        method: 'POST',
        headers: {
            'token': token
        }
    }).then(res => alert("Similarities calculated!"));
    }
}

function scheduleCalendar() {
    const conferenceId = prompt("Please enter the Conference ID:");
        if (!conferenceId) return;{
            fetch(`${baseUrl}/${conferenceId}/schedule`, {
            method: 'POST',
            headers: {
                'token': token
            }
        }).then(res => alert("Schedule generated!"));
    } 
}

function generateExcelTemplate() {
    window.location.href = 'http://127.0.0.1:5000/generate_excel_template';
}

function uploadExcel(type) {
    const fileInput = document.getElementById(`file${capitalize(type)}`);
    const file = fileInput.files[0];
    if (!file) {
        alert('Please select a file first.');
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    fetch(`http://127.0.0.1:5000/import/${type}`, {
        method: 'POST',
        headers: {
            'token': token
        },
        body: formData
    })
    .then(response => {
        if (response.ok) {
            alert(`${capitalize(type)} imported successfully!`);
        } else {
            alert(`Error importing ${type}`);
        }
    });
}

async function fetchData(type, needsId = false) {
    let url = '';
    const baseUrl = 'http://127.0.0.1:5000';

    if (needsId) {
        const conferenceId = prompt("Please enter the Conference ID:");
        if (!conferenceId) return;
            if (type === 'halls') {
                url = `${baseUrl}/${conferenceId}/halls`;
            } else if (type === 'papers') {
                url = `${baseUrl}/${conferenceId}/papers/get/all`;
            }
    } else {
        url = `${baseUrl}/${type}`;
    }

    const response = await fetch(url);
    const data = await response.json();

    if ((Array.isArray(data) && data.length === 0) || (data && typeof data === 'object' && 'message' in data)) {
        alert('No data found');
        return;
    }
    showPopup(type, data);
}

function showPopup(type, data) {
    // Eğer popup zaten varsa kaldır
    const existingPopup = document.getElementById('popup-container');
    if (existingPopup) existingPopup.remove();

    // Overlay oluştur
    const overlay = document.createElement('div');
    overlay.id = 'popup-container';
    overlay.style = `
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background: rgba(0,0,0,0.5);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 1000;
    `;

    // Popup kutusu
    const popup = document.createElement('div');
    popup.style = `
        background: white;
        padding: 20px;
        border-radius: 8px;
        max-width: 80vw;
        max-height: 80vh;
        overflow-y: auto;
        box-shadow: 0 2px 10px rgba(0,0,0,0.3);
        position: relative;
    `;

    // Çarpı butonu
    const closeBtn = document.createElement('button');
    closeBtn.innerHTML = '&times;';
    closeBtn.style = `
        position: absolute;
        top: 10px;
        right: 15px;
        font-size: 24px;
        border: none;
        background: none;
        cursor: pointer;
    `;
    closeBtn.onclick = () => {
        overlay.remove();
    };

    // Başlık
    const heading = document.createElement('h3');
    heading.textContent = `${capitalize(type)}:`;

    // Liste oluştur
    const list = document.createElement('ul');
    data.forEach(item => {
        const li = document.createElement('li');
        li.textContent = `${item.Id} - ${item.Title || item.FirstName + ' ' + item.LastName || ''}`;
        list.appendChild(li);
    });

    // Popup'a ekle
    popup.appendChild(closeBtn);
    popup.appendChild(heading);
    popup.appendChild(list);
    overlay.appendChild(popup);
    document.body.appendChild(overlay);
}

function capitalize(s) {
    return s.charAt(0).toUpperCase() + s.slice(1);
}
