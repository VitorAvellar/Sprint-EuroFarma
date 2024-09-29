from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Clientes, Exercicio, Setores, AcervoVideos, Pergunta, TipoPergunta, Resposta, Modulos, Material, Treinamentos


class ClienteForm(UserCreationForm):
    nome = forms.CharField(max_length=255)
    setor = forms.ModelChoiceField(queryset=Setores.objects.all())  # Esse campo será atualizado dinamicamente
    data_de_nascimento = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'format': '%Y-%m-%d'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(ClienteForm, self).__init__(*args, **kwargs)
        self.fields['setor'].queryset = Setores.objects.all()  # Atualiza os setores disponíveis

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()

        cliente, created = Clientes.objects.update_or_create(
            usuario=user,
            defaults={
                'nome': self.cleaned_data['nome'],
                'data_de_nascimento': self.cleaned_data['data_de_nascimento'],
                'setor': self.cleaned_data['setor']
            }
        )

        cliente.save()

        return user


class AcervoVideoForm(forms.ModelForm):
    class Meta:
        model = AcervoVideos
        exclude = ('treinamento',)

        widgets = {
            'nome_video': forms.TextInput(attrs={'class': 'form-control', 'autofocus': ''}),
            'url_video': forms.URLInput(attrs={'class': 'form-control'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'setor': forms.Select(attrs={'class': 'form-control'}),
           
        }

    def __init__(self, *args, **kwargs):
        super(AcervoVideoForm, self).__init__(*args, **kwargs)
        self.fields['setor'].queryset = Setores.objects.all()
        # Adiciona os módulos disponíveis

class PerguntaForm(forms.ModelForm):
    username = forms.CharField(max_length=150, help_text="Informe seu nome de usuário já cadastrado")

    class Meta:
        model = Pergunta
        fields = ['username', 'tipo_pergunta', 'texto_pergunta']
        widgets = {
            'tipo_pergunta': forms.Select(attrs={'class': 'form-control'}),
            'texto_pergunta': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError("O usuário informado não existe. Por favor, forneça um nome de usuário válido.")
        return username
    
class RespostaForm(forms.ModelForm):
    class Meta:
        model = Resposta
        fields = ['texto_resposta']  
        widgets = {
            'texto_resposta': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class SetorForm(forms.ModelForm):
    class Meta:
        model = Setores
        fields = ['nome_setor']
        widgets = {
            'nome_setor': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do Setor'}),
        }

class ModuloForm(forms.ModelForm):
    class Meta:
        model = Modulos
        fields = ['nome_modulo', 'video']  # Incluímos o campo vídeo
        widgets = {
            'nome_modulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do Módulo'}),
            'video': forms.Select(attrs={'class': 'form-control'})  # Exibe o dropdown de vídeos
        }

    def __init__(self, *args, **kwargs):
        super(ModuloForm, self).__init__(*args, **kwargs)
        # Adiciona a lista de vídeos disponíveis
        self.fields['video'].queryset = AcervoVideos.objects.all()
        self.fields['video'].label_from_instance = lambda obj: obj.nome_video  # Exibe apenas o nome do vídeo


class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['title', 'file', 'modulo']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título do Material'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'modulo': forms.Select(attrs={'class': 'form-control'})  # Campo de escolha de módulo
        }

    def __init__(self, *args, **kwargs):
        super(MaterialForm, self).__init__(*args, **kwargs)
        self.fields['modulo'].queryset = Modulos.objects.all()  # Adiciona os módulos disponíveis

class ExercicioForm(forms.ModelForm):
    class Meta:
        model = Exercicio
        fields = ['pergunta', 'alternativa_a', 'alternativa_b', 'alternativa_c', 'alternativa_d', 'alternativa_e', 'resposta_correta', 'treinamento', 'modulo']
        widgets = {
             'alternativa_a': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Alternativa A'}),
             'alternativa_b': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Alternativa B'}),
             'alternativa_c': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Alternativa C'}),
             'alternativa_d': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Alternativa D'}),
             'alternativa_e': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Alternativa E'}),
             'pergunta': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escreva sua Pergunta'})
         }
    def clean_resposta_correta(self):
        resposta_correta = self.cleaned_data.get('resposta_correta')
        if not resposta_correta:
            raise forms.ValidationError("Você deve selecionar a resposta correta.")
        return resposta_correta



class TreinamentoForm(forms.ModelForm):
    class Meta:
        model = Treinamentos
        fields = ['nome_treinamento', 'setor']
        widgets = {
            'nome_treinamento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do Treinamento'}),
            'setor': forms.Select(attrs={'class': 'form-control'})  # Campo de escolha de módulo
        }
    def __init__(self, *args, **kwargs):
        super(TreinamentoForm, self).__init__(*args, **kwargs)
        self.fields['setor'].queryset = Setores.objects.all()


class QuestionarioForm(forms.Form):
    treinamento = forms.ModelChoiceField(queryset=Treinamentos.objects.all(), label="Selecione o Treinamento")
    
    def __init__(self, *args, **kwargs):
        perguntas = kwargs.pop('perguntas', None)  # Recebe as perguntas como parâmetro
        super(QuestionarioForm, self).__init__(*args, **kwargs)
        
        if perguntas:
            # Adiciona um campo de resposta para cada pergunta
            for pergunta in perguntas:
                self.fields[f'pergunta_{pergunta.id}'] = forms.ChoiceField(
                    choices=[
                        ('A', pergunta.alternativa_a),
                        ('B', pergunta.alternativa_b),
                        ('C', pergunta.alternativa_c),
                        ('D', pergunta.alternativa_d),
                        ('E', pergunta.alternativa_e) if pergunta.alternativa_e else ('', '')  # Condicional para a alternativa E
                    ],
                    label=pergunta.pergunta,
                    widget=forms.RadioSelect
                )
