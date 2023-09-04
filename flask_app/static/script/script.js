const form = document.querySelector("#newForum")
const tableBody = document.querySelector("#table_body")
const errorDisplay = document.querySelector("#error_display")


function addForum(event) {
    event.preventDefault()
    console.log('submitted')
    let formData = new FormData(form)
    fetch('/api/forums/create', {
        method: 'POST',
        body: formData
    })
        .then(res => res.json())
        .then(data => {
            console.log(data)
            errorDisplay.innerHTML = "";
            if (data.hasOwnProperty('errors')) {
                console.log('errors exist')
                for (let error of data.errors) {
                    errorDisplay.innerHTML += `<p class = 'text-danger'> ${error}</p>`
                }
            }
            else {

                tableBody.innerHTML += `
                <tr>
                    <th class='text-center' scope="row">${data.name}</th>
                    <td class='text-center'>${data.subject}</td>
                    <td class='text-center'>${data.date_posted}</td>
                    <td class='text-center'>${data.user_name}</td>
                    <td class='text-center'>
                        <a href="/forums/${data.id}/view">View Forum</a>
                        <a href="/forums/${data.id}/edit">| Edit</a>
                        <a href="/forums/${data.id}/delete">| Delete</a>
                    </td>
                </tr>
                `
                form.name.value = ""
                form.subject.value = ""
                form.date_posted.value = ""
                form.posting.value = ""
            }
        })
        .catch(err => console.log(err))
}