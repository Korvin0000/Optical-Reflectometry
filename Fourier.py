import numpy as np
import pylab as pl
import glob


path = 'C:\\Users\\Nikolay\\Luna_exp\\12.05 (Fast Scan)\\Row\\'

path_Ampl = 'C:\\Users\\Nikolay\\Luna_exp\\12.05 (Fast Scan)\\Row\\Ampl\\'
path_Phase = 'C:\\Users\\Nikolay\\Luna_exp\\12.05 (Fast Scan)\\Row\\Phase\\'

Luna = glob.glob( path+'*.txt' )
# print(Luna)

for j in Luna:
    
    print( j.split("Row\\")[1].split(".00")[0] )
    
    a = np.genfromtxt( j, dtype=float, unpack=True, usecols=[1], delimiter='', skip_header=14 )
    
    Fourier = np.fft.fft( a )
    Ampl = abs( Fourier[1132500:1137000] )
    Phase = np.unwrap( np.angle(Fourier[1132500:1137000]) )
    
    np.savetxt( path_Ampl + j.split("Row\\")[1].split(".00")[0] + '.txt', Ampl, header = 'Amplitude of Fourier' )
    np.savetxt( path_Phase + j.split("Row\\")[1].split(".00")[0] + '.txt', Phase, header = 'Phase of Fourier' )
    
    # pl.plot(Ampl, markersize=2, label = j.split("Row\\1\\")[1].split(".00")[0] )
# pl.grid()
# pl.legend()
# pl.show()

# path_new = 'C:\\Users\\Nikolay\\Luna_exp\\12.05 (Fast Scan)\\1\\'
# Luna_1 = glob.glob( path_new+'*.txt' )
# print(Luna_1)

# for j in Luna_1:
    
#     print( j.split("1\\")[1].split(".00")[0] )
    
#     a = np.genfromtxt( j, dtype=float, unpack=True, usecols=[1], delimiter='', skip_header=14 )

#     pl.plot(a, markersize=2, label = j.split("1\\")[1].split(".00")[0] )