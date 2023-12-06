// Code written by Dillon Geary for CSC 49008 Final Project

//fetch the dweet for money made for the day
function fetchMoney(){
  const dweetUrl = 'https://dweet.io/get/latest/dweet/for/DGmon';
  const dataRow = document.getElementById('monRow');
  //fetch dweet and parse
  fetch(dweetUrl)
    .then(response=>response.json())
      .then(data=>{
        if (data.this === "succeeded"){
          //get value and put it in my table
          const val = data.with[0].content.Money;
          const newRow = dataRow.insertRow();
          const title = newRow.insertCell(0);
          const moneyCol = newRow.insertCell(1);
          title.textContent = 'Total';
          moneyCol.textContent = '$ ' + val;
        }
      }) 
}

//fetch the status of my last dweet
function fetchLatestStatus(thingName, imgElementId) {
  const dweetUrl = `https://dweet.io/get/latest/dweet/for/${thingName}`;
  const imgElement = document.getElementById(imgElementId);
  let statusValue;
  // fetch dweet and parse json
  fetch(dweetUrl)
    .then(response => response.json())
    .then(data => {
      console.log(data);
      // look if it was retrieved successfully
      if (data.this === "succeeded") {
        //extract the value
        statusValue = data.with[0].content.S1;
        //set the source depending on if 1/0
        imgElement.src = statusValue === 1
          ? 'green.png' 
          : 'red.png'; 

       console.log(`Thing: ${thingName}, Status: ${statusValue}`);
      } else {
        console.error(`Failed to retrieve the latest status for ${thingName}`);
      }
    })
    .catch(error => {
      console.error(`Error fetching data for ${thingName}: ${error}`);
    });

}

// Execute the function for each sensor when the page loads
document.addEventListener("DOMContentLoaded", function() {
  fetchLatestStatus("DGpark1", "statusImage1");
  fetchLatestStatus("DGpark2", "statusImage2");
  fetchLatestStatus("DGpark3", "statusImage3");
  fetchMoney();
});
