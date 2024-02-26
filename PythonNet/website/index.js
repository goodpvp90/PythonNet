

async function fetchClientsData() {
    const data = await fetch('api/clients');
    const dataJson = await data.json();
    console.log(dataJson);

    renderClients(dataJson);
}

function renderClients(clients) {
    const clientsList = document.querySelector('#clients-list');

    clientsList.innerHTML = '';

    clients.forEach(client => {
        const li = document.createElement('li');

        li.innerHTML = `
            <p>
                <span>${client.ip}</span>
                <span>${client.port}</span>
                <span>connected: ${client.connected}</span>
            <p>
        `;

        clientsList.appendChild(li);
    });
}


fetchClientsData();