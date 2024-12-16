const listContainer = document.getElementById('listContainer');
const newListBtn = document.getElementById('newListBtn');
const newListName = document.getElementById('newListName');

// Fetch and display lists and tasks
async function fetchLists() {
    try {
        const response = await fetch('/lists');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log(data); // Log the response to check its structure
        listContainer.innerHTML = '';
        if (Array.isArray(data.lists)) {
            data.lists.forEach(list => {
                console.log(list); // Log each list to check its structure
                const listElement = document.createElement('div');
                listElement.className = 'list';
                listElement.innerHTML = `
                        <h2>${list.name}</h2>
                        <button onclick="updateList(${list.id})" class="list-update-btn">Actualizar Lista</button>
                        <button onclick="deleteList(${list.id})" class="task-delete-btn">Eliminar Lista</button>
                        <div class="tasks">
                            ${(Array.isArray(list.tasks) ? list.tasks : []).map(task => `
                                <div class="task">
                                    <input type="checkbox" ${task.completed ? 'checked' : ''} onclick="toggleTask(${task.id})">
                                    <span>${task.title}</span><span class="separator"> - </span><span class="description">${task.description || 'Sin descripción'}</span>
                                    <button onclick="updateTask(${task.id})" class="task-update-btn">Actualizar</button>
                                    <button onclick="deleteTask(${task.id})" class="task-delete-btn">Eliminar</button>
                                </div>
                            `).join('')}
                        </div>
                        <input type="text" placeholder="Nueva tarea" onkeypress="addTask(event, ${list.id})">
                    `;
                listContainer.appendChild(listElement);
            });
        } else {
            console.error("Expected 'lists' to be an array");
        }
    } catch (error) {
        console.error('Error fetching lists:', error);
    }
}

// Add new list
newListBtn.addEventListener('click', async () => {
    const name = newListName.value.trim();
    if (name) {
        try {
            const response = await fetch('/lists', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name })
            });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            newListName.value = '';
            fetchLists();
        } catch (error) {
            console.error('Error creating list:', error);
        }
    }
});

// Delete list
window.deleteList = async (listId) => {
    try {
        const response = await fetch(`/lists/${listId}`, { method: 'DELETE' });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        fetchLists();
    } catch (error) {
        console.error('Error deleting list:', error);
    }
};

// Add new task
window.addTask = async (event, listId) => {
    if (event.key === 'Enter') {
        const title = event.target.value.trim();
        const description = prompt("Ingrese la descripción de la tarea:");
        if (title) {
            try {
                const response = await fetch('/tasks', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ title, description, list_id: listId })
                });
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                event.target.value = '';
                fetchLists();
            } catch (error) {
                console.error('Error adding task:', error);
            }
        }
    }
};

// Delete task
window.deleteTask = async (taskId) => {
    try {
        const response = await fetch(`/tasks/${taskId}`, { method: 'DELETE' });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        fetchLists();
    } catch (error) {
        console.error('Error deleting task:', error);
    }
};

// Toggle task completion
window.toggleTask = async (taskId) => {
    const taskElement = document.querySelector(`input[onclick="toggleTask(${taskId})"]`);
    const completed = taskElement.checked;
    try {
        const response = await fetch(`/tasks/${taskId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ completed })
        });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        fetchLists();
    } catch (error) {
        console.error('Error toggling task:', error);
    }
};

// Update list
window.updateList = async (listId) => {
    const newName = prompt("Ingrese el nuevo nombre de la lista:");
    if (newName) {
        try {
            const response = await fetch(`/lists/${listId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name: newName })
            });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            fetchLists();
        } catch (error) {
            console.error('Error updating list:', error);
        }
    }
};

// Update task
window.updateTask = async (taskId) => {
    const newTitle = prompt("Ingrese el nuevo título de la tarea:");
    const newDescription = prompt("Ingrese la nueva descripción de la tarea:");
    if (newTitle || newDescription) {
        try {
            const response = await fetch(`/tasks/${taskId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ title: newTitle, description: newDescription })
            });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            fetchLists();
        } catch (error) {
            console.error('Error updating task:', error);
        }
    }
};

// Initial fetch
fetchLists();


async function importData() {
    const fileInput = document.getElementById('importInput');
    const file = fileInput.files[0];
    if (!file) {
        alert("Por favor, selecciona un archivo para importar.");
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('/import', {
            method: 'POST',
            body: formData
        });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        alert("Datos importados con éxito.");
        fetchLists();
    } catch (error) {
        console.error('Error importing data:', error);
    }
}

async function exportData() {
    try {
        const response = await fetch('/export');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'exported_data.json';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    } catch (error) {
        console.error('Error exporting data:', error);
    }
}


function updateFileName() {
    const fileInput = document.getElementById('importInput');
    const fileLabel = document.getElementById('fileInputLabel');
    const fileName = fileInput.files[0] ? fileInput.files[0].name : "Seleccionar archivo";
    fileLabel.textContent = fileName;
}