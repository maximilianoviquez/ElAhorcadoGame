from flask import Flask, render_template, request
import random
import string
from palabras import palabras

app = Flask(__name__)

vidas_diccionario_visual = {
    0: """
        ---------------
        | /           |
        |/            |
        |            ( )
        |             |
        |            / \\
        |
        |
        |
        |
      """,
    1: """
        ---------------
        | /           |
        |/            |
        |            ( )
        |             |
        |            / 
        |
        |
        |
        |
      """,
    2: """
        ---------------
        | /           |
        |/            |
        |            ( )
        |             |
        |            
        |
        |
        |
        |
      """,
    3: """
        ---------------
        | /           |
        |/            |
        |            ( )
        |             |
        |            
        |
        |
        |
        |
      """,
    4: """
        ---------------
        | /           |
        |/            |
        |            ( )
        |             | 
        |            /
        |
        |
        |
        |
      """,
    5: """
        ---------------
        | /           |
        |/            |
        |            ( )
        |             |
        |
        |
        |
        |
        |
      """,
    6: """
        ---------------
        | /           |
        |/            |
        |            ( )
        |             
        |
        |
        |
        |
        |
      """,
    7: """
        ---------------
        | /           |
        |/            |
        |            
        |             
        |
        |
        |
        |
        |
      """,
}

def obtener_palabra_valida(palabras):
    palabra = random.choice(palabras)
    while '-' in palabra or ' ' in palabra:
        palabra = random.choice(palabras)
    return palabra.upper()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        letra_usuario = request.form['letra'].upper()
        palabra = request.form['palabra']
        letras_adivinadas = set(request.form['letras_adivinadas'])
        letras_por_adivinar = set(request.form['letras_por_adivinar'])
        vidas = int(request.form['vidas'])

        if letra_usuario in letras_adivinadas:
            mensaje = "Ya elegiste esa letra. Por favor, elige una nueva letra."
        elif letra_usuario not in string.ascii_uppercase:
            mensaje = "Esta letra no es válida."
        else:
            letras_adivinadas.add(letra_usuario)
            if letra_usuario in letras_por_adivinar:
                letras_por_adivinar.remove(letra_usuario)
                mensaje = ""
            else:
                vidas -= 1
                mensaje = f"\nTu letra, {letra_usuario}, no está en la palabra."

        if vidas == 0:
            mensaje = f"Ahorcado! Has perdido el juego. La palabra era: {palabra}!"
            juego_terminado = True
        elif not letras_por_adivinar:
            mensaje = f"Has ganado! Adivinaste la palabra: {palabra}!"
            juego_terminado = True
        else:
            juego_terminado = False

        palabra_lista = [letra if letra in letras_adivinadas else '-' for letra in palabra]

        return render_template('index.html', 
                               palabra=' '.join(palabra_lista), 
                               letras_adivinadas=' '.join(sorted(letras_adivinadas)), 
                               vidas=vidas, 
                               vidas_visual=vidas_diccionario_visual[vidas], 
                               mensaje=mensaje,
                               palabra_original=palabra,
                               letras_por_adivinar=''.join(letras_por_adivinar),
                               juego_terminado=juego_terminado)

    else:
        palabra = obtener_palabra_valida(palabras)
        letras_por_adivinar = set(palabra)
        letras_adivinadas = set()
        vidas = 7
        palabra_lista = ['-' for _ in palabra]

        return render_template('index.html', 
                               palabra=' '.join(palabra_lista), 
                               letras_adivinadas='', 
                               vidas=vidas, 
                               vidas_visual=vidas_diccionario_visual[vidas], 
                               mensaje='',
                               palabra_original=palabra,
                               letras_por_adivinar=''.join(letras_por_adivinar),
                               juego_terminado=False)

if __name__ == '__main__':
    app.run(debug=True)