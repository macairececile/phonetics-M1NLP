#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 19:05:57 2019

@author: Cécile Macaire et Ludivine Robert
"""

# Librairies
import nltk

# Variables globales
ortho_c = ["p", "t", "k", "b", "d", "g", "f", "s", "c", "v", "z", "g", "j", "m", "n", "r", "l", "h"]
ortho_v = ["a", "e", "i", "o", "u", "y", "é", "ê", "ë", "ï", "à", "ù"]
stop_V = ["b", "d", "g"]
stop_U = ["p", "t", "k"]
fric_V = ["v", "z", "Z"]
fric_U = ["f", "s", "S"]
liquids = ["R", "l"]
nasals = ["m", "n", "N", "G"]
semi_vowels = ["w", "j", "8"]
vowels_O = ["a", "e", "i", "u", "o", "y", "E", "9", "2", "O", "*"]
vowels_N = ["@", "1", "5"]

v = ['aa', 'ee', 'ii', 'oo', 'uu', 'yy', 'EE', '99', '22', 'OO', '**', '@@', '11', '55']

syl_cons = stop_V + stop_U + fric_V + fric_U + nasals
syl_vow = vowels_N + vowels_O


def open_input(path):
    """Ouvrir et lire le contenu du fichier input"""
    input_file = open(path, "r", encoding='utf-8-sig')
    words = []
    transcriptions = []
    for lines in input_file:
        tmp = lines.split()
        words.append(tmp[0])
        transcriptions.append(tmp[1])
    return words, transcriptions


def ortho_VC(l):
    """Conversion en forme VC de la forme orthographique"""
    words_VC = []
    for word in l:
        word_VC = ''
        for letter in word:
            if letter in ortho_c:
                word_VC += 'C'
            else:
                word_VC += 'V'
        words_VC.append(word_VC)
    return words_VC


def phon_VC(l):
    """Conversion en forme VC de la forme phonétique"""
    trans_VC = []
    for word in l:
        word_VC = ''
        for letter in word:
            if letter in vowels_O:
                word_VC += 'V'
            elif letter in vowels_N:
                word_VC += 'V'
            else:
                word_VC += 'C'
        trans_VC.append(word_VC)
    return trans_VC


def syll_VC(l):
    """Conversion en forme VC de la forme syllabique"""
    syll_VC = []
    for word in l:
        word_VC = ''
        for letter in word:
            if letter in vowels_O:
                word_VC += 'V'
            elif letter in vowels_N:
                word_VC += 'V'
            elif letter == '-':
                word_VC += '-'
            else:
                word_VC += 'C'
        syll_VC.append(word_VC)
    return syll_VC


def cut_syll(l):
    """Extraction de chaque syllabe"""
    cut = [a.split('-') for a in l]
    return [x for z in cut for x in z if x]


def freq_VC(l):
    """Fréquence avec la librairie nltk"""
    frequency = nltk.FreqDist(l)
    return frequency.most_common(15)


def freq_label(l):
    """Fréquence de chaque label"""
    freq_label = []
    for i in l:
        string = ''
        for j in i[0]:
            for k in j:
                if k in stop_V:
                    string += 'stopV'
                elif k in stop_U:
                    string += 'stopU'
                elif k in liquids:
                    string += 'liquids'
                elif k in nasals:
                    string += 'nasals'
                elif k in semi_vowels:
                    string += 'semiVowels'
                elif k in fric_U:
                    string += 'fricU'
                elif k in fric_V:
                    string += 'fricV'
                elif k in vowels_O:
                    string += 'vowelsO'
                elif k in vowels_N:
                    string += 'vowelsN'
        a = (string, i[1])
        freq_label.append(a)
    return freq_label


def merge(l):
    """Création de la fréquence finale des labels"""
    labels = []
    labels_num = []
    for i in l:
        if i[0] not in labels:
            labels.append(i[0])
            labels_num.append(i[1])
        else:
            for k, l in enumerate(labels):
                if l == i[0]:
                    labels_num[k] += i[1]
    l_final = list(zip(labels, labels_num))
    return sorted(l_final, key=lambda x: x[1])


def syllabification(l):
    """Syllabification de la forme phonétique"""
    syllab = []
    for word in l:
        string = ''
        i = 0
        is_add2 = False
        is_add3 = False
        cpt = 0
        for p in word:
            if p in syl_vow:
                cpt += 1
        if cpt == 1:
            string += word
            is_add2 = True
        if not is_add2 and all(a in (syl_cons + liquids + semi_vowels) for a in word[:-1]):
            if word[-1] in syl_vow:
                string += word
                is_add3 = True
        if not is_add3 and not is_add2:
            while i < len(word):
                is_add = False
                if i == 0 and word[i] in (syl_cons + liquids + semi_vowels):
                    if word[i + 1] in (syl_cons + liquids + semi_vowels):
                        string += word[i] + word[i + 1]
                        is_add = True
                        i += 2
                    else:
                        string += word[i]
                        is_add = True
                        i += 1
                if i == 0 and i + 1 < len(word):
                    if word[i] in syl_vow and word[i + 1] in syl_vow:
                        string += word[i] + '-' + word[i + 1]
                        is_add = True
                        i += 1
                if i + 1 < len(word):
                    if word[i] in syl_vow and word[i + 1] in syl_vow:
                        string += word[i] + '-' + word[i + 1]
                        is_add = True
                        i += 1
                if not is_add and i + 5 < len(word):
                    if (word[i] and word[i + 5]) in syl_vow and word[i + 1] not in (syl_vow) and \
                            word[i + 2] not in (syl_vow) and word[i + 3] not in (
                            syl_vow) and word[i + 4] not in (syl_vow):
                        string += word[i] + word[i + 1] + '-' + word[i + 2] + word[i + 3] + word[i + 4] + word[i + 5]
                        is_add = True
                        i += 5
                if not is_add and i + 4 < len(word):
                    if (word[i] and word[i + 4]) in syl_vow:
                        if word[i + 1] not in (syl_vow + liquids + semi_vowels) and word[i + 2] in liquids and word[
                            i + 3] in semi_vowels:
                            string += word[i] + '-' + word[i + 1] + word[i + 2] + word[i + 3] + word[i + 4]
                            is_add = True
                            i += 4
                        elif word[i + 1] not in syl_vow and word[i + 2] not in syl_vow and word[i + 3] not in syl_vow:
                            string += word[i] + word[i + 1] + '-' + word[i + 2] + word[i + 3] + word[i + 4]
                            is_add = True
                            i += 4
                if not is_add and i + 3 < len(word):
                    if (word[i] and word[i + 3]) in syl_vow:
                        if word[i + 1] in nasals and word[i + 2] in (liquids + semi_vowels):
                            string += word[i] + word[i + 1] + '-' + word[i + 2] + word[i + 3]
                            is_add = True
                            i += 3
                        elif word[i + 1] not in (syl_vow + liquids + semi_vowels) and word[i + 2] in (
                                liquids + semi_vowels):
                            string += word[i] + '-' + word[i + 1] + word[i + 2] + word[i + 3]
                            is_add = True
                            i += 3
                        elif (word[i + 1] and word[i + 2]) in liquids or (
                                word[i + 1] in liquids and word[i + 2] not in (
                                syl_vow + liquids + semi_vowels)) or (
                                word[i + 1] in semi_vowels and word[i + 1] not in syl_vow) or (
                                (word[i + 1] and word[i + 2]) not in (syl_vow + liquids + semi_vowels)):
                            string += word[i] + word[i + 1] + '-' + word[i + 2] + word[i + 3]
                            is_add = True
                            i += 3
                        elif word[i + 1] in liquids and word[i + 2] in semi_vowels:
                            string += word[i] + '-' + word[i + 1] + word[i + 2] + word[i + 3]
                            is_add = True
                            i += 3
                if not is_add and i + 2 < len(word):
                    if word[i] in syl_vow and word[i + 1] not in syl_vow and word[i + 2] in syl_vow:
                        string += word[i] + '-' + word[i + 1] + word[i + 2]
                        is_add = True
                        i += 2
                if not is_add and i + 1 < len(word):
                    if word[i] in syl_vow and word[i + 1] in syl_vow:
                        string += word[i] + '-' + word[i + 1]
                        is_add = True
                        i += 2
                if not is_add and len(word) - (i + 1) == 0 and word[i - 1] in syl_vow:
                    string += word[i - 1] + word[i]
                    i += 1
                    is_add = True
                if not is_add and len(word) - (i + 1) == 0 and word[i] in (syl_cons + liquids + nasals) and word[
                    i - 1] in (syl_cons + liquids + nasals) and word[i - 2] in (syl_cons + liquids + nasals) and word[
                    i - 3] in syl_vow:
                    string += word[i - 2] + word[i - 1] + word[i]
                    i += 1
                    is_add = True
                if not is_add and len(word) - (i + 1) == 0 and word[i] in (syl_cons + liquids + nasals) and word[
                    i - 1] in (syl_cons + liquids + nasals) and word[i - 2] in syl_vow:
                    string += word[i - 1] + word[i]
                    i += 1
                    is_add = True
                if not is_add:
                    i += 1
            for i in v:
                if i in string:
                    string = string.replace(i, i[0])
        syllab.append(string)
    return syllab


if __name__ == "__main__":
    words, transcriptions = open_input("Input_File.txt")  # lecture fichier input
    words_VC = ortho_VC(words)
    trans_VC = phon_VC(transcriptions)
    trans_syll = syllabification(transcriptions)
    trans_syll_VC = syll_VC(trans_syll)
    # print(words)
    # print(transcriptions)
    # print(words_VC)
    # print(trans_VC)

    # print(trans_syll)
    # print(trans_syll_VC)

    # Ecriture de fichier output avec les formes précédemment générées
    with open('Output_File.txt', 'w') as file:
        for i, j in enumerate(words):
            file.write(
                words[i] + ' ' + words_VC[i] + ' ' + transcriptions[i] + ' ' + trans_VC[i] + ' ' + trans_syll[i] + ' ' +
                trans_syll_VC[i] + '\n')
        file.close()

    # Fréquences
    cut_syll_VC = cut_syll(trans_syll_VC)
    cut_cons_vow = cut_syll(trans_syll)
    frequence_1 = freq_VC(cut_syll_VC)
    frequence_3 = freq_VC(cut_cons_vow)
    frequence_2 = freq_label(frequence_3)
    print(frequence_1)
    print(frequence_3)
    print(frequence_2)
    print(merge(frequence_2))
