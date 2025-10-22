
let selectedParticipantIndex = null;

function editParticipantDetail(index) {
    selectedParticipantIndex = index;

    const participants = JSON.parse(localStorage.getItem('participants')) || [];
    const participant = participants[index];

    document.getElementById('edit-name').value = participant.name;
    document.getElementById('edit-age').value = participant.age;
    document.getElementById('edit-gender').value = participant.gender;
    document.getElementById('edit-weight').value = participant.weight;

    document.getElementById('popupeditparticipant').style.display = 'flex';
}

function saveParticipant() {
    const name = document.getElementById('edit-name').value.trim();
    const age = parseInt(document.getElementById('edit-age').value);
    const gender = document.getElementById('edit-gender').value;
    const weight = parseFloat(document.getElementById('edit-weight').value);

    if (!name || isNaN(age) || age < 12 || !gender || isNaN(weight) || weight <= 0) {
        alert("Please fill in all fields with correct value");
        return;
    }

    const category = determineCategory(gender, weight);
    let participants = JSON.parse(localStorage.getItem('participants')) || [];

    if (selectedParticipantIndex === null) {
        alert("No participant selected for editing.");
        return;
    }

    participants[selectedParticipantIndex] = {
        name,
        age,
        gender,
        weight,
        category
    };

    localStorage.setItem('participants', JSON.stringify(participants));
    document.getElementById('popupeditparticipant').style.display = 'none';
    loadParticipants()

}


function determineCategory(gender, weight){
    const femaleCategories = {
        48: "W48",
        53: "W53",
        58: "W58",
        63: "W63",
        69: "W69",
        77: "W77",
        86: "W86"
    }

    const maleCategories = {
        60: "M60",
        65: "M65",
        71: "M71",
        79: "M79",
        88: "M88",
        98: "M98",
        110: "M110"
    }

    if (gender === "FEMALE"){
        let keys = Object.keys(femaleCategories).map(Number).sort((a,b) => a - b);
        for (let i = 0; i < keys.length; i++){
            if (weight < keys[i]){
                return femaleCategories[keys[i]];
            }
        }
    } 
    
    if (gender === "MALE") {
        let keys = Object.keys(maleCategories).map(Number).sort((a,b) => a - b);
        for (let i = 0; i < keys.length; i++){
            if (weight < keys[i]){
                return maleCategories[keys[i]];
            }
        }
    }

    return gender === "FEMALE" ? "W86+" : "W110+";
}