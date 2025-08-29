function checkDuplicate() {
    let q1 = document.getElementById("question1").value;
    let q2 = document.getElementById("question2").value;

    fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ 
            question1: q1, 
            question2: q2 
        })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("result").innerText = 
            `Result: ${data.result} (Score: ${data.similarity_score.toFixed(2)})`;
    })
    .catch(error => {
        console.error("Error:", error);
        document.getElementById("result").innerText = "Error: Backend not responding";
    });
}