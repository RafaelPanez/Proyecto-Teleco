let token = "";
const SERVER = "https://healthymed-sedecentral.duckdns.org";

function login() {
    fetch(SERVER + "/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            username: document.getElementById("username").value,
            password: document.getElementById("password").value
        })
    })
    .then(r => r.json())
    .then(data => {
        if (data.access_token) {
            token = data.access_token;
            document.getElementById("result").innerHTML = "Login correcto";
        } else {
            document.getElementById("result").innerHTML =
                "Error: " + (data.message || "credenciales incorrectas");
        }
    })
    .catch(err => {
        document.getElementById("result").innerHTML =
            "Error de conexión: " + err;
    });
}

function getStudies() {
    if (!token) {
        document.getElementById("result").innerHTML =
            "Primero debes iniciar sesión.";
        return;
    }
    fetch(SERVER + "/studies", {
        headers: {
            "Authorization": "Bearer " + token
        }
    })
    .then(r => r.json())
    .then(data => {
        document.getElementById("result").innerHTML =
            JSON.stringify(data, null, 2);
    })
    .catch(err => {
        document.getElementById("result").innerHTML =
            "Error de conexión: " + err;
    });
}
