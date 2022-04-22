from nltk.corpus import stopwords
import re
import pandas as pd

df_g_f = pd.read_json (r'gennaio-febbraio-buono.json')
df_m_a = pd.read_json (r'marzo-aprile-buono.json')


df_g_f = df_g_f[["title"]]
df_m_a = df_m_a[["title"]]
df_g_a = df_m_a[["title"]]

df_g_f = df_g_f[df_g_f['title'] != 'no titolo']
df_m_a = df_m_a[df_m_a['title'] != 'no titolo']
df_g_a = df_g_a[df_g_a['title'] != 'no titolo']

dataset_totale = pd.concat([df_g_f, df_m_a])

print(dataset_totale.size)
print(df_g_a.size)
print(df_m_a.size)



def controllo_nome(word):
    if(len(word) > 0 and word[0].isupper()):
       valid = True
       for i in range (1, len(word)):
           if(word[i].isupper()):
               valid=False
               break
       return valid
    return False



# Lista utilizzata per inserire tutti i singoli nodi che si
# creeranno durante l'esecuzione della funzione
lista_nodi = []

# Funzione utilizzata per la pulizia del testo
def pulisci_stringhe(text):
    if text: #Se il testo che analizziamo non è vuoto

        #Lista utilizzata per l'unione di nomi maiuscoli consecutivi
        lista_nomi_maiuscoli = [] 
        
        #Lista finale delle parole dopo la pulizia
        lista_nomi_parole = []       
        
        #Si distanziano tutti i simboli prima dello split
        text = re.sub(r",", " , ", text)
        text = re.sub(r"\:", " : ", text)
        text = re.sub(r"\'", " ' ", text)
        text = re.sub(r"\!", " ! ", text)
        text = re.sub(r"\?", " ? ", text)
        text = re.sub(r"\"", " \" ", text)
        text = re.sub(r"“", " “ ", text)
        text = re.sub(r"”", " ” ", text)
        text = re.sub(r"\’", " ’ ", text)
        text = re.sub(r"-", " - ", text)
        text = re.sub(r"\.", " . ", text)
        text = re.sub(r"\(", " ( ", text)
        text = re.sub(r"\)", " ) ", text)
        text = re.sub(r"«", " « ", text)
        text = re.sub(r"»", " » ", text)
        text = text.split()
       
        lista = ['.' , '?', '!', '“', '”', '’', '"']            
        prima_parola = text[0]
        #Se la prima lettera della prima parola non è maiuscola ed è diversa da # allora:
        if(not(prima_parola[0][0].isupper()) and prima_parola[0][0] != '#'):
            #Aggiungi la parola alla lista dei nomi maiuscoli
            lista_nomi_maiuscoli.append(prima_parola[0])
        #Se la prima lettera della prima parola è un # allora viene comunque aggiunta
        if(prima_parola[0][0] == '#'):
            lista_nomi_maiuscoli.append(prima_parola)
 
        j = 0
        i = 1  
        #Per tutte le parole del testo:
        while i < len(text):
            #Se la parola è un nome e l'elemento prima di lei non è presente nella 'lista' allora:
            if(controllo_nome(text[i]) and text[i-1] not in lista):
                local = text[i] #Salvala su una variabile temporanea
                #Si controlla se la parola successiva è un nome maiuscolo
                for j in range(i+1, len(text)):    
                        if(controllo_nome(text[j])): #Se così fosse
                            local += " " + text[j] #Si concatenano tutti i nomi maiuscoli consecutivi
                        else: 
                            #Altrimenti la parola non è seguita da nomi maiuscoli
                            lista_nomi_maiuscoli.append(local) #Si effettua l'append nella lista
                            local = "" #Si pulisce la variabile temporanea
                            i = j #Si aggiorna l'indice del while
                            break
                if(local != ""): # Se local non è vuoto
                    lista_nomi_maiuscoli.append(local) # Aggiungilo alla lista dei nomi maiuscoli
                    local = "" # Pulisci local
                    i = j # Aggiorna l'indice
                    break # ultima istruzione del for  
            lista_nomi_maiuscoli.append(text[i]) # La parola non è un nome maiuscolo, viene aggiunta alla lista
            i+=1 #Ultima istruzione dello While, si aggiorna l'indice
        
        
        
        #Rimozione di tutti i nomi maiuscoli presenti dopo uno dei caratteri della lista 'da_controllare'
        i = 0
        a = False
        da_escludere = [":",".",",","-","\"", "\'", "“","”", ")", "(", "/", "«", "»", "&"]
        da_controllare = [".", "?","!", "\"", "\'", "“","”", "«", "»", "’"]

        #print(lista_nomi_maiuscoli)
        # Per tutte le parole dentro la lista
        while i < len(lista_nomi_maiuscoli):
          #Se la parola selezionata è nella lista da_controllare
          if(lista_nomi_maiuscoli[i] in da_controllare):
              try:
                  #Controllo la parola successiva e se questa è un nome maiuscolo, non si prende in considerazione
                  if(controllo_nome(lista_nomi_maiuscoli[i+1])):
                     a=True
                     i+=1
                  else:
                      i+=1
              except IndexError:
                  break;
          if(a):
              a= False
              i+=1
          else: #Altrimenti, se la parola non è nella lista da_controllare
              if(lista_nomi_maiuscoli[i] in da_escludere): #Si controlla se non è nella lista da_escludere
                 i+=1 # Si aggiorna l'indice dello while senza salvare la parola
              else:
                  #Altrimenti si salva la parola nella lista e si aggiorna l'indice
                  lista_nomi_parole.append(lista_nomi_maiuscoli[i])  
                  i+=1
              
        #Processo di rimozione delle stoprowds in lingua italiana.
        stops = set(stopwords.words("italian"))
        #Si controlla parola per parola e se questa è una stopwords viene eliminata
        lista_nomi_parole = [w for w in lista_nomi_parole if not w.lower() in stops]
    
        #Se la lista non è vuota
        if lista_nomi_parole:
            #Si aggiunge ogni parola nella lista dei nodi
            for parola in lista_nomi_parole:
                lista_nodi.append(parola)
            #Si ritorna la lista dei titoli con tutte le parole filtrate
            return lista_nomi_parole
    
        

# Lista che conterrà tutti gli archi del dataset
lista_archi_unita = []    
def genera_archi(text):
    #Se il testo non è vuoto e non ha lunghezza 1
    if(text != None and len(text) !=1):
        #Si accoppiano tutte le parole all'interno del titolo
        finale = []
        Pairs = []
        i = 0
        j = 0    
        for i in range(len(text) - 1):  
            for j in range(i , len(text) - 1):
                Pairs = [text[i], text[j + 1]]
                finale.append(Pairs)  
                lista_archi_unita.append(Pairs)
        return finale


#Si puliscono tutti i titoli all'interno del dataframe
df_g_f['title'] = df_g_f['title'].map(lambda x: pulisci_stringhe(x))

#Si generano tutti gli archi per il mese gennaio-febbraio
df_g_f['title'] = df_g_f['title'].map(lambda x: genera_archi(x))

#Viene creato il dataframe contenente la lista degli archi
df_lista_archi_g_f = pd.DataFrame(lista_archi_unita, columns =['Partenza','Arrivo'])

#Si contano le occorrenze di ogni arco all'interno del dataframe per definirne il peso
conta_g_f = df_lista_archi_g_f.groupby(['Partenza', 'Arrivo']).size() 

#Si salva la lista creata in formato CSV
conta_g_f.to_csv('lista_archi_g_f.csv', encoding='utf-8')

#
# Secondo Dataset. Mese: Marzo - Aprile
#

#Svuolo le liste contenenti informazioni del precedente dataset
lista_nodi = []
lista_archi_unita = []   

#Si effettuano le stesse operazioni svolte per il primo dataset
df_m_a['title'] = df_m_a['title'].map(lambda x: pulisci_stringhe(x))
df_m_a['title'] = df_m_a['title'].map(lambda x: genera_archi(x))
df_lista_archi_m_a = pd.DataFrame(lista_archi_unita, columns =['Partenza','Arrivo'])
conta_m_a = df_lista_archi_m_a.groupby(['Partenza', 'Arrivo']).size() 
conta_m_a.to_csv('lista_archi_m_a.csv', encoding='utf-8')

