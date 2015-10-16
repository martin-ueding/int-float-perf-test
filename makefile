efficiency.pdf: data-int.txt analysis.py
	python3 analysis.py data*.txt

data-int.txt: int-float-perf
	./$<

int-float-perf: int-float-perf.cpp
	clang++ -std=c++11 -O3 -march=native $< -o $@ -pthread
