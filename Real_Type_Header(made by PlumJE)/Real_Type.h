#pragma once
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdbool.h>
#include <math.h>

typedef struct real {
	long long frac : 52;// ���� �κ�
	int exp : 11;		// ���� �κ�
} Real;

// Real�� ������. �ð��� O(2n)
Real newReal(char* f) {
	// ��ȿ������ ������, ����, �Ҽ����� ��ġ�� ã�´�!
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

	// frac_start == frac_end == -1�̶�� 0.0�� ���� ���̹Ƿ�, 0.0�� �����Ѵ�
	if (frac_start == -1 && frac_end == -1) {
		Real result = { 0, 0 };
		return result;
	}

	// point == -1�̶�� �Ҽ����� ���ٴ� ������, f�� ������� �����Ѵ�
	if (point == -1) {
		Real result = { atoi(f), 0 };
		return result;
	}

	// ��ȿ���ڸ� ������ frac�� �����Ѵ�! �翬�� ��ȣ�� ����
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

	// ��ȿ���� �� ��ġ�� �Ҽ��� ��ġ�� ����� exp���� ���Ѵ�!
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

// Real�� ���� ���ڿ��� �Ǽ��� ����. �ð��� O(n)
char* realToString(Real r) {
	// r�� 0.0�� ������ �׳� "0.0"�� �����Ѵ�
	if (r.frac == 0 && r.exp == 0) {
		return "0.0";
	}

	// result�� frac�� ���� ���ڿ� �������� �ٿ��ִ´�
	char* result = malloc(0);
	sprintf(result, "%d", r.frac);
	
	// result�ڿ� "...000.0"�� ���� ��
	if (r.exp > -1) {
		for (int i = 0; i < r.exp; i++)
			strcat(result, "0");
		strcat(result, ".0");
	}
	// result���̿� "0.000..." �Ǵ� "."�� ������ ��
	else {
		int index = strlen(result) + r.exp;
		int zeros = -index;
		int is_neg = result[0] == '-' ? 1 : 0;	// ���� ��ȣ�� ������ 1, �ƴϸ� 0�̴�.
		char *middle = malloc(0);
		char *back = malloc(0);

		// index�� 0/1���� �۴ٸ� 0/1�� �����, result[index~]�κ��� back�� ����Ѵ�
		if (index < is_neg)
			index = is_neg;
		strcpy(back, result + index);

		// zeros�� �� middle="."�̰�, �� middle="0."+"0"*zeros�̴�
		if (zeros < -is_neg) {
			strcpy(middle, ".");
		}
		else {
			strcpy(middle, "0.");
			for (int i = 0; i < zeros; i++)
				strcat(middle, "0");
		}

		// result[index]�� middle�� �����Ѵ�
		result[index] = '\0';
		strcat(result, middle);
		strcat(result, back);
	}

	return result;
}

// Real������ ���ϱ� ����
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

// Real�� �ݼ� ���ϱ� ����
Real negReal(Real r) {
	Real result = { -r.frac, r.exp };
	return result;
}

// Real������ ���� ����
Real subReal(Real a, Real b) {
	return addReal(a, negReal(b));
}

// Real������ ���ϱ� ����
Real mulReal(Real a, Real b) {
	Real result = { a.frac * b.frac, a.exp + b.exp };
	return result;
}

// Real�� ���� ���ϱ� ����
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

// Real������ ������ ����
Real divReal(Real a, Real b) {
	if (b.frac == 0) {
		Real result = { 2147483647, 0 };
		return result;
	}
	return mulReal(a, invReal(b));
}