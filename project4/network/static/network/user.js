let targetid = document.querySelector("#user-script").dataset.target;

document.addEventListener('DOMContentLoaded', function () {
    

    document.querySelector("#follow-btn").addEventListener("click", () => {
        fetch(`/follow/${targetid}`, {
            method: 'PUT'
        })
            .then(response => response.json())
            .then(result => {
                console.log(result);

                location.reload(true);
            });
    })
});