const form = document.querySelector("#newForum")
const tableBody = document.querySelector("#table_body")



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
        )
        .catch(err => console.log(err))
}