#! /usr/bin/python
# -*- coding: iso-8859-1 -*-

# Criado em: "01/11/2009"
# Autor: MRSantos mrsantos.caxias@gmail.com
#
# A espera não é uma esperaça vazia,
# possui a certeza interior de alcançar seu objetivo...

from random import choice

def gera_senha(tamanho):
        caracters = '0123456789abcdefghijlmnopqrstuwvxz'
        senha = ''
        for char in xrange(tamanho):
                senha += choice(caracters)
        return  senha

print gera_senha(10)
