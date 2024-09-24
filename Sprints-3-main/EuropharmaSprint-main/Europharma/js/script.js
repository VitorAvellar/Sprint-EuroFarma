var email = "";

function handleLogin() {
    email = document.getElementById('email').value;
    console.log('Usuário digitado:', email);

    if (email === "usuario") {
        redirectToPage(email);
    } else if (email === "ADM") {
        redirectToPage(email);
    } else {
        window.alert("usuario nao encontrado")
    }
}


function redirectToPage(email) {
    //armazenando o campo no localStorage
    localStorage.setItem("userEmail", email);
   // window.location.href = 'treinamentos.html';

    if (email === "usuario") {
        window.location.href = 'userIni.html';
    } else if (email === "ADM") {
        window.location.href = 'treinamentos.html';
    }
}



function validaUsu() {
    //retornando a variavel salva no localSotrage
    const userEmail = localStorage.getItem("userEmail");
    console.log('A página foi carregada e a função foi chamada.');
    if (userEmail === "usuario") {
        document.getElementById('var_usu').textContent = `${userEmail}`;

    } else if (userEmail === "ADM") {
        document.getElementById('var_usu').textContent = `${userEmail}`;

    }
}