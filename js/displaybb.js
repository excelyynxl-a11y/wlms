
// Equipment object
class Equipment {
    constructor(weight){
        this.weight = weight;
    }

    getWeight(){
        return this.weight;
    }
}

class FemaleBar extends Equipment {
    constructor(){
        super(15);
    }
}

class MaleBar extends Equipment {
    constructor(){
        super(20);
    }
}

class Clip extends Equipment {
    constructor(){
        super(2.5);
    }
}

class RedPlate extends Equipment {
    constructor(){ 
        super(25); 
    }
}

class BluePlate extends Equipment {
    constructor(){ 
        super(20); 
    }
}

class YellowPlate extends Equipment {
    constructor(){ 
        super(15); 
    }
}

class GreenPlate extends Equipment {
    constructor(){ 
        super(10); 
    }
}

class WhitePlate extends Equipment {
    constructor(){ 
        super(5); 
    }
}

class SmallRedPlate extends Equipment {
    constructor(){ 
        super(2.5); 
    }
}

class SmallBluePlate extends Equipment {
    constructor(){ 
        super(2); 
    }
}

class SmallYellowPlate extends Equipment {
    constructor(){ 
        super(1.5); 
    }
}

class SmallWhitePlate extends Equipment {
    constructor(){ 
        super(0.5); 
    }
}
 
// barbells
const barbells = {
    "FEMALE": new FemaleBar(),
    "MALE" : new MaleBar()
};

// clips
const clips = [new Clip(), new Clip()]; 

// plate racks
const platesRack = [
    new RedPlate(),
    new BluePlate(),
    new YellowPlate(),
    new GreenPlate(),
    new WhitePlate(),
    new SmallRedPlate(),
    new SmallBluePlate(),
    new SmallYellowPlate(),
    new SmallWhitePlate()
];


// fucntion to validate attempt
function validateAttempt(partcipantGender, attemptWeight){
    const genderMinimumAttemptWeight = {
        "FEMALE": 20,
        "MALE": 25
    }; 

    if (!genderMinimumAttemptWeight.hasOwnProperty(partcipantGender)){
        throw new Error("Invalid gender");
    }

    if (attemptWeight < genderMinimumAttemptWeight[partcipantGender]){
        throw new Error(`${partcipantGender} must lift at least ${genderMinimumAttemptWeight[partcipantGender]}`);
    }
}

// function to sum up weight of all equipments
function calculateTotalWeight(barbellSetup) {
    let totalWeight = 0;
    for (let item of barbellSetup) {
        totalWeight += item.getWeight();
    }
    return totalWeight;
}

function loadPlateOntoBarbell(barload, barbellSetup, attemptWeight){
    for (let plate of platesRack){
        while (barload + 2*plate.getWeight() <= attemptWeight){
            barbellSetup.push(plate);
            barbellSetup.push(plate); 
            barload += 2* plate.getWeight();
        }
    }

    if (Math.abs(barload - attemptWeight) > 0.01){
        throw new Error(`Cannot load exactly to ${attemptWeight} kg`);
    }

    return barbellSetup;
}

function loadBarbellSetup(partcipantGender, attemptWeight){
    validateAttempt(partcipantGender, attemptWeight);

    let barbellSetup = [];
    let barbell = barbells[partcipantGender];
    barbellSetup.push(barbell);

    for (let clip of clips) {
        barbellSetup.push(clip);
    }

    let currentBarLoad = calculateTotalWeight(barbellSetup);
    return loadPlateOntoBarbell(currentBarLoad, barbellSetup, attemptWeight);
}

function reorderBarbellSetup(barbellSetup){
    let bar = barbellSetup.find(item => item instanceof FemaleBar || item instanceof MaleBar);
    let clips = barbellSetup.filter(item => item instanceof Clip);
    let plates = barbellSetup.filter(item => !(item instanceof FemaleBar) && !(item instanceof MaleBar) && !(item instanceof Clip));

    plates.sort((a,b) => a.getWeight() - b.getWeight());

    let leftSide = plates.filter((_, index) => index%2 === 0);
    let rightSide = [...leftSide].reverse(); 

    return [clips[0], ...leftSide, bar, ...rightSide, clips[1]];
}

function getEquipmentClass(equipment){
    if (equipment instanceof FemaleBar) return 'bar';
    if (equipment instanceof MaleBar) return 'bar';
    if (equipment instanceof Clip) return 'clip';
    if (equipment instanceof RedPlate) return 'red-plate';
    if (equipment instanceof BluePlate) return 'blue-plate';
    if (equipment instanceof YellowPlate) return 'yellow-plate';
    if (equipment instanceof GreenPlate) return 'green-plate';
    if (equipment instanceof WhitePlate) return 'white-plate';
    if (equipment instanceof SmallRedPlate) return 'small-red-plate';
    if (equipment instanceof SmallBluePlate) return 'small-blue-plate';
    if (equipment instanceof SmallYellowPlate) return 'small-yellow-plate';
    if (equipment instanceof SmallWhitePlate) return 'small-white-plate';
    return 'equipment';
}

function getEquipmentLabel(equipment){
    if (equipment instanceof FemaleBar) return 'Female Bar';
    if (equipment instanceof MaleBar) return 'Male bar';
    if (equipment instanceof Clip) return 'Clip';
    if (equipment instanceof RedPlate) return '25 kg';
    if (equipment instanceof BluePlate) return '20 kg';
    if (equipment instanceof YellowPlate) return '15 kg';
    if (equipment instanceof GreenPlate) return '10 kg';
    if (equipment instanceof WhitePlate) return '5 kg';
    if (equipment instanceof SmallRedPlate) return '2.5 kg';
    if (equipment instanceof SmallBluePlate) return '2 kg';
    if (equipment instanceof SmallYellowPlate) return '1.5 kg';
    if (equipment instanceof SmallWhitePlate) return '0.5 kg';
    return '';
}

function setupBarbell(){
    const errorDiv = document.getElementById('error-message');
    errorDiv.innerHTML = '';
    errorDiv.style.display = 'none';

    try {
        const gender = document.getElementById('gender').value;
        const weight = parseFloat(document.getElementById('weight').value);

        if (!weight || weight <= 0) {
            throw new Error("Please enter a valid weight");
        }

        console.log('loading barbel  for: ', gender, weight);

        const barbellSetup = loadBarbellSetup(gender, weight);
        console.log('barbell setup: ', barbellSetup); 

        const orderedSetup = reorderBarbellSetup(barbellSetup);
        console.log('ordered setup: ', orderedSetup);

        displayBarbell(orderedSetup, weight);
    } catch (error) {
        console.log('error: ', error.message);
        errorDiv.innerHTML = `<div class="error">${error.message}</div>`;
        errorDiv.style.display = 'block';
        document.getElementById('barbell-display').style.display = 'none';
    }

} 

function displayBarbell(orderedSetup, totalWeight) {
    const container = document.getElementById('barbell-container');
    const weightInfo = document.getElementById('weight-info');
    const display = document.getElementById('barbell-display');

    container.innerHTML = '';

    const barbellAssembly = document.createElement('div');
    barbellAssembly.className = 'barbell-assembly';

    const centerIndex = Math.floor(orderedSetup.length / 2); 
    const leftSide = orderedSetup.slice(0, centerIndex);
    const bar = orderedSetup[centerIndex];
    const rightSide = orderedSetup.slice(centerIndex + 1); 

    leftSide.forEach(equipment => {
        const equipmentDiv = createEquipmentElement(equipment);
        barbellAssembly.appendChild(equipmentDiv);
    });

    // const barLength = calculateBarLength(leftSide, rightSide);
    const barDiv = document.createElement('div');

    barDiv.className = 'equipment bar';
    // barDiv.style.width = `${barLength}px`;
    barDiv.textContent = getEquipmentLabel(bar);
    barbellAssembly.appendChild(barDiv);

    rightSide.forEach(equipment => {
        const equipmentDiv = createEquipmentElement(equipment);
        barbellAssembly.appendChild(equipmentDiv);
    })

    container.appendChild(barbellAssembly);
    weightInfo.textContent = `Total weight: ${totalWeight} kg`;
    display.style.display = 'block';
}

function createEquipmentElement(equipment){
    const equipmentDiv = document.createElement('div');
    equipmentDiv.className = `equipment ${getEquipmentClass(equipment)}`;

    // if u want the equipment to have name labelled on it 
    // if (equipment instanceof Clip) {
    //     equipmentDiv.textContent = "CLIP";
    // } else {
    //     equipmentDiv.textContent = getEquipmentLabel(equipment);
    // }

    return equipmentDiv;
}

function calculateBarLength(leftSide, rightSide){
    let length = 200; 

    const allPlates = [...leftSide, ...rightSide].filter(equipment =>
        !(equipment instanceof Clip) && !(equipment instanceof FemaleBar) && !(equipment instanceof MaleBar)
    ); 

    length += Math.max(allPlates.length * 10, 100);

    return length;
}

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('weight').value = 100;

    const weightInput = document.getElementById('weight');

    if (weightInput) {
        weightInput.addEventListener('keyup', function(event){
            if (event.key === 'Enter'){
                event.preventDefault();
                setupBarbell();
            }
        }
        )
    }
});







