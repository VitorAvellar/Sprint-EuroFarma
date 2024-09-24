document.getElementById('cadastroForm').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const nome = document.getElementById('nome').value;
    const email = document.getElementById('email').value;
    const senha = document.getElementById('senha').value;
    const errorDiv = document.getElementById('error');
    
    errorDiv.innerHTML = ''; // Limpa mensagens anteriores

    // Validação simples
    if (nome === '' || email === '' || senha === '') {
        errorDiv.innerHTML = 'Por favor, preencha todos os campos.';
        return;
    }

    if (senha.length < 6) {
        errorDiv.innerHTML = 'A senha deve ter no mínimo 6 caracteres.';
        return;
    }

    // Se a validação passar, exibir uma mensagem de sucesso (você pode fazer um POST para backend aqui)
    alert('Cadastro realizado com sucesso!');
});