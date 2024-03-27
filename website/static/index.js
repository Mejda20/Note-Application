// Function to show the edit form modal
function showEditForm(noteId) {
  // Fetch the note content using its ID
  fetch(`/get-note/${noteId}`)
    .then(response => response.json())
    .then(data => {
      // Populate the edit form with the note content
      document.getElementById('editNoteContent').value = data.note.data;
      // Set the note ID as a data attribute of the save button
      document.getElementById('saveEditedNoteBtn').setAttribute('data-note-id', noteId);
      // Show the edit form modal
      $('#editNoteModal').modal('show');
    })
    .catch(error => console.error('Error fetching note:', error));
}

// Function to save the edited note content
function saveEditedNote() {
  // Get the edited note content from the textarea
  const editedContent = document.getElementById('editNoteContent').value;
  // Get the note ID from the save button's data attribute
  const noteId = document.getElementById('saveEditedNoteBtn').getAttribute('data-note-id');

  // Send a POST request to update the note content
  fetch(`/edit-note/${noteId}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ content: editedContent })
  })
  .then(response => {
    if (response.ok) {
      // Reload the page after successfully saving the edited note
      window.location.reload();
    } else {
      // Handle errors if any
      console.error('Error editing note:', response.status);
    }
  })
  .catch(error => console.error('Error editing note:', error));
}
