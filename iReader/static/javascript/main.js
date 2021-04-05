document.getElementById('mid-container').addEventListener('click', clickImage = () => {
    document.getElementById('image-input').click()
})

document.getElementById('image-input').addEventListener("click", function (e) {
    e.stopPropagation();
    e.target.value = null
});

document.getElementById('image-input').addEventListener('change', async (e) => {
    const file = document.getElementById('image-input').files[0]
    const fileForm = new FormData()
    fileForm.append('myfile', file)
    await fetch('http://localhost:8000/sendimage', { method: 'POST', headers: { 'Cookie': 'csrftoken=3VP14bO9yh1gzNq7wpF8CJpiwbyXjSi6favlJb0yTzuxbhQxkA50zIrWZJ5wFH4W; sessionid=6bdwmrmrurbqivhafujmimcooli6pv54', 'X-CSRFToken': '3VP14bO9yh1gzNq7wpF8CJpiwbyXjSi6favlJb0yTzuxbhQxkA50zIrWZJ5wFH4W', 'X-Requested-With': 'XMLHttpRequest' }, body: fileForm }).then(res => { return res.blob() }).then(blob => {
        if (blob.type.includes('image')) {
            var img = URL.createObjectURL(blob)
            const midcon = document.getElementById('mid-container')
            midcon.style.borderStyle = "none"
            midcon.style.width = "1200px"
            midcon.style.height = "700px"
            midcon.innerHTML = ""
            midcon.style.cursor = "auto"
            midcon.removeEventListener("click", clickImage, false)
            const newImage = document.createElement('img')
            newImage.id = "outputImage"
            newImage.src = img
            midcon.appendChild(newImage)
            document.getElementById('button-tools-container').style.display = "flex"
            document.getElementById('uploadAnother').addEventListener('click', () => {
                document.getElementById('image-input').click()
            })

            document.getElementById('downloadPhoto').addEventListener('click', () => {
                const newEle = document.createElement('a')
                newEle.download = "abs.jpg"
                newEle.href = document.getElementById('outputImage').src
                newEle.click();
            })
        }

    })


})

