
// load localStorage
window.onload = function() {
    const participants = JSON.parse(localStorage.getItem("participants")) || [];

    if (participants.length === 0){
        this.document.getElementById("participant-container").textContent = "No participants registered yet.";
        return;
    }

    participants.forEach(p => {
        createParticipantBox(p.name, p.gender, p.category);
    });
}

function createParticipantBox(name, gender, category){
    const container = document.getElementById("participants-container");

    if (!container){
        return;
    }

    const box = document.createElement("div");
    box.className = "participant-box";

    const nameBox = document.createElement("div");
    nameBox.className = "participant-name";
    nameBox.textContent = name;

    const genderBox = document.createElement("div");
    genderBox.className = "participant-gender";
    genderBox.textContent = gender; 

    const categoryBox = document.createElement("div");
    categoryBox.className = "participant-category";
    categoryBox.textContent = category;

    box.appendChild(nameBox);
    box.appendChild(genderBox);
    box.appendChild(categoryBox);

    container.appendChild(box);
}