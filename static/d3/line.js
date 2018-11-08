(function($){
  $(document).ready(function(){
    // Carga de JSON (desde archivo o API)
    fetch('/static/plot.JSON')
    .then(response => response.json())
    .then((data)=>{
      console.log("data", data);

      // Lógica D3 para graficar
      let container = $("#graph")
      let width = container.width()
      let height = container.height()
      let svg = d3.select("#graph").append("svg")
      .attr("width", "100%")
      .attr("height", "100%")

      


    })
    .catch((e)=>{
      console.log("Error cargando JSON", e);
    })
  });

})(jQuery);
