from functions import *


print(num2char_transform(encoder_frase("Hola soy julian")))

print("date tu frase a decodificar")

frase = input()

print("tu frase es " + frase)

encode_frase = num2char_transform(encoder_frase(frase))

print(" y ahora es en código cesar como: " + encode_frase + "... ok voy a tratar de traducir!")


#julinnum = num2char_transform(encoder_frase("Hola soy julian y me gusta comprar cafe"))


print("Primero lo haré a fuerza bruta!")
#decone with brute force
print(decode_frase_unknown_fuerzaBruta(encode_frase))


print("Dame un momento le pregunto a google!")
#deconde with google traslate
print(decode_frase_unknown(encode_frase))

print("Ok ahora voy a pensar por mi mismo, no quiero que google me gane!")
#decone with ML
print(decode_frase_unknown_ml(encode_frase))

