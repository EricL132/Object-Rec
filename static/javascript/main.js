document.getElementById('mid-container').addEventListener('click', clickImage = () => {
    document.getElementById('image-input').click()
})

document.getElementById('image-input').addEventListener("click", function (e) {
    e.stopPropagation();
    e.target.value = null
});

document.getElementById('image-input').addEventListener('change', async (e) => {
    //converts image to send to server
    const file = document.getElementById('image-input').files[0]
    const fileForm = new FormData()
    fileForm.append('myfile', file)
    //sends POST request to server and server returns new image after reading 
    await fetch('/sendimage', { method: 'POST',headers: {'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value}, body: fileForm }).then(res => { return res.blob() }).then(blob => {
        if (blob.type.includes('image')) {
            //Create new elements for image
            const midcon = document.getElementById('mid-container')
            const imageContainerEle = document.createElement('div')
            const imageElement = document.createElement('img')
            //Resets midcon element
            midcon.innerHTML = ""
            midcon.removeEventListener("click", clickImage, false)
            //Creates image url from returned blob
            var img = URL.createObjectURL(blob)
            imageElement.id = "output-image"
            imageElement.src = img
            imageContainerEle.classList = "output-container"
            imageContainerEle.appendChild(imageElement)
            midcon.appendChild(imageContainerEle)
            midcon.style.borderStyle = "none"

            //Upload another
            document.getElementById('button-tools-container').style.display = "flex"
            document.getElementById('uploadAnother').addEventListener('click', () => {
                document.getElementById('image-input').click()
            })
            //Download photo 
            document.getElementById('downloadPhoto').addEventListener('click', () => {
                const newEle = document.createElement('a')
                newEle.download = "abc.jpg"
                newEle.href = document.getElementById('outputImage').src
                newEle.click();
            })
        }

    })


})

