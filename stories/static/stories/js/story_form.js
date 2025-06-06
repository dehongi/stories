// Initialize CKEditor
function initializeEditor(contentFieldId, existingContent = null) {
    const contentField = document.querySelector(contentFieldId);

    ClassicEditor
        .create(document.querySelector('#editor-container'), {
            toolbar: ['heading', '|', 'bold', 'italic', 'link', 'bulletedList', 'numberedList', 'blockQuote'],
            placeholder: 'Write your story here...'
        })
        .then(editor => {
            // Initialize with existing content
            if (existingContent) {
                editor.setData(existingContent);
            } else if (contentField.value) {
                editor.setData(contentField.value);
            }

            // Update the hidden textarea before form submission
            document.getElementById('storyForm').addEventListener('submit', function (e) {
                const content = editor.getData();
                contentField.value = content;

                // If publishing (not draft) and content is empty, prevent submission
                if (e.submitter && e.submitter.value === 'publish' && !content.trim()) {
                    e.preventDefault();
                    alert('Please write some content before publishing.');
                    return false;
                }
            });

            // Update hidden field on editor changes
            editor.model.document.on('change:data', () => {
                contentField.value = editor.getData();
            });
        })
        .catch(error => {
            console.error('CKEditor initialization error:', error);
            const editorContainer = document.querySelector('#editor-container');
            const errorMessage = document.createElement('div');
            errorMessage.className = 'alert alert-danger mt-2';
            errorMessage.innerHTML = '<i class="bi bi-exclamation-triangle me-2"></i>Error initializing editor. Please refresh the page or contact support.';
            editorContainer.appendChild(errorMessage);
        });
}
