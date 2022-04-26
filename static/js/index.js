function reqListener () {
  pred = this.responseText
  console.log("Response: ", pred)
  document.getElementById("predicted-value").innerText = "Cost: " + pred
}

function predict(event) {
  event.preventDefault()
  data = {
    'region': "",
    'car_value': 0.0,
    'group_size': 0,
    'car_age': 0,
    'risk_factor': 0,
    'age_oldest': 0,
    'c_previous': 0,
    'duration_previous': 0,
    'home_owner': false,
    'married_couple': false
  }
  console.log("Predicting: ")
  
  region = document.getElementById("selectRegion").value
  carValue = document.getElementById("selectCarValue").value

  groupSize = document.getElementById("inputGroupSize").value
  carAge = document.getElementById("inputCarAge").value
  riskFactor = document.getElementById("inputRiskFactor").value
  ageOldest = document.getElementById("inputAgeOldest").value
  ageYoungest = document.getElementById("inputAgeYoungest").value
  cPrevious = document.getElementById("inputCPrevious").value
  durationPrevious = document.getElementById("inputDurationPrevious").value

  homeOwnership = document.getElementById("chkHomeOwner").checked
  marriedCouple = document.getElementById("chkMarriedCouple").checked
  
  coverages = {
    'A': document.getElementById("inputCovA").value,
    'B': document.getElementById("inputCovB").value,
    'C': document.getElementById("inputCovC").value,
    'D': document.getElementById("inputCovD").value,
    'E': document.getElementById("inputCovE").value,
    'F': document.getElementById("inputCovF").value,
    'G': document.getElementById("inputCovG").value,
  }

  data = {
    'region': region,
    'car_value': carValue,
    'group_size': groupSize,
    'car_age': carAge,
    'risk_factor': riskFactor,
    'age_oldest': ageOldest,
    'age_youngest': ageYoungest,
    'C_previous': cPrevious,
    'duration_previous': durationPrevious,
    'coverages': coverages,
    'homeowner': homeOwnership,
    'married_couple': marriedCouple
  }

  console.log("Sending: ")
  console.log(data)
  
  var oReq = new XMLHttpRequest();
  oReq.addEventListener("load", reqListener);
  oReq.open("POST", "/predict", false);
  oReq.setRequestHeader("Content-type", "application/json");
  oReq.send(JSON.stringify(data));
}

