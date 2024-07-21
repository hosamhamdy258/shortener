let clipboard = new ClipboardJS(".btn");

clipboard.on("success", function (e) {
    let copyBtn = document.getElementById(e.trigger.id);
    const greenColor = "btn-success"
    copyBtn.classList.add(greenColor);
    setTimeout(() => {
        copyBtn.classList.remove(greenColor);
    }, "3000");
    e.clearSelection();
});


function get_shorted_url() {
    const urlInput = document.getElementById("target-url");
    const url = urlInput.value;
    fetch("", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url }),
    })
        .then(async (response) => {
            if (response.ok) {
                return response.json();
            } else {
                const errorData = await response.json();
                throw new Error(errorData.message);
            }
        })
        .then((json) => {
            const shortedUrl = `${location.href}${json.message}`;
            document.getElementById("shorted-url").value = shortedUrl;
        })
        .catch((error) => {
            const errorElement = document.getElementById("target-url-label")
            const shortenBtn = document.getElementById("shorten-btn")
            const labelText = errorElement.textContent
            const redColor = "btn-danger"
            const textColor = "text-danger"
            shortenBtn.classList.add(redColor);
            errorElement.classList.add(textColor);
            errorElement.textContent = error.message;
            setTimeout(() => {
                shortenBtn.classList.remove(redColor);
                errorElement.classList.remove(textColor);
                errorElement.textContent = labelText;
            }, "3000");
        });
}
