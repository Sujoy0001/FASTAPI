const taskContainer = document.getElementById("tasks");

async function fetchTasks() {
    const res = await fetch("/tasks/");
    const tasks = await res.json();

    taskContainer.innerHTML = "";

    tasks.forEach(task => {
        taskContainer.innerHTML += `
            <div class="task ${task.completed ? "completed" : ""}">
                <h3>${task.title}</h3>
                <p>${task.description}</p>

                ${
                    !task.completed
                    ? `<button onclick="completeTask(${task.id})">Complete</button>`
                    : ""
                }

                <button onclick="deleteTask(${task.id})">Delete</button>
            </div>
        `;
    });
}

async function createTask() {
    const title = document.getElementById("title").value;
    const description = document.getElementById("description").value;

    await fetch("/tasks/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            title,
            description
        })
    });

    document.getElementById("title").value = "";
    document.getElementById("description").value = "";

    fetchTasks();
}

async function completeTask(id) {
    await fetch(`/tasks/${id}`, {
        method: "PUT"
    });

    fetchTasks();
}

async function deleteTask(id) {
    await fetch(`/tasks/${id}`, {
        method: "DELETE"
    });

    fetchTasks();
}

fetchTasks();