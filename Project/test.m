b = [0.3984375, 0.456];
a = [1, 0.343];

nfft = 4;
h = fft(b, 2*nfft);
h = h(1:nfft);

for i = 1:nfft
    fprintf('%f%fj ', real(h(i)), imag(h(i)));
end

fprintf('\n');

for i = 1:nfft
    fprintf('%f ', sqrt(real(h(i))*real(h(i)) + imag(h(i))*imag(h(i))));
end

z = freqz(b, a);
for i = 1:z
    z(i)=sqrt(real(z(i))*real(z(i)) + imag(z(i))*imag(z(i)));
end
figure; plot(z)