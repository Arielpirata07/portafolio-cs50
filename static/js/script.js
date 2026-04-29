// Espera a que el documento cargue
    document.addEventListener("DOMContentLoaded", function() {
        // Selecciona todas las alertas
        let alertas = document.querySelectorAll('.alert');
        
        alertas.forEach(function(alerta) {
            // Después de 4000 milisegundos (4 segundos)...
            setTimeout(function() {
                // Usa la animación de Bootstrap para cerrarla
                let bsAlert = new bootstrap.Alert(alerta);
                bsAlert.close();
            }, 4000);
        });
    });
    
///////////// TO TOP BOTON /////////////////////////////
const btnToTop = document.getElementById("btnToTop");

// Mostrar/ocultar el botón al hacer scroll
window.addEventListener("scroll", () => {
  if (window.scrollY > 500) {
    btnToTop.classList.add("show");
  } 
  else {
    btnToTop.classList.remove("show");
  }
});

// Scroll suave al hacer clic
btnToTop.addEventListener("click", (e) => {
  e.preventDefault();
  window.scrollTo({
    top: 0,
    behavior: "smooth"
  });
});


function reveal() {
    var reveals = document.querySelectorAll(".reveal");
    for (var i = 0; i < reveals.length; i++) {
        var windowHeight = window.innerHeight;
        var elementTop = reveals[i].getBoundingClientRect().top;
        var elementVisible = 100; // Cuántos píxeles antes de aparecer
        if (elementTop < windowHeight - elementVisible) {
            reveals[i].classList.add("active");
        }
    }
}
window.addEventListener("scroll", reveal);
reveal(); // Para que ejecute al cargar la página
