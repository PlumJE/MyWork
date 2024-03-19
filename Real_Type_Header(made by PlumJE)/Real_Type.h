#pragma once
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdbool.h>
#include <math.h>

typedef struct real {
	long long frac : 52;// 가수 부분
	int exp : 11;		// 지수 부분
} Real;

// Real의 생성자. 시간은 O(2n)
Real newReal(char* f) {
	// 유효숫자의 시작점, 끝점, 소수점의 위치를 찾는다!
	int frac_start = -1, frac_end = -1, point = -1;
	size_t f_len = strlen(f);

	bool trigger = false;
	for (int i = 0; i < f_len; i++) {
		if ('1' <= f[i] && f[i] <= '9') {
			if (trigger == false) {
				frac_start = i;
				trigger = true;
			}
			frac_end = i;
		}
		else if (f[i] == '.') {
			point = i;
		}
	}

	// frac_start == frac_end == -1이라면 0.0과 같은 값이므로, 0.0을 리턴한다
	if (frac_start == -1 && frac_end == -1) {
		Real result = { 0, 0 };
		return result;
	}

	// point == -1이라면 소수점이 없다는 뜻으로, f를 정수삼아 리턴한다
	if (point == -1) {
		Real result = { atoi(f), 0 };
		return result;
	}

	// 유효숫자만 추출해 frac에 저장한다! 당연히 부호도 저장
	int frac = f[frac_start] - '0';
	for (int i = frac_start + 1; i <= frac_end; i++) {
		if (i != point) {
			frac *= 10;
			frac += f[i] - '0';
		}
	}
	if (f[0] == '-') {
		frac *= -1;
	}

	// 유효숫자 끝 위치와 소수점 위치를 고려해 exp값을 구한다!
	int exp;
	if (point > frac_end) {
		exp = point - frac_end - 1;
	}
	else {
		exp = point - frac_end;
	}

	Real result = { frac, exp };
	return result;
}

// Real의 값을 문자열형 실수로 리턴. 시간은 O(n)
char* realToString(Real r) {
	// r이 0.0과 같으면 그냥 "0.0"을 리턴한다
	if (r.frac == 0 && r.exp == 0) {
		return "0.0";
	}

	// result에 frac의 값을 문자열 형식으로 붙여넣는다
	char* result = malloc(0);
	sprintf(result, "%d", r.frac);
	
	// result뒤에 "...000.0"을 붙일 때
	if (r.exp > -1) {
		for (int i = 0; i < r.exp; i++)
			strcat(result, "0");
		strcat(result, ".0");
	}
	// result사이에 "0.000..." 또는 "."을 삽입할 때
	else {
		int index = strlen(result) + r.exp;
		int zeros = -index;
		int is_neg = result[0] == '-' ? 1 : 0;	// 음의 부호가 붙으면 1, 아니면 0이다.
		char *middle = malloc(0);
		char *back = malloc(0);

		// index가 0/1보다 작다면 0/1로 만들고, result[index~]부분을 back에 백업한다
		if (index < is_neg)
			index = is_neg;
		strcpy(back, result + index);

		// zeros가 면 middle="."이고, 면 middle="0."+"0"*zeros이다
		if (zeros < -is_neg) {
			strcpy(middle, ".");
		}
		else {
			strcpy(middle, "0.");
			for (int i = 0; i < zeros; i++)
				strcat(middle, "0");
		}

		// result[index]에 middle을 삽입한다
		result[index] = '\0';
		strcat(result, middle);
		strcat(result, back);
	}

	return result;
}

// Real끼리의 더하기 연산
Real addReal(Real a, Real b) {
	int result_frac;
	int result_exp;

	int diff = abs(a.exp - b.exp);
	if (a.exp > b.exp) {
		result_frac = a.frac;
		for (int i = 0; i < diff; i++)
			result_frac *= 10;
		result_frac += b.frac;
		result_exp = b.exp;
	}
	else {
		result_frac = b.frac;
		for (int i = 0; i < diff; i++)
			result_frac *= 10;
		result_frac += a.frac;
		result_exp = a.exp;
	}

	Real result = { result_frac, result_exp };
	return result;
}

// Real의 반수 구하기 연산
Real negReal(Real r) {
	Real result = { -r.frac, r.exp };
	return result;
}

// Real끼리의 빼기 연산
Real subReal(Real a, Real b) {
	return addReal(a, negReal(b));
}

// Real끼리의 곱하기 연산
Real mulReal(Real a, Real b) {
	Real result = { a.frac * b.frac, a.exp + b.exp };
	return result;
}

// Real의 역수 구하기 연산
Real invReal(Real r) {
	if (r.frac == 0) {
		Real result = { 2147483647, 0 };
		return result;
	}

	char* frac = malloc(0);
	sprintf(frac, "%lf", (1.0 / r.frac));

	Real result = { atoi(frac + 2), -r.exp - 6 };
	return result;
}

// Real끼리의 나누기 연산
Real divReal(Real a, Real b) {
	if (b.frac == 0) {
		Real result = { 2147483647, 0 };
		return result;
	}
	return mulReal(a, invReal(b));
}