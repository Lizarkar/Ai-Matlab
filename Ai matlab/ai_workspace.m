% File 1: Tao va luu du lieu vao file data.csv (5 diem ngau nhien)
x = rand(5, 1) * 10;
y = rand(5, 1) * 10;
data = [x, y];
writematrix(data, 'data.csv');

% File 2 (ve_do_thi.m): Doc du lieu tu data.csv va ve do thi
csvData = readmatrix('data.csv');
x_read = csvData(:, 1);
y_read = csvData(:, 2);

figure('Name', 'Do thi tu data.csv', 'NumberTitle', 'off');
plot(x_read, y_read, 'ro-', 'LineWidth', 2, 'MarkerSize', 8, 'MarkerFaceColor', 'r');
grid on; box on;
title('Do thi 5 diem ngau nhien tu file data.csv');
xlabel('Toa do X');
ylabel('Toa do Y');

for i = 1:length(x_read)
    text(x_read(i) + 0.15, y_read(i), sprintf('P%d (%.2f, %.2f)', i, x_read(i), y_read(i)), ...
        'FontSize', 10, 'FontWeight', 'bold');
end