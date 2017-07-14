# Disciplina : Linguagens Formais e Automatos
# Aluno      : Pedro Henrique Oliveira Veloso
# Matricula  : 0002346

import xml.etree.ElementTree as ElementTree;
import xml.dom.minidom as minidom;

class AFD(object):
    # OBJETO:
    def __init__(self):
    	""" Objeto AFD, composto pela quintupla M = (E, sigma [alfabeto], delta [transicoes], i, F) """
        self.__E      = [];		# Lista de estados.
        self.__sigma  = [];		# Lista de letras do alfabeto.
        self.__delta  = [];		# Lista de dicionarios {"from": x, "to": y, "read": w}.
        self.__i      = 'None';	# Estado inicial, apenas um e aceito.
        self.__F      = [];		# Lista de estados finais.
    


    # ENTRADA E SAIDA:
    def load(self, local):
        """ Carrega um arquivo '.jff' e o converte para um objeto da classe AFD. """
        root        = ElementTree.parse(local).getroot();
        automaton   = root[1]; # Pula tag <type> (root[0]).

        for child in automaton:
            # Pega todos os estados:
            if (child.tag == 'state'):
                state   = child.attrib['id'];
                initial = child.find('initial');
                final   = child.find('final');

                # Determina se e estado inicial:
                if (initial is not None):
                    initial = True;
                else:
                    initial = False;

                # Determina se e estado final:
                if (final is not None):
                    final = True;
                else:
                    final = False;

                # Adiciona ao automato:
                self.addState(int(state) + 1, initial, final);

            # Pega todas as transicoes:
            # O alfabeto e criado de acordo com as letras
            # recebidas em cada transicao.
            if (child.tag == 'transition'):
                initial = child.find('from').text;
                final   = child.find('to').text;
                read    = child.find('read').text;

                # Adiciona transicao ao automato:
                self.addTransition(int(initial) + 1, int(final) + 1, read);

        return;

    def save(self, local):
        """ Salva um objeto da classe AFD em formato '.jff'. """
        structure   = ElementTree.Element('structure');

        # Tipo do automato:
        aType       = ElementTree.SubElement(structure, 'type');
        aType.text  = 'fa';

        # Automato:
        automaton   = ElementTree.SubElement(structure, 'automaton');

        # Estados:
        for e in self.__E:
            state = ElementTree.SubElement(automaton, 'state');
            state.set('id', str(e));
            if (e == self.__i):
                initial = ElementTree.SubElement(state, 'initial');
            if (e in self.__F):
                final   = ElementTree.SubElement(state, 'final');

        # Transicoes:
        for t in self.__delta:
            trans       = ElementTree.SubElement(automaton, 'transition');
            tfrom       = ElementTree.SubElement(trans, 'from');
            tfrom.text  = str(t['from']);
            tto         = ElementTree.SubElement(trans, 'to');
            tto.text    = str(t['to']);
            read        = ElementTree.SubElement(trans, 'read');
            read.text   = t['consume'];

        # Salvar em arquivo:
        tree = ElementTree.ElementTree(structure);
        tree.write(local);
    	
        return;



    # EQUIVALENCIA (automato minimo):
    def equivalentStates(self):
        """ Retorna uma lista com os estados equivalentes do AFD. """

        # Se for um automato vazio, retorne uma lista vazia:
        if (len(self.__E) == 0):
            return [];

        # Cria uma lista com todas as combinacoes possiveis,
        # Exceto um estado e ele mesmo.
        equivalentes = [];

        # Variaveis para auxiliar a combinacao:
        max = 1;
        combinacao = max;

        for e in range(0, len(self.__E) - 1):
            
            while(combinacao < len(self.__E)):
                state1 = self.__E[combinacao - 1];
                state2 = self.__E[e - 1];

                # Estados finais nao sao equivalentes aos nao finais:
                if((state1 in self.__F) & (state2 in self.__F)) | ((state1 not in self.__F) & (state2 not in self.__F)):
                    equivalentes.append([state1, state2]);

                combinacao = combinacao + 1;

            max = max + 1;
            combinacao = max;

        # Para cada combinacao na lista 'equivalentes',
        i = 0;
        while(i < len(equivalentes)):
            for l in self.__sigma:
                target1 = self.getTarget(equivalentes[i][0], l);
                target2 = self.getTarget(equivalentes[i][1], l);

                # Se os destinos forem diferentes e nao estiverem na lista de equivalentes:
                if(([target1, target2] not in equivalentes) & ([target2, target1] not in equivalentes)) & (target1 != target2):
                    # Remova a combinacao atual da lista:
                    equivalentes.pop(equivalentes.index([equivalentes[i][0], equivalentes[i][1]]));

                    # Inicia no comeco da lista para checar novamente por combinacoes que dependiam
                    # do estado removido:
                    i = 0;
                    break;

            i = i + 1;

        return equivalentes;

    def minimum(self):
        """ Retorna o autonomo minimo do AFD. """

        # Faz uma copia do original:
        min = self.deepcopy();

        # Remove estados inalcancaveis:
        min.removeUnreachableStates();

        # Obtem estados equivalentes:
        equivalentes = min.equivalentStates();

        # Remove o segundo estado equivalente para cada estado da lista:
        for tupla in equivalentes:
            # Todas as transicoes que chegam ao estado a ser removido
            # sao passadas para o primeiro estado:
            # tupla[0] -> estado que permanece. tupla[1] -> estado a ser removido.
            for transicao in min.__delta:
                if(transicao["to"] == tupla[1]):
                    transicao["to"] = tupla[0];

            # Deleta o estado:
            # Se o estado removido for final, seu equivalente sera final:
            if(tupla[1] in min.finals()) & (tupla[0] not in min.finals()):
                min.__F.append(tupla[0]);

            # Se o estado removido for inicial, seu equivalente sera inicial:
            if(tupla[1] == min.__i):
                min.__i = tupla[0];

            min.deleteState(tupla[1]);

        return min;



    # EQUIVALENCIA ENTRE AFDs:
    def equivalents(aut1, aut2):
        """ Determina se dois automatos sao equivalentes. """
    
        # Automatos com alfabetos diferentes nao sao equivalentes:
        if(aut1.__sigma != aut2.__sigma):
            return False;

        # Concatena os automatos num unico automato:
        res = AFD();
        aut3 = aut2.deepcopy();

        # Cria uma copia de aut2 e multiplica a id dos seus estados por 10,
        # a nova id sera usada pra distinguir aut2 de aut1 apos a concatenacao:
        for e in range(0, len(aut3.__E)):
            aut3.__E[e] = aut2.__E[e] * 10;
        for t in aut3.__delta:
            t["from"] = t["from"] * 10;
            t["to"] = t["to"] * 10;
        for f in range(0, len(aut3.__F)):
            aut3.__F[f] = aut3.__F[f] * 10;
        aut3.__i = aut3.__i * 10;

        res.__E = aut1.__E + aut3.__E;
        res.__F = aut1.__F + aut3.__F;
        res.__delta = aut1.__delta + aut3.__delta;
        res.__sigma = aut1.__sigma;
        res.__i = aut1.__i;

        # Determina os estados equivalentes:
        eq = res.equivalentStates();

        # Se os iniciais dos dois automatos sao equivalentes,
        # os automatos sao equivalentes:
        if([aut1.__i, aut3.__i] in eq) | ([aut3.__i, aut1.__i] in eq):
            return True;

        return False;



    # OPERACOES ENTRE AFDs:
    def complement(self):
        """ Determina o complemento do AFD. """
        # Todos os estados finais se tornam nao-finais,
        # Todos os estados nao-finais se tornam finais.
        comp = self.deepcopy();
        finals = comp.finals();

        comp.__F = [];

        # Coloque todos os estados de 'comp' que nao era um estado final:
        for i in comp.__E:
            if (i not in finals):
                comp.__F.append(i);
            
        return comp;

    def union(self, aut2):
        """ Realiza a uniao entre dois AFDs. """
        # Realiza a operacao apenas sobre automatos
        # que aceitam o mesmo alfabeto:
        if (self.__sigma != aut2.__sigma):
            return;

        res = AFD();

        # Pega todas as combinacoes de estado:
        for e in self.__E:
            for e2 in aut2.__E:
                # Para cada letra no alfabeto:
                for l in self.__sigma:
                    # Determina source:
                    source = int(str(e) + str(e2));

                    # Determina target:
                    target1  = self.getTarget(e, l);
                    target2 = aut2.getTarget(e2, l);

                    # Novas transicoes so sao validas se ambos os targets forem um estado valido:
                    if((target1 != "") & (target2 != "")):
	                    target = int(str(target1) + str(target2));
	                    
	                    # Checa se 'source1' e estado final e adiciona estado se nao existir:
	                    if (e in self.finals()) | (e2 in aut2.finals()):
	                        res.addState(source, False, True);
	                    else:
	                        res.addState(source, False, False);

	                    # Checa se 'target' e estado final e adiciona estado se nao existir:
	                    if (target1 in self.finals()) | (target2 in aut2.finals()):
	                        res.addState(target, False, True);
	                    else:
	                        res.addState(target, False, False);

	                    # Adiciona transicao:
	                    res.addTransition(source, target, l);

	                    # Determina estado inicial:
	                    res.__i = int(str(self.__i) + str(aut2.__i));

        # Ordena os conjuntos de estado:
        res.__E.sort();
        res.__F.sort();

        # Remove estados inalcancaveis:
        res.removeUnreachableStates();

        return res;

    def intersection(self, aut2):
        """ Realiza a intersecao entre dois AFDs. """
        # Realiza a operacao apenas sobre automatos
        # que aceitam o mesmo alfabeto:
        if (self.__sigma != aut2.__sigma):
            return;

        res = AFD();

        # Pega todas as combinacoes de estado:
        for e in self.__E:
            for e2 in aut2.__E:
                # Para cada letra no alfabeto:
                for l in self.__sigma:
                    # Determina source:
                    source = int(str(e) + str(e2));

                    # Determina target:
                    target1  = self.getTarget(e, l);
                    target2 = aut2.getTarget(e2, l);

                    # Novas transicoes so sao validas se ambos os targets forem um estado valido:
                    if((target1 != "") & (target2 != "")):
	                    target = int(str(target1) + str(target2));
	                    
	                    # Checa se 'source1' e estado final e adiciona estado se nao existir:
	                    if (e in self.finals()) & (e2 in aut2.finals()):
	                        res.addState(source, False, True);
	                    else:
	                        res.addState(source, False, False);

	                    # Checa se 'target' e estado final e adiciona estado se nao existir:
	                    if (target1 in self.finals()) & (target2 in aut2.finals()):
	                        res.addState(target, False, True);
	                    else:
	                        res.addState(target, False, False);

	                    # Adiciona transicao:
	                    res.addTransition(source, target, l);

	                    # Determina estado inicial:
	                    res.__i = int(str(self.__i) + str(aut2.__i));

        # Ordena os conjuntos de estado:
        res.__E.sort();
        res.__F.sort();

        # Remove estados inalcancaveis:
        res.removeUnreachableStates();

        return res;

    def difference(self, aut2):
        """ Realiza a diferenca entre dois AFDs. """
        # Realiza a operacao apenas sobre automatos
        # que aceitam o mesmo alfabeto:
        if (self.__sigma != aut2.__sigma):
            return;

        # Determina o complemento de 'aut2':
        complement2 = AFD();
        complement2 = aut2.complement();

        # A diferenca e a intersecao entre 'self' e o complemento de 'aut2':
        res = AFD();
        res = self.intersection(complement2);

        return res;



    # CONSULTAS SOBRE AFDs:
    def initial(self):
        """ Retorna o estado inicial do AFD. """
        return self.__i;

    def move(self, estado, palavra):
        """ Dado o estado 'estado', determina o estado final apos ler 'palavra'. """
        e = estado;

        # Itere para cada letra da palavra:
        for i in range(0, len(palavra)):
            # Se a letra nao existir no alfabeto, retorne estado invalido:
            if (palavra[i] not in self.__sigma):
                return "Invalido";
		
            for j in range(0, len(self.__delta)):
                if((self.__delta[j]['from'] == e) and (self.__delta[j]['consume'] == palavra[i])):                   
                    e = self.__delta[j]['to'];
                    break;         
        return e;

    def finals(self):
        """ Retorna todos os estados finais do AFD. """
        return self.__F;



    # ALTERAR AFD:
    def addState(self, id, initial, final):
        """ Adiciona um estado ao automato se ele nao existir. """
        if (int(id) not in self.__E):
            self.__E.append(int(id));
        if (initial):
            self.__i = int(id);
        if (final & (int(id) not in self.finals())):
            self.__F.append(int(id));
        return;

    def addTransition(self, source, target, consume):
        """ Adiciona uma transicao ao automato se ela nao existir. """
        
        # Os estados fornecidos devem pertencer ao automato:
        if(source not in self.__E) | (target not in self.__E):
            return;

        new = {'from': int(source), 'to': int(target), 'consume': consume};
        if (new not in self.__delta):
            self.__delta.append(new);

            # Se 'consume' nao estiver no alfabeto, adicione-o:
            if (str(consume) not in self.__sigma):
                self.__sigma.append(str(consume));
                self.__sigma.sort();
        return;

    def deleteState(self, state):
        """ Deleta o estado 'state' do automato. """
        e = state;

        # Remove estado se ele existir no automato:
        if (e in self.__E):
            self.__E.remove(e);

            # Remove todas as transicoes que envolvem o estado removido:
            i = 0;
            while(i < len(self.__delta)):
                if ((self.__delta[i]['from'] == e) | (self.__delta[i]['to'] == e)):
                    self.__delta.pop(i);
                    i -= 1;
                i += 1;

            # Checa se o estado removido era inicial:
            if (self.__i == e):
                self.__i = 'None';

            # Checa se o estado removido era final:
            if (e in self.__F):
                self.__F.pop(self.__F.index(e));
        return;

    def deleteTransition(self, source, target, consume):   
        """ Deleta a transicao '(source, consume) -> target' do AFD. """
        target = {'from': source, 'to': target, 'consume': str(consume)};

        # Remova apenas se a transicao existir:
        if target in self.__delta:
            index = self.__delta.index(target);
            self.__delta.pop(index);

        return;



    # UTILITARIOS:
    def getTarget(self, source, consume):
        for i in self.__delta:
            if ((i['from'] == source) & (i['consume'] == str(consume))):
                return i['to'];
	   # Transicao inexistente:
        return "";

    def deepcopy(self):
        """ Retorna um novo automato 'res' que e copia de 'self'. """
        res = AFD();

        # Copia todos os estados:
        for e in self.__E:
            ini = False;
            fin = False;            

            if (e == self.__i):
                ini = True;
            if (e in self.__F):
                fin = True;

            res.addState(e, ini, fin);

        # Copia todas as transicoes e letras do alfabeto:
        for t in self.__delta:
            res.addTransition(t['from'], t['to'], t['consume']);

        return res;

    def removeUnreachableStates(self):
        """ Remove estados que nao sao alvo de nenhuma transicao. """
        i = 0;
        while(i < len(self.__E)):
            # Procura por uma transicao que leve ate E[i]:
            found = False;
            for transition in self.__delta:
                if(transition['to'] == self.__E[i]):
                    found = True;

            # Se nao houver uma, deleta o estado:
            if(found == False):
                self.deleteState(self.__E[i]);
                i = 0;  # Volta para o inicio dos estados.
            else:
                i = i + 1;  # Ou prossiga para o proximo estado.

        return;

    def printStates(self):
        """ Imprime todos os estados do AFD. """
        for e in self.__E:
            print(e);

    def printTransitions(self):
        """Imprime todas as transicoes do AFD."""
        for t in self.__delta:
            print(t);

    def printAlphabet(self):
        """ Imprime todas letras do alfabeto do AFD. """
        for r in self.__sigma:
            print(r);

    def __str__(self):
        """ Imprimir todo o automato. """
        # Coleta estados:
        prt = 'E: \t{';
        for i in range(0, len(self.__E) - 1):
            prt += str(self.__E[i]) + ', ';

        if (len(self.__E) > 0):
            prt += str(self.__E[len(self.__E) - 1]);
        prt += '}\n';

        # Coleta alfabeto:
        prt += 'Sigma: \t{';
        for i in range(0, len(self.__sigma) - 1):
            prt += self.__sigma[i] + ', ';

        if (len(self.__sigma) > 0):
            prt += self.__sigma[len(self.__sigma) - 1];
        prt += '}\n';

        # Coleta transicoes:
        if (len(self.__delta) > 0):
            prt += 'Delta: \t{\n\t';
            count = 1;
            for i in range(0, len(self.__delta) - 1):
                prt += '(' + str(self.__delta[i]['from']) + ', ' + self.__delta[i]['consume'] + ') -> ' + str(self.__delta[i]['to']) + ', ';
                
                # Quebra de linha:
                count += 1;
                if (count == 4):
                    count = 1;
                    prt += '\n\t';

            if (len(self.__delta) > 0):
                prt += '(' + str(self.__delta[len(self.__delta) - 1]['from']) + ', ' + self.__delta[len(self.__delta) - 1]['consume'] + ') -> ' + str(self.__delta[len(self.__delta) - 1]['to']) + '\n\t}\n';
        else:
            prt += 'Delta: \t{}\n';

        # Estado inicial:
        prt += 'i: \t' + str(self.__i) + '\n';

        # Coleta estados finais:
        prt += 'F: \t{';
        for i in range(0, len(self.__F) - 1):
            prt += str(self.__F[i]) + ', ';
        if (len(self.__F) > 0):
            prt += str(self.__F[len(self.__F) - 1]);
        prt += '}\n';

        return prt;
