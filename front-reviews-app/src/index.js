import Chart from 'chart.js/auto';

const form = document.getElementById("reviewForm");
const URL = "http://127.0.0.1:8000/prediction";

const jsonPath = "./assets/recomendations.json"
let jsonRecomendations;


const renderPie = (dataFetch) => {   
    const elementHTML = document.getElementById('segundaColumna');
    elementHTML.innerHTML= '<canvas id="myPieChart" width="100" height="100"></canvas>'
    const ctx = document.getElementById('myPieChart').getContext('2d');
    let probabilities = dataFetch.probabilities[0];
    probabilities = probabilities.map(element => {return element.toFixed(2)});
    const data = {
        labels: ['1', '2', '3', '4', '5'],
        datasets: [
          {
            label: 'Probabilidad',
            data: probabilities,
            backgroundColor: ['#FF0000', '#FF7D03', '#FFF40A', '#8ac73e', '#006837'],
          }
        ]
    };
    const config = {
        type: 'pie',
        data,
        options: {
          responsive: true,
          plugins: {
            legend: {
              position: 'top',
            },
            title: {
              display: true,
              text: 'Probabilidad predicha para cada calificación'
            }
          }
        },
      };
    const myPieChart = new Chart(ctx, config);
};

const renderRecomendaciones = (calification) => {
    const divHTML = document.getElementById("terceraColumna");
    let htmlToRender = `
    <div>
    <h5>RECOMENDACIONES:</h5>
    <ol class="list-group list-group-numbered">`

    const recomendationsObject = jsonRecomendations.recomendaciones[calification-1];
    const recomendations = Object.keys(recomendationsObject);
    recomendations.forEach(recomendation =>{
        htmlToRender+= `
        <li class="list-group-item d-flex justify-content-between align-items-start">
            <div class="ms-2 me-auto">
            <div class="fw-bold">${recomendation}</div>
            ${recomendationsObject[recomendation]}
            </div>
      </li>`
    })

    htmlToRender += `</ol>
                        </div>`

    divHTML.innerHTML = htmlToRender;
}

const renderCalification = (dataFetch) => {
    const calification = dataFetch.predictions[0];
    const divHTML = document.getElementById("primeraColumna");
    divHTML.innerHTML = `
    <div class="containerNumber">
        <div class="number">${calification}</div>
        <div class="title">Calificación Predecida</div>
    </div>`;
    renderRecomendaciones(calification);
    
}

const renderReview = (review) =>{
    const elementHTML = document.getElementById('reviewDiv');
    elementHTML.innerHTML = review;
}


const fetchPrediction = (reviewText) => {
  // Hacer la solicitud POST al endpoint de predicción
  fetch(URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ reviewText }),
  })
    .then((response) => response.json())
    .then(data => {
        renderPie(data);
        renderCalification(data);
        renderReview(reviewText);
    })
    .catch((error) => console.error("Error:", error));
};

form.onsubmit = (event) => {
  event.preventDefault();
  const formText = document.getElementById("reviewText")
  const reviewText = formText.value;
  formText.value = '';

  fetchPrediction(reviewText);
};

fetch(jsonPath)
  .then(response => response.json())
  .then(data => {
    jsonRecomendations = data;
  })
  .catch(error => console.error('Error al cargar el archivo JSON:', error));





