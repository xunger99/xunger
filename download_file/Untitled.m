Fs=48000;
t=0:Fs:10;

y1000=sin(2*pi*Fs*t);
audiowrite('1kHz.wav',y1000,Fs);

y5000=sin(2*pi*Fs*t);
audiowrite('5kHz.wav',y1000,Fs);