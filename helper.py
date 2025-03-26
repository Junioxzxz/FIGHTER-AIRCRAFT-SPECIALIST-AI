def carrega(nome_do_arquivo):
    try:
        with open(nome_do_arquivo, "r", encoding="utf-8") as arquivo:
            dados = arquivo.read()
            return dados
    except UnicodeDecodeError as e:
        print(f"Erro com codificação UTF-8, tentando com 'latin1'. Erro: {e}")
        try:
            with open(nome_do_arquivo, "r", encoding="latin1") as arquivo:
                dados = arquivo.read()
                return dados
        except UnicodeDecodeError as e:
            print(f"Erro com codificação 'latin1'. Erro: {e}")
            raise
    except FileNotFoundError:
        print(f"Erro: O arquivo '{nome_do_arquivo}' não foi encontrado.")
        raise
    except IOError as e:
        print(f"Erro no carregamento de arquivo: {e}")
        raise
    except Exception as e:
        print(f"Erro inesperado ao carregar o arquivo: {e}")
        raise

def salva(nome_do_arquivo, conteudo):
    try:
        with open(nome_do_arquivo, "w", encoding="utf-8") as arquivo:
            arquivo.write(conteudo)
    except IOError as e:
        print(f"Erro ao salvar o arquivo: {e}")
        raise
    except Exception as e:
        print(f"Erro inesperado ao salvar o arquivo: {e}")
        raise




