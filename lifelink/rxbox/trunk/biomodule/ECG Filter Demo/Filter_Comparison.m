load output.txt % load CSV file
subplot(2,1,1)
plot(output(250:3000)) % initial ECG waveform
fs = 500; % sampling frequency
f = 35; % cutoff frequency
n = 10; % filter order

[b,a] = butter(n,f/fs); % extracting filter coefficients
filtered = filter(b,a,output); % filtering the data from CSV file
subplot(2,1,2)
plot(filtered(250:3000)) % filtered ECG waveform

save('-text',"octave_output.txt","filtered"); % save filtered data to a text file