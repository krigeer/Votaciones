function RegistroInformacion() {
    const formHtml = document.getElementById('form-foto').innerHTML;
    Swal.fire({
        title: 'Completa todos los campos',
        html: formHtml,
        showCancelButton: true,
        focusConfirm: false,
        confirmButtonText: 'Guardar',
        cancelButtonText: 'Cancelar',
        preConfirm:() => {
            const form = document.getElementById("form_foto");
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
                    Swal.fire("Guardado", "Datos  actualizados.", "success").then(() => location.reload());
                }).catch(error => {
                    Swal.fire("Error", error.message, "error");
                });
        }
    })
}

function RegistroPropuesta() {
    const formHtml = document.getElementById('form_propuesta').innerHTML;

    Swal.fire({
        title: 'Completa todos los campos',
        html: formHtml,
        showCancelButton: true,
        focusConfirm: false,
        confirmButtonText: 'Guardar',
        cancelButtonText: 'Cancelar',
        preConfirm: () => {
            const form = Swal.getPopup().querySelector("#form_propuesta"); 
            const formData = new FormData(form);

            return fetch("", {
                method: "POST",
                body: formData,
                headers: {
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                }
            })
            .then(response => response.json())
            .then(data => {
                if (!data.success) throw new Error(JSON.stringify(data.mensaje));
            })
            .then(() => {
                Swal.fire("Guardado", "Datos actualizados.", "success")
                .then(() => location.reload());
            })
            .catch(error => {
                Swal.fire("Error", error.message, "error");
            });
        }
    })
}
