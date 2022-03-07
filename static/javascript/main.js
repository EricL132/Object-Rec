document.getElementById('mid-container').addEventListener('click', clickImage = () => {
    document.getElementById('image-input').click()
})

document.getElementById('image-input').addEventListener("click", function (e) {
    e.stopPropagation();
    e.target.value = null
});

document.getElementById('uploadAnother').addEventListener('click', () => {
    document.getElementById('image-input').click()
})
//Download photo 
document.getElementById('downloadPhoto').addEventListener('click', () => {
    const newEle = document.createElement('a')
    newEle.download = "image.jpg"
    newEle.href = document.getElementById('output-image').src
    newEle.click();
})

document.getElementById('image-input').addEventListener('change', async (e) => {
    const loadingElement = document.getElementById("loading-icon")
    const midcon = document.getElementById('mid-container')
    const toolElement = document.getElementById('button-tools-container')

    //Resets midcon element
    midcon.removeEventListener("click", clickImage, false)
    midcon.innerHTML = ""
    midcon.style.cursor="auto"
    loadingElement.style.visibility = "visible"
    toolElement.style.visibility = "hidden"
    //converts image to send to server
    const file = document.getElementById('image-input').files[0]
    const fileForm = new FormData()
    fileForm.append('myfile', file)
    //sends POST request to server and server returns new image after reading 
    await fetch('/sendimage', { method: 'POST',headers: {'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value}, body: fileForm }).then(res => { return res.blob() }).then(blob => {
        if (blob.type.includes('image')) {
            //Create new elements for image
            const imageContainerEle = document.createElement('div')
            const imageElement = document.createElement('img')

            
            //Creates image url from returned blob
            var img = URL.createObjectURL(blob)
            imageElement.id = "output-image"
            imageElement.src = img
            imageContainerEle.classList = "output-container"
            imageContainerEle.appendChild(imageElement)
            midcon.appendChild(imageContainerEle)
            midcon.style.borderStyle = "none"
            loadingElement.style.visibility = "hidden"
            //Upload another
            toolElement.style.visibility = "visible"
        }

    })


})

