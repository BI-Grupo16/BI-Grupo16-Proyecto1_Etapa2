import Chart from 'chart.js/auto';

const reviewForm = document.getElementById("reviewForm");
const textButton = document.getElementById("predictTextButton");
const URL = "http://127.0.0.1:8000/prediction";
const URL2 = "http://127.0.0.1:8000/predictions";
const jsonPath = "./assets/recomendations.json";
const fileForm = document.getElementById("fileForm");
const fileButton = document.getElementById("predictFileButton");
let jsonRecomendations;

textButton.addEventListener("click", (event) => {
  event.preventDefault();
  const reviewText = document.getElementById("reviewText").value;
  document.getElementById("reviewText").value = ''; // Limpiar el campo de texto después de enviar

  fetchPrediction(reviewText);
});

const fetchPrediction = (reviewText) => {
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

fileButton.addEventListener("click", async (event) => {
  event.preventDefault();
  const fileInput = document.getElementById("fileUpload");
  const file = fileInput.files[0];

  if (file) {
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch(URL2, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Error al procesar el archivo.");
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'processed_data.csv');
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    } catch (error) {
      console.error('Error:', error);
    }
  } else {
    console.error("No se ha seleccionado ningún archivo.");
  }
});


const renderPie = (dataFetch) => {   
  const elementHTML = document.getElementById('segundaColumna');
  elementHTML.innerHTML= '<canvas id="myPieChart" width="100" height="100"></canvas>';
  const ctx = document.getElementById('myPieChart').getContext('2d');
  let probabilities = dataFetch.probabilities[0];
  probabilities = probabilities.map(element => element.toFixed(2));  // Format to 2 decimal places
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
          tooltip: {
            callbacks: {
              label: function(tooltipItem) {
                let label = tooltipItem.dataset.label || '';
                if (label) {
                  label += ': ';
                }
                const value = parseFloat(tooltipItem.raw).toFixed(2) * 100 + '%';
                return label + value;
              }
            }
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

  // Función para generar estrellas basadas en la calificación
  const generateStars = (calification) => {
      return '⭐'.repeat(calification); 
  };

  const stars = generateStars(calification); 

  divHTML.innerHTML = `
  <div class="containerNumber">
      <div class="number">${calification}</div>
      <div class="stars">${stars}</div>
      <div class="title">Calificación Predicha</div>
  </div>`;

  renderRecomendaciones(calification);
};

const renderReview = (review) =>{
    const elementHTML = document.getElementById('reviewDiv');
    elementHTML.innerHTML = review;
}



// Carga inicial de recomendaciones
fetch(jsonPath)
  .then(response => response.json())
  .then(data => {
    jsonRecomendations = data;
  })
  .catch(error => console.error('Error al cargar el archivo JSON:', error));