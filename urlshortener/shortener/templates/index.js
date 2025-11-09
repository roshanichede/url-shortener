const form = document.getElementById('f');
const res = document.getElementById('res');

form.addEventListener('submit', (e) => {
  e.preventDefault();
        try {
            const response = await fetch("http://127.0.0.1:8000/urlshortener", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ url: "example" }),
            });
            if (response.ok) {
                const res = await response.json();
                console.log(res);
            }
        } 
        catch (err) {
            console.error(err);
        }
})




    

