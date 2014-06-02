#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append("/home/jonas/apps/pywikipedia/")

import wikipedia as wp
from urllib import quote
from time import sleep
from time import ctime
from random import randint
import os
import csv

head = u"\n\n== Wiki Loves Earth Brasil 2014 ==\n\n{| width='100%' cellpadding='0' cellspacing='0' style=' color:#A2B5CD; border:1px solid #A2B5CD; margin-top:0;'\n|-\n| style='width:100px;' |[[Image:WLE Austria Logo (no text).svg|100px|Wiki Loves Earth Logo]]\n|  style='text-align:center;' | <div style='background-color:;  border:solid 0px; font-size:180%; line-height:100%;  padding:10px;'><span style='color:#000000;'>'''''Wiki Loves  Earth'' Brasil 2014'''<br />Patrimônio  Natural</span></div>\n| style='width:600px; text-align:right;' |[[Image:Chapada_Diamantina_Panorama.jpg|x100px|Chapada Diamantina]]  [[Image:Jericoacoara_Ceará.jpg|x100px|]]  [[Image:Rio_de_Janeiro_from_Sugarloaf_mountain,_May_2004.jpg|x100px|]]\n|}\n\n"

msg = u'Oi, {0}:\n\nEstamos na reta final do concurso Wiki Loves Earth Brasil 2014! Você ainda poderá submeter mais fotos até o dia 31 de maio e ampliar suas chances na premiação de até R$2.500,00! Além da premiação em dinheiro, as melhores fotografias serão publicadas na edição de Agosto da revista impressa [http://fotografemelhor.com.br/ Fotografe Melhor] da Editora Europa.\n\nA comunidade Wikimedia Commons agradece a sua participação desde já, obrigado {1}, esse material será usado em vários dos nossos projetos. Acesse o site do [https://pt.wikipedia.org/wiki/Wikip%C3%A9dia:Wiki_Loves_Earth_2014/Brasil concurso] e submeta mais fotografias! Contribua também divulgando para seus amigos, contatos e curtindo nossa página no [https://www.facebook.com/wikilovesearthbrasil Facebook]\n\nEm breve anunciaremos novidades sobre os vencedores e a exposição das melhores fotografias do concurso.\n\nAtenciosamente,\n\nMovimento Wikimedia'

def loadCSV(filename):
        editors = {}
        f = open(filename, 'r')
        reader = csv.reader(f)
        for row in reader:
                editors[row[0]] = {'images': int(row[1])}
        f.close()
        return editors

def firstName(name):
        if len(name.split(' ')) > 1:
                name = name.split(' ')[0]
        return name.decode("utf-8")

def saveCSV(editors, remove, filename="nova_lista.csv"):
        f = open(filename, 'w')
        for r in remove:
                editors.pop(r)
        for editor in editors:
                f.write(editor + ", " + str(editors[editor]['images']) + "\n")
        f.close()
        

def invite(editors):
        s = wp.Site('', 'commons')
        remove = []
        try:
                for editor in editors:
                        p = wp.Page(s, "User talk:" + quote(editor))                                
                        pageContent = u''
                        try:
                                pageContent += p.get()
                        except:
                                pageContent += "{{Welcome}} - ~~~~"
                        pageContent += head
                        
                        if editors[editor]['images'] < 2:
                                pageContent += msg.format(firstName(editor), u"por enviar uma foto")
                        else:
                                pageContent += msg.format(firstName(editor), u"pelas {0} fotos envidas".format(editors[editor]['images']) )
                                
                        p.put(pageContent, u'Mensagem do Concurso WikiLoves Earth - [[pt:Wikipédia:Wiki_Loves_Earth_2014/Brasil|WLE Brasil]]')
                        sleepTime = randint(19, 40)
                        print(editor + "foi notificado, esperar " + str(sleepTime))
                        remove.append(editor)
                        sleep(sleepTime)
        except UnicodeDecodeError as e:
                for p in dir(e):
                        if not p.startswith('_'):
                                print '%s=%r' % (p, getattr(e, p))
        finally:
                saveCSV(editors, remove, "teste1.csv")
                        
editors = loadCSV(sys.argv[1])
invite(editors)
