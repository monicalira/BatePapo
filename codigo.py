
import flet

def main(pagina):
    texto = flet.Text("Bate papo")

    chat = flet.Column()

    nome_usuario = flet.TextField(label="Escreva seu nome")

    def enviar_mensagem_tunel(mensagem):
        tipo = mensagem["tipo"]
        if tipo == "mensagem":
            texto_mensagem = mensagem["texto"]
            usuario_mensagem = mensagem["usuario"]
            # adicionar a mensagem no chat
            chat.controls.append(flet.Text(f"{usuario_mensagem}: {texto_mensagem}"))
        else:
            usuario_mensagem = mensagem["usuario"]
            chat.controls.append(flet.Text(f"{usuario_mensagem} entrou no chat", 
                                         size=12, italic=True, color=flet.colors.PURPLE_500))
        pagina.update()

    pagina.pubsub.subscribe(enviar_mensagem_tunel)

    def enviar_mensagem(evento):
        pagina.pubsub.send_all({"texto": campo_mensagem.value, "usuario": nome_usuario.value,
                                "tipo": "mensagem"})
        # limpar o campo de mensagem
        campo_mensagem.value = ""
        pagina.update()

    campo_mensagem = flet.TextField(label="Digite uma mensagem", on_submit=enviar_mensagem)
    botao_enviar_mensagem = flet.ElevatedButton("Enviar", on_click=enviar_mensagem)

    def entrar_popup(evento):
        pagina.pubsub.send_all({"usuario": nome_usuario.value, "tipo": "entrada"})
        # adicionar o chat
        pagina.add(chat)
        # fechar o popup
        popup.open = False
        # remover o botao iniciar chat
        pagina.remove(botao_iniciar)
        pagina.remove(texto)
        # criar o campo de mensagem do usuario
        # criar o botao de enviar mensagem do usuario
        pagina.add(flet.Row(
            [campo_mensagem, botao_enviar_mensagem]
        ))
        pagina.update()

    popup = flet.AlertDialog(
        open=False, 
        modal=True,
        title=flet.Text("Bem vindo ao Bate papo"),
        content=nome_usuario,
        actions=[flet.ElevatedButton("Entrar", on_click=entrar_popup)],
        )

    def entrar_chat(evento):
        pagina.dialog = popup
        popup.open = True
        pagina.update()

    botao_iniciar = flet.ElevatedButton("Iniciar chat", on_click=entrar_chat)

    pagina.add(texto)
    pagina.add(botao_iniciar)

flet.app(target=main, view=flet.WEB_BROWSER, port=8000)

# deploy
