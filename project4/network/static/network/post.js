document.addEventListener('DOMContentLoaded', () => {
    const editbuttons = document.querySelectorAll('.edit');
    const likebuttons = document.querySelectorAll('.like-btn');

    editbuttons.forEach(button => {
        button.addEventListener('click', editPost)
    });
    
    likebuttons.forEach(button => {
        button.addEventListener('click', likePost)
    })
});


function likePost() { 
    const counter = document.querySelector(`#like-count${this.dataset.id}`)
    fetch(window.location.origin + '/like', {
        method: 'POST',
        body: JSON.stringify({
            id: this.dataset.id,
            liked: this.dataset.liked
        })
    })
    .then(response => response.json())
    .then(result => {
        if (result.liked === true) {
            this.innerHTML = '<i class="fas fa-thumbs-up">';
            counter.innerHTML = parseInt(counter.innerHTML) + 1;
            return false;
        }else {
            this.innerHTML = '<i class="far fa-thumbs-up">';
            counter.innerHTML = parseInt(counter.innerHTML) - 1;
            return false;     
        }
    })
}
function editPost() {
    const id = this.dataset.id
    let textElement = document.querySelector(`#text${id}`);
    let text = textElement.innerHTML;

    

    textElement.innerHTML =`
        <form id="edit-form">
            <textarea type="text" id="edit-content" class="form-control" required>${text}</textarea>
            <button class="btn btn-primary" type="submit">Edit</button>
        </form>
    `;

    document.querySelector('#edit-form').onsubmit = () => {
        fetch('/edit', {
            method: 'PUT',
            body: JSON.stringify({
                id:id,
                text: document.querySelector('#edit-content').value
            })
        })  
        
        .then(response => response.json())
        .then(result => {
            console.log(result);
            textElement.innerHTML = document.querySelector('#edit-content').value;

        });

    return false;
    }
}

            