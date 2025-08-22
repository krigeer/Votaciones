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







function enviarMensajeMasivo() {
    document.getElementById("btnEnviarMensaje").addEventListener("click", function () {
        const url = this.dataset.url;

        Swal.fire({
            title: 'Escribe el mensaje a enviar',
            input: 'textarea',
            inputPlaceholder: 'Escribe tu mensaje aquí...',
            showCancelButton: true,
            confirmButtonText: 'Enviar',
            cancelButtonText: 'Cancelar',
            preConfirm: (mensaje) => {
                if (!mensaje) {
                    Swal.showValidationMessage('Debes escribir un mensaje');
                }
                return mensaje;
            }
        }).then((result) => {
            if (result.isConfirmed) {

                // Mostrar mensaje de espera
                Swal.fire({
                    title: 'Enviando mensajes...',
                    html: 'Por favor espera mientras se envían los correos',
                    allowOutsideClick: false,
                    didOpen: () => {
                        Swal.showLoading(); //  spinner
                    }
                });

                fetch(url, {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": document.querySelector('meta[name="csrf-token"]').getAttribute('content'),
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ mensaje: result.value })
                })
                .then(response => {
                    if (!response.ok) throw new Error("Error al enviar");
                    return response.json();
                })
                .then(data => {
                    Swal.close(); // Cierra "enviando"

                    if (data.ok) {
                        let detalleFallidos = "";
                        if (data.fallidos.length > 0) {
                            detalleFallidos = `
                                <br><strong>Correos fallidos:</strong><ul style="text-align:left;">
                                    ${data.fallidos.map(f => `<li>${f.correo}</li>`).join('')}
                                </ul>
                            `;
                        }

                        Swal.fire({
                            icon: 'success',
                            title: 'Mensajes enviados',
                            html: `
                                <p><strong>Total destinatarios:</strong> ${data.total}</p>
                                <p><strong>Enviados correctamente:</strong> ${data.enviados}</p>
                                <p><strong>Fallidos:</strong> ${data.fallidos.length}</p>
                                ${detalleFallidos}
                            `
                        });
                    } else {
                        Swal.fire('Error', data.error || 'Error inesperado en el servidor', 'error');
                    }
                })
                .catch(error => {
                    Swal.close();
                    console.error(error);
                    Swal.fire('Error', 'No se pudo enviar el mensaje', 'error');
                });
            }
        });
    });
}

document.addEventListener("DOMContentLoaded", function () {
    enviarMensajeMasivo();
});



