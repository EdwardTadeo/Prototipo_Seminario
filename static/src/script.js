// Mostrar los datos del usuario seleccionado en el formulario de edición
function showUserDataInModal() {
    document.querySelector('#update-nombre').value = selectedUser.nombre;
    document.querySelector('#update-apellido').value = selectedUser.apellido;
    document.querySelector('#update-email').value = selectedUser.email;
  }
  
  // Mostrar la ventana modal al hacer clic en el botón de actualizar
  document.addEventListener("click", (event) => {
    if (event.target.classList.contains("update-button")) {
      const userId = event.target.dataset.id;
      const userRow = event.target.parentNode.parentNode;
      const nombre = userRow.cells[1].textContent;
      const apellido = userRow.cells[2].textContent;
      const email = userRow.cells[3].textContent;
  
      selectedUser = { id: userId, nombre, apellido, email };
      showUserDataInModal();
  
      modal.style.display = "block";
    }
  });
  