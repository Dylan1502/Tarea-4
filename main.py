import numpy as np
from scipy import stats
from scipy import signal
from scipy import integrate
import matplotlib.pyplot as plt

A=[]
N = 0
f = 5000 #frecuencia#
Ts= T = 1/f #período de símbolo igual a un período completo de la onda portadora.

#Convertimos el csv en un vector de valores float ademas de calcular N que ya sabemos que es 10k

with open('bits10k.csv') as datos:
  linea = datos.read().splitlines()

  for row in linea:
    A.append(float(row))
    N +=1

# Número de puntos de muestreo por período
p = 50
# Puntos de muestreo para cada período
tp = np.linspace(0, T, p)
# Creación de la forma de onda de la portadora
sinus = np.sin(2*np.pi * f * tp) 

# Visualización de la forma de onda de la portadora

#plt.plot(tp, sinus)
#plt.xlabel('Tiempo / s')
#plt.show()

# Frecuencia de muestreo
fs = p/T # 250 kHz

# Creación de la línea temporal para toda la señal Tx
t = np.linspace(0, N*T, N*p)

# Inicializar el vector de la señal modulada Tx
senal = np.zeros(t.shape)

#################### Inciso 1 ########################

# Creación de la señal modulada  BPSK

for k,b in enumerate(A):
  if b==1:
    senal[k*p:(k+1)*p]= b * sinus
  else:
    senal[k*p:(k+1)*p]=  -sinus

# Visualización de los primeros bits modulados
#pb = 5
#plt.figure()
#plt.plot(senal[0:pb*p])
#plt.show()

################### Inciso 2 ######################

# Potencia instantánea
Pinst = senal**2

# Potencia promedio a partir de la potencia instantánea (W)
Ps = integrate.trapz(Pinst, t) / (N * T)
print(Ps)

################## Inciso 3 ############################

#Debido a que tenemos un rango, debemos simular 6 canales ruidosos, uno para cada valor del dB

# Relación señal-a-ruido deseada
SNR = -3
for SNR in range(-2, 4):
  print (SNR)
  # Potencia del ruido para SNR y potencia de la señal dadas
  Pn = Ps / (10**(SNR / 10))
  
  # Desviación estándar del ruido
  
  sigma = np.sqrt(Pn)
  
  # Crear ruido (Pn = sigma^2)
  
  ruido = np.random.normal(0, sigma, senal.shape)
  
  # Simular "el canal": señal recibida
  if SNR == -2:
    Rx1 = senal + ruido
    #print (Rx1)
  if SNR == -1:
    Rx2 = senal + ruido
    #print (Rx2)
  if SNR == 0:
    Rx3 = senal + ruido
    #print (Rx3)
  if SNR == 1:
    Rx4 = senal + ruido
    #print (Rx4)
  if SNR == 2:
    Rx5 = senal + ruido
    #print (Rx5)
  if SNR == 3:
    Rx6 = senal + ruido
    #print (Rx6)
  
  SNR +=1


# Visualización de los primeros bits recibidos
#pb = 5
#plt.figure()
#plt.plot(Rx2[0:pb*p])
#plt.show()

################### Inciso 4 ##############################

# Antes del canal ruidoso para todas es la misma dado que se usa sin ruido

#fw, PSD = signal.welch(senal, fs, nperseg=1024)
#plt.figure()
#plt.semilogy(fw, PSD)
#plt.xlabel('Frecuencia / Hz')
#plt.ylabel('Densidad espectral de potencia / V**2/Hz')
#plt.show()

# Después del canal ruidoso, esto se realizó para cada una de las Rx, pero para no poner el mismo codigo muchas veces se pone unicamente el de Rx1

#fw, PSD = signal.welch(Rx1, fs, nperseg=1024)
#plt.figure()
#plt.semilogy(fw, PSD)
#plt.xlabel('Frecuencia / Hz')
#plt.ylabel('Densidad espectral de potencia / V**2/Hz')
#plt.show()

#################### Inciso 5 ###################################
Af= np.array(A)


# Pseudo-energía de la onda original (esta es suma, no integral)
Es = np.sum(sinus**2)

# Inicialización del vector de bits recibidos
AfRx = np.zeros(Af.shape)

# Hacemos lo siguiente para cada valor de Rx

####### Para Rx1

# Decodificación de la señal por detección de energía
for k, b in enumerate(Af):
    Ep = np.sum(Rx1[k*p:(k+1)*p] * sinus)
    if Ep > Es/2:
        AfRx[k] = 1
    else:
        AfRx[k] = 0

err1 = np.sum(np.abs(Af - AfRx))
BER1 = err1/N

print('Hay un total de {} errores en {} bits para una tasa de error de {} para un SNR de -2dB.'.format(err1, N, BER1))

####### Para Rx2

# Decodificación de la señal por detección de energía
for k, b in enumerate(Af):
    Ep = np.sum(Rx2[k*p:(k+1)*p] * sinus)
    if Ep > Es/2:
        AfRx[k] = 1
    else:
        AfRx[k] = 0

err2 = np.sum(np.abs(Af - AfRx))
BER2 = err2/N

print('Hay un total de {} errores en {} bits para una tasa de error de {} para un SNR de -1dB.'.format(err2, N, BER2))

####### Para Rx3

# Decodificación de la señal por detección de energía
for k, b in enumerate(Af):
    Ep = np.sum(Rx3[k*p:(k+1)*p] * sinus)
    if Ep > Es/2:
        AfRx[k] = 1
    else:
        AfRx[k] = 0

err3 = np.sum(np.abs(Af - AfRx))
BER3 = err3/N

print('Hay un total de {} errores en {} bits para una tasa de error de {} para un SNR de 0dB.'.format(err3, N, BER3))

####### Para Rx4

# Decodificación de la señal por detección de energía
for k, b in enumerate(Af):
    Ep = np.sum(Rx4[k*p:(k+1)*p] * sinus)
    if Ep > Es/2:
        AfRx[k] = 1
    else:
        AfRx[k] = 0

err4 = np.sum(np.abs(Af - AfRx))
BER4 = err4/N

print('Hay un total de {} errores en {} bits para una tasa de error de {} para un SNR de 1 dB.'.format(err4, N, BER4))

####### Para Rx5

# Decodificación de la señal por detección de energía
for k, b in enumerate(Af):
    Ep = np.sum(Rx5[k*p:(k+1)*p] * sinus)
    if Ep > Es/2:
        AfRx[k] = 1
    else:
        AfRx[k] = 0

err5 = np.sum(np.abs(Af - AfRx))
BER5 = err5/N

print('Hay un total de {} errores en {} bits para una tasa de error de {} para un SNR de 2 dB.'.format(err5, N, BER5))

####### Para Rx6

# Decodificación de la señal por detección de energía
for k, b in enumerate(Af):
    Ep = np.sum(Rx6[k*p:(k+1)*p] * sinus)
    if Ep > Es/2:
        AfRx[k] = 1
    else:
        AfRx[k] = 0

err6 = np.sum(np.abs(Af - AfRx))
BER6 = err6/N

print('Hay un total de {} errores en {} bits para una tasa de error de {} para un SNR de 3 dB.'.format(err6, N, BER6))

#################### Inciso 6 ############################

BER=[BER1, BER2, BER3, BER4, BER5, BER6]
SNR=[-2, -1, 0, 1, 2, 3]

plt.plot(SNR,BER,'green')
plt.xlabel('Relación señal-a-ruido deseada (SNR)')
plt.ylabel('Bite error rate (BER)')
plt.show()