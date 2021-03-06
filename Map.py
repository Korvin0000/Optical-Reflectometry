import numpy as np
import pylab as pl
import glob
from scipy.ndimage.filters import gaussian_filter 


#%%
path = 'C:\\Users\\Nikolay\\Luna_exp\\12.05 (Fast Scan)\\Row\\'

path_Ampl = 'C:\\Users\\Nikolay\\Luna_exp\\12.05 (Fast Scan)\\Row\\Ampl\\'
path_Phase = 'C:\\Users\\Nikolay\\Luna_exp\\12.05 (Fast Scan)\\Row\\Phase\\'

Luna = glob.glob( path+'*.txt' ) #all files


#Fourier transformation
for j in Luna:
    
    print( j.split("Row\\")[1].split(".00")[0] )
    
    a = np.genfromtxt( j, dtype=float, unpack=True, usecols=[1], delimiter='', skip_header=14 ) #Reading
    
    Fourier = np.fft.fft( a )
    Ampl = abs( Fourier[1132500:1137000] )
    Phase = np.unwrap( np.angle(Fourier[1132500:1137000]) )
    
    np.savetxt( path_Ampl + j.split("Row\\")[1].split(".00")[0] + '.txt', Ampl, header = 'Amplitude of Fourier' )
    np.savetxt( path_Phase + j.split("Row\\")[1].split(".00")[0] + '.txt', Phase, header = 'Phase of Fourier' )
    
#     pl.plot(Ampl, markersize=2, label = j.split("Row\\1\\")[1].split(".00")[0] )
    
# pl.grid()
# pl.legend()
# pl.show()
#%%

path_Ampl = 'C:\\Users\\Nikolay\\Luna_exp\\12.05 (Fast Scan)\\Row\\Ampl\\'
path_Phase = 'C:\\Users\\Nikolay\\Luna_exp\\12.05 (Fast Scan)\\Row\\Phase\\'


Ampl_ = glob.glob( path_Ampl + '*.txt' )

#Sorting
Ampl_sort = np.array([])
for i in Ampl_:
    Ampl_sort = np.append(Ampl_sort,i.split( "Ampl\\")[1].split(".txt")[0] )
    
Ampl_sort = sorted( Ampl_sort, key=int )
# print(Ampl_sort)

#map
Final_Ampl = np.zeros((61, 4500))
Final_Phase = np.zeros((61, 4500))
Blurred = np.zeros((61,4500))

max_1 = np.array([])
max_2 = np.array([])
max_1_ph = np.array([])
max_2_ph = np.array([])
N_2 = np.array([])
N_1 = np.array([])


for i in range(Final_Ampl.shape[0]):
    # print(i,Ampl_sort[i])
    Final_Ampl[i] = np.genfromtxt( path_Ampl + Ampl_sort[i] + '.txt', dtype = 'f8'  , unpack=True, usecols=[0], delimiter='', skip_header = 1 )
    Blurred[i] = gaussian_filter( Final_Ampl[i], sigma=20 )
    Blurred[i] = 10*np.log10( Blurred[i] )
    
    Final_Phase[i] = np.genfromtxt( path_Phase + Ampl_sort[i] + '.txt', dtype = 'f8', unpack=True, usecols=[0], delimiter='', skip_header = 1 )
    
    # print(np.size(Final_Ampl[i]))
    if i == 0:
        max_1 = np.append( max_1, np.max(Blurred[i][180:510]) )
        max_2 = np.append( max_2, np.max(Blurred[i][2966:3300]) )
      
        N_1 = np.append( N_1, np.where( Blurred[i][180:510] == np.max(Blurred[i][180:510]))[0][0] + 180) 
        N_2 = np.append( N_2, np.where( Blurred[i][2966:3300] == np.max(Blurred[i][2966:3300]))[0][0] + 2966)
        
    else:
        
        max_1 = np.append( max_1, np.max(Blurred[i][int(N_1[i-1]-130):int(N_1[i-1]+130)]) )
        N_1 = np.append( N_1, np.where( Blurred[i][int(N_1[i-1]-130):int(N_1[i-1]+130)] == np.max(Blurred[i][int(N_1[i-1]-130):int(N_1[i-1]+130)]))[0][0] + int(N_1[i-1]-130))
        
        max_2 = np.append( max_2, np.max(Blurred[i][int(N_2[i-1]-130):int(N_2[i-1]+130)]) )
        N_2 = np.append( N_2, np.where( Blurred[i][int(N_2[i-1]-130):int(N_2[i-1]+130)] == np.max(Blurred[i][int(N_2[i-1]-130):int(N_2[i-1]+130)]))[0][0] + int(N_2[i-1]-130))        
    # print(int(N_2[i]))
    
    Final_Phase[i] = gaussian_filter( Final_Phase[i], sigma=25 )
    max_1_ph = np.append(max_1_ph,  Final_Phase[i][int(N_1[i])])
    max_2_ph = np.append(max_2_ph,  Final_Phase[i][int(N_2[i])])
    
    print('T = ', Ampl_sort[i], '; Maximum of Ampl = ', max_2[i], '; Position = ', int(N_2[i]))


pl.figure('Map with Gaussian filter (log scale)')
pl.imshow(Blurred,
          cmap = 'nipy_spectral',
          interpolation = "Gaussian",
          label = "Reflectogramms",
          extent = (0, 4500,
                    60, -60))
pl.colorbar()
pl.xlabel('Length (arb. un.)', fontsize = 15)
pl.ylabel('Temperature (C)', fontsize = 15)
pl.axis('auto')

#%%

pl.figure('Splices for different T')
#Gap
# pl.plot(Blurred[6], label = Ampl_sort[6], linewidth = 3)
# pl.plot(Blurred[7], label = Ampl_sort[7], linewidth = 3)
# pl.plot(Blurred[8], label = Ampl_sort[8], linewidth = 3)
# pl.plot(Blurred[9], label = Ampl_sort[9], linewidth = 3)

#Reference
pl.plot(Blurred[0], label = Ampl_sort[0], linewidth = 3)
pl.plot(Blurred[15], label = Ampl_sort[15], linewidth = 3)
pl.plot(Blurred[30], label = Ampl_sort[30], linewidth = 3)
pl.plot(Blurred[45], label = Ampl_sort[42], linewidth = 3)
pl.plot(Blurred[60], label = Ampl_sort[60], linewidth = 3)

pl.xlabel('Length (arb. un.)', fontsize = 20)
pl.ylabel('Amlitude (dB)', fontsize = 20)
pl.legend(fontsize = 20)
pl.grid()
pl.show()
pl.tight_layout()


fig, ax1 = pl.subplots()

ax1.set_xlabel('Temperature (C)', fontsize = 20)
ax1.set_ylabel('Phase (arb. un.)', fontsize = 20)
ax1.plot(np.arange(-60,62,2), max_1_ph,'-o',label = 'Phase_Begining', color = 'red', linewidth = 3)
ax1.plot(np.arange(-60,62,2), max_2_ph,'-o',label = 'Phase_End', color = 'green', linewidth = 3)
ax1.tick_params(axis ='y')
pl.grid()
pl.legend(loc='lower right', fontsize = 20)

ax2 = ax1.twinx()

color = 'tab:green'
ax2.set_ylabel('Amplitude (dB)', fontsize = 20)
ax2.plot( np.arange(-60,62,2), max_1, '-o', label = 'Ampl_Begining', color='blue', linewidth = 3 )
ax2.plot( np.arange(-60,62,2), max_2, '-o', label = 'Ampl_End', color='brown', linewidth = 3 )

ax2.tick_params(axis ='y')
pl.legend(fontsize = 20)
pl.show()
pl.grid()
pl.title ("Phase and Amplitude corresponding to the peaks", fontsize = 20)

pl.figure('Position of the peaks (T)')
pl.plot(np.arange(-60,62,2), N_1, "o-", label = 'Begining')
pl.plot(np.arange(-60,62,2), N_2, "o-", label = 'End')
pl.xlabel('T (C)', fontsize = 20)
pl.ylabel('N (arb. un.)', fontsize = 20)
pl.legend(fontsize = 20)
pl.grid()
pl.show()
pl.tight_layout()





# pl.figure('Ampl of the peaks(T)')
# pl.plot(np.arange(-60,62,2), max_1, label = 'Begining')
# pl.plot(np.arange(-60,62,2), max_2, label = 'End')
# pl.xlabel('T (C)', fontsize = 20)
# pl.ylabel('Amlitude (dB)', fontsize = 20)
# pl.legend(fontsize = 20)
# pl.grid()
# pl.show()
# pl.tight_layout()







