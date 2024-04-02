import os, csv, shutil, json
from datetime import datetime
from dotenv import load_dotenv
from weasyprint import HTML

class Main:

    def main(self):
        print("---")
        print(f"Template : {os.environ.get('TEMPLATE_FILE')}")
        print(f"Input : {os.environ.get('INPUT_DIR')}")
        print(f"Output: {os.environ.get('OUTPUT_DIR')}")
        print("---\n")
        self.read_input_files()

        


    def read_input_files(self):
        
        for input_file_name in os.listdir(os.environ.get('INPUT_DIR')):
            full_input_file_name = os.path.join(os.environ.get('INPUT_DIR'), input_file_name)
            
            # Verifica se é um arquivo e não um diretório
            if os.path.isfile(full_input_file_name):
                print(f">> Obtendo registros do arquivo: {full_input_file_name}")

                registros = []
                with open(full_input_file_name, 'r', encoding='utf-8') as arquivo_csv:
                    leitor_csv = csv.DictReader(arquivo_csv)

                    for linha in leitor_csv:
                        registros.append(linha)

                input_file_noex = self.prepare_output_dir(full_input_file_name)

                # Exibe a lista de dicionários
                for r in registros:
                    print(f"- Gerando declaração para a venda: {r['id']}")
                    self.generate(input_file_noex=input_file_noex, data=r)



    def generate(self, input_file_noex, data):

        html_content = ""
        with open(os.environ.get('TEMPLATE_FILE'), 'r') as arquivo:
            html_content = arquivo.read()

        html_content = html_content.replace("{id}", data['id'])
        # 
        html_content = html_content.replace("{nome.d}", data['nome'])
        html_content = html_content.replace("{endereco.d}", data['endereco'])
        html_content = html_content.replace("{cidade.d}", data['cidade'])
        html_content = html_content.replace("{uf.d}", data['uf'])
        html_content = html_content.replace("{cep.d}", data['cep'])
        html_content = html_content.replace("{cpf.d}", data['cpf'])

        # 
        remetente = self.get_remetente()
        html_content = html_content.replace("{nome.r}", remetente['nome'])
        html_content = html_content.replace("{endereco.r}", remetente['endereco'])
        html_content = html_content.replace("{cidade.r}", remetente['cidade'])
        html_content = html_content.replace("{uf.r}", remetente['uf'])
        html_content = html_content.replace("{cep.r}", remetente['cep'])
        html_content = html_content.replace("{cpf.r}", remetente['cpf'])


        # 
        html_content = html_content.replace("{item1_id}", "1")
        html_content = html_content.replace("{item1_nome}", data['item1_nome'])
        html_content = html_content.replace("{item1_quantidade}", data['item1_quantidade'])
        html_content = html_content.replace("{item1_valor}", data['item1_valor'])

        id2 = "2" if data['item2_nome'] != "" else "."
        html_content = html_content.replace("{item2_id}", id2)
        html_content = html_content.replace("{item2_nome}", data['item2_nome'])
        html_content = html_content.replace("{item2_quantidade}", data['item2_quantidade'])
        html_content = html_content.replace("{item2_valor}", data['item2_valor'])        
        
        id3 = "3" if data['item3_nome'] != "" else "."
        html_content = html_content.replace("{item3_id}", id3)
        html_content = html_content.replace("{item3_nome}", data['item3_nome'])
        html_content = html_content.replace("{item3_quantidade}", data['item3_quantidade'])
        html_content = html_content.replace("{item3_valor}", data['item3_valor'])                

        id4 = "4" if data['item4_nome'] != "" else "."
        html_content = html_content.replace("{item4_id}", id4)
        html_content = html_content.replace("{item4_nome}", data['item4_nome'])
        html_content = html_content.replace("{item4_quantidade}", data['item4_quantidade'])
        html_content = html_content.replace("{item4_valor}", data['item4_valor'])   
        
        id5 = "5" if data['item5_nome'] != "" else "."
        html_content = html_content.replace("{item5_id}", id5)
        html_content = html_content.replace("{item5_nome}", data['item5_nome'])
        html_content = html_content.replace("{item5_quantidade}", data['item5_quantidade'])
        html_content = html_content.replace("{item5_valor}", data['item5_valor'])

        # 
        totais = self.get_totais(data)
        html_content = html_content.replace("{total_quantidade}", f"{totais['total_quantidade']}")
        html_content = html_content.replace("{total_valor}", f"R$ {format(totais['total_valor'], '.2f')}")
        html_content = html_content.replace("{total_peso}", f"{format(totais['total_peso'], '.3f')}")

        # 
        html_content = html_content.replace("{data}", self.get_data(data['data']))


        HTML(string=html_content).write_pdf(f"{os.environ.get('OUTPUT_DIR')}/{input_file_noex}/{data['id']}-declaracao.pdf")




    def prepare_output_dir(self, full_input_filename) -> str :
        '''
        1 - Criar o subdiretorio das vendas do arquivo de input em OUTPUT_DIR
        2 - Copiar arquivo de vendas para o diretorio OUTPUT_DIR
        3 - Retornar o nome do arquivo sem o path e extencao
        '''

        nome_arquivo_com_extensao = os.path.basename(full_input_filename)
        input_filename_noex, _ = os.path.splitext(nome_arquivo_com_extensao)

        diretorio = f"{os.environ.get('OUTPUT_DIR')}/{input_filename_noex}"
        
        try:
            # 
            os.makedirs(diretorio, exist_ok=True)
            print(f"Diretório '{diretorio}' criado com sucesso ou já existia.")

            # 
            shutil.copy(f"{full_input_filename}", diretorio)

            return input_filename_noex

        except Exception as e:
            print(f"Não foi possível criar o diretório '{diretorio}'. Erro: {e}")


    def get_remetente(self):
        remetente_json_file = os.path.join(os.environ.get('INPUT_DIR'), "remetente", "remetente.json")
        try:
            with open(remetente_json_file, 'r', encoding='utf-8') as arquivo:
                dados = json.load(arquivo)

            return dados
        except Exception as e:
            print(f"Ocorreu um erro ao ler o arquivo JSON: {e}")


    def get_data(self, dataDDMMYYYY) -> str:

        meses = {  1: "Janeiro", 2: "Fevereiro", 3: "Março",
                    4: "Abril", 5: "Maio", 6: "Junho",
                    7: "Julho", 8: "Agosto", 9: "Setembro",
                    10: "Outubro", 11: "Novembro", 12: "Dezembro"
                }
        data = datetime.strptime(dataDDMMYYYY, "%d/%m/%Y")
    
        # Formata a data como "São Paulo, DD de Mês de YYYY"
        data_formatada = f"São Paulo, {data.day} de {meses[data.month]} de {data.year}"
    
        return data_formatada


    def get_totais(self, data) -> dict:
        '''
        1 - Receber a linha do pedido como parametro
        2 - Retornar um dict com as chaves: 'total_quantidade', 'total_valor' e 'total_peso'
        '''
        rdata = {"total_quantidade":0, "total_valor":0, "total_peso":0}

        rdata['total_quantidade'] = self._to_int(data['item1_quantidade']) + \
            self._to_int(data['item3_quantidade']) + \
                self._to_int(data['item3_quantidade']) + \
                    self._to_int(data['item4_quantidade']) + \
                        self._to_int(data['item5_quantidade'])

        rdata['total_valor'] = self._to_float(data['item1_valor']) + \
            self._to_float(data['item2_valor']) + \
                self._to_float(data['item3_valor']) + \
                    self._to_float(data['item4_valor']) + \
                        self._to_float(data['item5_valor'])

        rdata['total_peso'] = self._to_float(data['item1_peso']) + \
            self._to_float(data['item2_peso']) + \
                self._to_float(data['item3_peso']) + \
                    self._to_float(data['item4_peso']) + \
                        self._to_float(data['item5_peso'])

        return rdata


    def _to_int(self, s) -> int:
        # Verifica se a string é None ou está em branco (após remover espaços)
        if s is None or s.strip() == "":
            return 0
        try:
            # Tenta converter a string para inteiro
            return int(s)
        except ValueError:
            # Se a conversão falhar (por exemplo, se a string contém letras), retorna 0
            return 0        


    def _to_float(self, s, s2remove="r$") -> float:
        # Verifica se a string é None ou está em branco (após remover espaços)
        _s = s.lower().replace(s2remove, '').replace(',', '.')

        if _s is None or _s.strip() == "":
            return 0.0
        try:
            # Tenta converter a string para float
            return float(_s)
        except ValueError:
            # Se a conversão falhar (por exemplo, se a string contém caracteres não numéricos), retorna 0.0
            return 0.0        




load_dotenv()
Main().main()
