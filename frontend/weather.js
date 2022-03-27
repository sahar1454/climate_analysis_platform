var DETAIL_KEYS = ["mean", "median"];
var BASE_URL = "http://localhost:8020"
var GET_CITIES_URL = BASE_URL + "/cities";
var GET_CITY_DETAILS_URL = BASE_URL + "/stats/cities/";
var GET_COUNTRY_DETAILS_URL = BASE_URL + "/stats/canada/";

function getCityList() {

  $.ajax({url: GET_CITIES_URL}).then(function(data) {
    let citySelect = $("#cities");
    let cityList = JSON.parse(data);
    let cityListSorted = [];
    for (let i=0; i<cityList["data"].length; i++) {
      cityListSorted.push(cityList["data"][i].city);
    }
    cityListSorted.sort();
    for (let i=0; i<cityListSorted.length; i++) {
      let city = cityListSorted[i];
      jQuery("<option>", {text: city}).appendTo(citySelect);
    }
    if (cityListSorted.length > 0) {
        let selectedCity = $("#cities").val();
        getTemperatureDetails(GET_CITY_DETAILS_URL + selectedCity + "/", $("#city_details"));
    }
  });
}

function getTemperatureDetails(detailsUrl, resultElement) {

  resultElement.empty();
  let weatherDate = $("#weather_date").val();
  $.ajax({url: detailsUrl + weatherDate}).then(function(data) {
    let temperatureDetails = JSON.parse(data);
    for (let i=0; i<temperatureDetails["data"].length; i++) {
    temperatureDetail = temperatureDetails["data"][i];
    const keys = Object.keys(temperatureDetail);
      for (let j=0; j<keys.length; j++) {
        if (DETAIL_KEYS.includes(keys[j])) {
          let resultDiv = jQuery("<div>", {class: "result"}).appendTo(resultElement);
          jQuery("<label>", {text: keys[j]}).appendTo(resultDiv);
          temperature = jQuery("<span>", {text: Number(temperatureDetail[keys[j]]).toFixed(2) + " \u00B0C"}).appendTo(resultDiv);  
        }
      }
    }
  });
}

function initialize() {

  getTemperatureDetails(GET_COUNTRY_DETAILS_URL, $("#country_details"));
  getCityList();
  $("#cities").on("change", function() {
    let selectedCity = $("#cities").val();
    getTemperatureDetails(GET_CITY_DETAILS_URL + selectedCity + "/", $("#city_details"));
  });
  $("#weather_date").on("change", function() {
    let selectedCity = $("#cities").val();
    getTemperatureDetails(GET_COUNTRY_DETAILS_URL, $("#country_details"));
    getTemperatureDetails(GET_CITY_DETAILS_URL + selectedCity + "/", $("#city_details"));
  });
}