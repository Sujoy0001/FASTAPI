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
                <p><strong>Importance:</strong> ${task.importance}</p>

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
    const importance = document.getElementById("importance").value;

    await fetch("/tasks/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            title,
            description,
            importance
        })
    });

    document.getElementById("title").value = "";
    document.getElementById("description").value = "";
    document.getElementById("importance").value = "normal";

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