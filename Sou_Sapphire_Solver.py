import numpy as np
import matplotlib.pyplot as plt
from functools import lru_cache

'''

All the differential equations were solved by hand.
It took a while.

-Souhail

'''

# af''+bf'+cf=0
def DIFF_SOLVE(a,b,c,y0,derivative=False):
    tauBC = b/c
    tauBA = b/a
    tau = tauBC*tauBA - 4
    omega2 = c/a
    if tau > 0:
        #print('TAU - 1')
        r1 = omega2*(-b+np.sqrt(tau/c))
        r2 = omega2*(-b-np.sqrt(tau/c))
        if not derivative:
            return lambda t: y0*((r2*(np.exp(r1*t)-np.exp(r2*t))/(r2-r1))+np.exp(r2*t))
        else:
            return lambda t: y0*((r2*(r1*np.exp(r1*t)-r2*np.exp(r2*t))/(r2-r1))+r2*np.exp(r2*t))
    elif tau < 0:
        #print('TAU - 2')
        aph = -b*omega2
        bet = omega2*np.sqrt(-tau/c)
        if not derivative:
            return lambda t: y0*np.exp(aph*t)*(np.cos(bet*t)-(aph/bet)*np.sin(bet*t))
        else:
            return lambda t: -aph*y0*np.exp(aph*t)*np.sin(bet*t)*((aph/bet)+(bet/aph))
    else:
        #print('TAU - 0')
        r0 = -b*omega2
        if not derivative:
            return lambda t: y0*(1-t*r0)*np.exp(r0*t)
        else:
            return lambda t: -y0*r0*r0*np.exp(r0*t)

def EXTREMAS(arr):
    sign = np.sign(np.diff(arr))
    sign_d = np.where(np.diff(sign)!=0)[0] + 1

    #boundary check
    if sign[0] == -1:
        sign_d = np.concatenate(([0],sign_d))
    if sign[-1] == 1:
        sign_d = np.concatenate((sign_d,[len(arr)-1]))

    #the main deal
    maxima = np.zeros_like(arr,dtype=bool)
    minima = np.zeros_like(arr,dtype=bool)
    for i in sign_d:
        try:
            if sign[i-1] == 1 and sign[i] == -1:
                maxima[i] = True
            elif sign[i-1] == -1 and sign[i] == 1:
                minima[i] = True
        except IndexError:
            pass

    return np.where(maxima)[0], np.where(minima)[0]

'''
ay''+by'+cy=g(t)
with g(t)=Asin(w*t+phi)
'''

def LAPLACE_SOLVE(a,b,c,y0,A,w,phi,derivative=False):
    delta = b*b-4*a*c
    sgn = np.sign(delta)

    cphi = np.cos(phi)
    sphi = np.sin(phi)

    if sgn == 1:
        r1 = (-b+np.sqrt(delta))/(2*a)
        r2 = (-b-np.sqrt(delta))/(2*a)

        B = A*r1*sphi+A*w*cphi
        B /= a*(r1-r2)*(r1*r1+w*w)
        C = A*r2*sphi+A*w*cphi
        C /= a*(r2-r1)*(r2*r2+w*w)
        D = A*np.exp(phi*1j)
        E = D - 2*A*cphi
        D /= 2*a*1j*(r1-w*1j)*(r2-w*1j)
        E /= 2*a*1j*(r1+w*1j)*(r2+w*1j)
        F = (a*r1*y0+b*y0)/(a*(r1-r2))
        G = (a*r2*y0+b*y0)/(a*(r2-r1))
        
        #y(t)=
        if not derivative:
            return lambda t: (B+F)*np.exp(r1*t)+(C+G)*np.exp(r2*t)+(D*np.exp(w*t*1j)+E*np.exp(-w*t*1j))*np.sin(w*t)
        #y'(t)=
        else:
            return lambda t: (B+F)*r1*np.exp(r1*t)+(C+G)*r2*np.exp(r2*t)+w*np.sin(w*t)*(D*(1+1j)*np.exp(w*t*1j)+E*(1-1j)*np.exp(-w*t*1j))
        
    elif sgn == 0:
        r = -b/(2*a)

        B = -r*r*sphi-2*r*w*cphi+w*w*sphi
        B *= (A/(a*((r*r+w*w)**2)))
        C = r*sphi+w*cphi
        C *= (A/(a*(r*r+w*w)))
        D = A*np.exp(phi*1j)
        E = D - 2*A*cphi
        D /= 2*a*1j*((r-w*1j)**2)
        E /= 2*a*1j*((r+w*1j)**2)
        F = y0
        G = (r+(b/a))*y0

        #y(t)=
        if not derivative:
            return lambda t: (B+F+C*t+G*t)*np.exp(r*t)+np.sin(w*t)*(D*np.exp(w*t*1j)+E*np.exp(-w*t*1j))
        #y'(t)=
        else:
            return lambda t: (B+F+C+G)*np.exp(r*t)+(C+G)*t*r*np.exp(r*t)+w*np.sin(w*t)*(D*(1+1j)*np.exp(w*t*1j)+E*(1-1j)*np.exp(-w*t*1j))

    elif sgn == -1:
        aph = -b/(2*a)
        bet = np.sqrt(-delta)/(2*a)
        r1 = aph + bet*1j
        r2 = aph - bet*1j

        B = A*(r1)*sphi+A*w*cphi
        C = A*(r2)*sphi+A*w*cphi
        B /= 2*a*1j*bet*(((r1)**2)+w*w)
        C /= -2*a*1j*bet*(((r2)**2)+w*w)
        D = A*np.exp(phi*1j)
        E = D - 2*A*cphi
        D /= 2*a*1j*(((aph-w*1j)**2)+bet*bet)
        E /= 2*a*1j*(((aph+w*1j)**2)+bet*bet)
        F = a*r1*y0+b*y0
        G = a*r2*y0+b*y0
        F /= 2*a*bet*1j
        G /= 2*a*bet*1j

        #y(t)=
        if not derivative:
            return lambda t: (B+F)*np.exp(t*r1)+(C+G)*np.exp(t*r2)+D*np.exp(w*t*1j)+E*np.exp(-w*t*1j)
        #y'(t)=
        else:
            return lambda t: r1*(B+F)*np.exp(t*r1)+r2*(C+G)*np.exp(t*r2)+1j*w*(D*np.exp(w*t*1j)-E*np.exp(-w*t*1j))

@lru_cache
def LAPLACE_SOLVE_MECH(m,h,k,x0,v0,derivative=False):
    delta = h*h-4*m*k
    sgn = np.sign(delta)

    if sgn == 1:
        r1 = (-h+np.sqrt(delta))/(2*m)
        r2 = (-h-np.sqrt(delta))/(2*m)

        A = (m*r1*x0+m*v0+h*x0)/(m*(r1-r2))
        B = (m*r2*x0+m*v0+h*x0)/(m*(r2-r1))

        if not derivative:
            return lambda t: A*np.exp(r1*t)+B*np.exp(r2*t)
        else:
            return lambda t: r1*A*np.exp(r1*t)+r2*B*np.exp(r2*t)
        
    elif sgn == -1:
        aph = -h/(2*m)
        bet = np.sqrt(-delta)/(2*m)
        r1 = aph+bet*1j
        r2 = aph-bet*1j
        A = (m*r1*x0+m*v0+h*x0)/(m*(r1-r2))
        B = (m*r2*x0+m*v0+h*x0)/(m*(r2-r1))

        if not derivative:
            return lambda t: A*np.exp(r1*t)+B*np.exp(r2*t)
        else:
            return lambda t: r1*A*np.exp(r1*t)+r2*B*np.exp(r2*t)
        
    else:
        r = -h/(2*m)

        B = (m*r*x0+m*v0+h*v0)/m

        if not derivative:
            return lambda t: np.exp(r*t)*(x0+B*t)
        else:
            return lambda t: np.exp(r*t)*(x0+B+B*r*t)

def tickUnit(data, unit):
    abs_data = np.abs(data)
    scale_factors = [(1e24, 'Y'), (1e21, 'Z'), (1e18, 'E'),(1e15,'P'),
                     (1e12, 'T'), (1e9, 'G'), (1e6, 'M'),(1e3, 'k'),
                     (1, ''), (1e-3, 'm'),(1e-6, 'μ'), (1e-9, 'n'),
                     (1e-12, 'p'),(1e-15,'f'),(1e-18,'a'),
                     (1e-21,'z'),(1e-24,'y')]
    for factor, prefix in scale_factors:
        if np.max(abs_data) >= factor:
            return f'{{:.1e}} {prefix}{unit}{{}}{{}}'
    return f'{{:.{int(-np.log10(abs_data.min()))+1}f}} {unit}{{}}{{}}'
  
if __name__ == '__main__':
    TIME = np.linspace(0,100,400)
    a = 1
    b = 1
    c = 1
    y0 = 10
    A = 10
    w = 1
    phi = 0
    func = LAPLACE_SOLVE(a,b,c,y0,A,w,phi)
    values = np.round(func(TIME),2)

    plt.plot(TIME,A*np.sin(w*TIME+phi),label='Générateur',color='green')
    plt.plot(TIME,values,label='Partie Réelle (Observée)')
    plt.plot(TIME,-1j*values, color='red',label='Partie Imaginaire')
    plt.grid()
    plt.legend()
    plt.show()
    '''TAU_2 = DIFF_SOLVE(1,1,1,1)
    TAU_1 = DIFF_SOLVE(0.25,1,0.25,1)
    TAU_0 = DIFF_SOLVE(0.25,1,1,1)
    print('TAU - 2')
    for t in TIME:
        print('TIME:',np.round(t,2),'VALUE:',np.round(TAU_2(t),2))
    print('TAU - 1')
    for t in TIME:
        print('TIME:',np.round(t,2),'VALUE:',np.round(TAU_1(t),2))
    print('TAU - 0')
    for t in TIME:
        print('TIME:',np.round(t,2),'VALUE:',np.round(TAU_0(t),2))'''
