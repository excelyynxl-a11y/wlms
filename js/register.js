
function registerParticipant(){

    const name = document.getElementById('participant-name').value.trim();
    const age = parseInt(document.getElementById('participant-age').value);
    const gender = document.getElementById('participant-gender').value;
    const weight = parseFloat(document.getElementById('participant-weight').value);
    const category = determineCategory(gender, weight);

    if (!name || isNaN(age) || age < 12 || !gender || isNaN(weight) || weight <= 0){
        alert("Please fill in all fields with correct value");
        return;
    }

    let participants = JSON.parse(localStorage.getItem('participants')) || []

    const participant = {
        name: name,
        age: age,
        gender: gender,
        weight: weight,
        category: category
    };

    participants.push(participant);
    localStorage.setItem('participants', JSON.stringify(participants));

    // trigger a manual refresh event for view_dashboard,html page 
    window.dispatchEvent(new Event("participantUpdated"));

    showCustomPopup(name);

    document.getElementById('participant-name').value = "";
    document.getElementById('participant-age').value = "";
    document.getElementById('participant-gender').value = "";
    document.getElementById('participant-weight').value = "";
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

function showCustomPopup(name){
    const popup = document.getElementById("register-success-popup");
    const nameSpan = document.getElementById("participant-registered-name");
    
    nameSpan.textContent = name;
    popup.style.display = "flex";

    // auto-hide popup after 2s
    setTimeout(() => {
        popup.style.display = "none";
    }, 2000);
}

document.addEventListener('DOMContentLoaded', function() {
    const nameInput = document.getElementById('participant-name');
    const ageInput = document.getElementById('participant-age');
    const genderInput = document.getElementById('participant-gender');
    const weightInput = document.getElementById('participant-weight');

    function handleEnterKey(event) {
        if (event.key === 'Enter'){
            event.preventDefault();
            registerParticipant();
        }
    }
    nameInput.addEventListener('keyup', handleEnterKey);
    ageInput.addEventListener('keyup', handleEnterKey);
    genderInput.addEventListener('keyup', handleEnterKey);
    weightInput.addEventListener('keyup', handleEnterKey);
})

