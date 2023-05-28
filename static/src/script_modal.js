// Seleccionamos los botones "Actualizar" y la ventana modal
const updateButtons = document.querySelectorAll('.update-button');
const updateModal = document.getElementById('update-modal');

// Añadimos un evento clic a cada botón "Actualizar"
updateButtons.forEach((button) => {
    button.addEventListener('click', (event) => {
        // Detenemos el evento para evitar que se recargue la página
        event.preventDefault();

        // Obtenemos el ID del usuario a actualizar
        const userId = button.getAttribute('data-id');

        // Enviamos una petición AJAX para obtener los datos del usuario
        const xhr = new XMLHttpRequest();
        xhr.open('GET', `/usuarios/${userId}`);
        xhr.onload = () => {
            if (xhr.status === 200) {
                // Si la petición fue exitosa, cargamos los datos del usuario en los campos de la ventana modal
                const user = JSON.parse(xhr.responseText);
                const updateId = updateModal.querySelector('#update-id');
                const updateNombre = updateModal.querySelector('#update-nombre');
                const updateApellido = updateModal.querySelector('#update-apellido');
                const updateEmail = updateModal.querySelector('#update-email');
                updateId.value = user.id;
                updateNombre.value = user.nombre;
                updateApellido.value = user.apellido;
                updateEmail.value = user.email;

                // Mostramos la ventana modal
                updateModal.style.display = 'block';
            } else {
                console.error(xhr.statusText);
            }
        };
        xhr.onerror = () => console.error(xhr.statusText);
        xhr.send();
    });
});

// Añadimos un evento clic al botón cerrar de la ventana modal
const closeModal = updateModal.querySelector('.close');
closeModal.addEventListener('click', () => {
    updateModal.style.display = 'none';
});

// Añadimos un evento clic fuera de la ventana modal para cerrarla
window.addEventListener('click', (event) => {
    if (event.target == updateModal) {
        updateModal.style.display = 'none';
    }
});
