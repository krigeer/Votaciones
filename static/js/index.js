function fechaVotacion() {
    const formHtml = document.getElementById("form-fecha-votacion-template").innerHTML;

    Swal.fire({
        title: 'Configurar Fecha de Votación',
        html: formHtml,
        showCancelButton: true,
        focusConfirm: false,
        confirmButtonText: 'Guardar',
        cancelButtonText: 'Cancelar',
        preConfirm: () => {
            const form = document.getElementById("form-fecha-swal");
            const formData = new FormData(form);

            return fetch("", {
                method: "POST",
                body: formData,
                headers: {
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                }
            }).then(response => response.json())
              .then(data => {
                  if (!data.success) throw new Error(data.error || "Error al guardar");
              }).then(() => {
                  Swal.fire("Guardado", "El votante ha sido añadido.", "success").then(() => location.reload());
              }).catch(error => {
                  Swal.fire("Error", error.message, "error");
              });
        }
    });
}


function nuevoVotante() {
    const formHtml = document.getElementById("form-nuevo-votante-template").innerHTML;

    Swal.fire({
        title: 'Nuevo Votante',
        html: formHtml,
        showCancelButton: true,
        focusConfirm: false,
        confirmButtonText: 'Guardar',
        cancelButtonText: 'Cancelar',
        preConfirm: () => {
            const form = document.getElementById("form-nuevo-votante-swal");
            const formData = new FormData(form);

            return fetch("", {
                method: "POST",
                body: formData,
                headers: {
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                }
            }).then(response => response.json())
              .then(data => {
                  if (!data.success) throw new Error(data.error || "Error al guardar");
              }).then(() => {
                  Swal.fire("Guardado", "El votante ha sido añadido.", "success").then(() => location.reload());
              }).catch(error => {
                  Swal.fire("Error", error.message, "error");
              });
        }
    });
}