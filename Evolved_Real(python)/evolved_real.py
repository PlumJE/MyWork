class real(float):
    frac = 0
    exp = 0
    '''
    유효숫자 끝부분 위치와 소수점 위치를 구하고, 유효숫자 끝부분 < 소수점이면 지수부에 유효숫자_끝 - 소수점 - 1 을, 
    반대이면 지수부에 유효숫자_끝 - 소수점 을 저장한다. 다음으로 숫자에서 소수점을 없앤 뒤 뒤에 붙은 0들을 제거해
    가수부에 저장한다.
    '''
    def __init__(self, __value:float=0):
        super().__init__()
        if __value != 0.0:
            __value = str(__value)
            eofrac = -1
            point = -1
            for i in range(len(__value)):
                if __value[i] in '123456789':
                    eofrac = i
                elif __value[i] == '.':
                    point = i
            self.exp = int(point - eofrac)
            if eofrac < point:
                self.exp -= 1
            __value = "".join(__value.split('.')).rstrip('0')
            self.frac = int(__value)
    '''
    소수점이 유효숫자 오른쪽 너머에 있으면, 유효숫자 뒤에 지수개 만큼의 0을 붙이고 그 뒤에 .0을 붙인다.
    소수점이 유효숫자 사이에 있으면, 소수점을 유효숫자 사이의 해당하는 위치에 삽입한다
    소수점이 유효숫자 왼쪽 너머에 있으면, 유효숫자 앞에 (-지수 - 유효숫자갯수)개 만큼의 0을 붙이고 그 앞에 0.을 붙인다
    '''
    def __str__(self) -> str:
        if self.frac == 0:
            return "0.0"
        if self.exp >= 0:
            result = str(self.frac) + ('0' * self.exp) + '.0'
        else:
            result = str(self.frac)
            if -self.exp < len(str(self.frac)):
                result = result[:self.exp] + '.' + result[self.exp:]
            else:
                result = '0.' + ('0' * (-self.exp - len(result))) + str(self.frac)
        return result
    '''반수를 리턴하는 함수이다'''
    def __neg__(self):
        return real().insert(-self.frac, self.exp)
    '''더하기 연산자를 구현하는 함수이다'''
    def __add__(self, __value):
        if self.exp < __value.exp:
            frac = self.frac + __value.frac * 10 ** (__value.exp - self.exp)
            exp = self.exp
        else:
            frac = self.frac * 10 ** (self.exp - __value.exp) + __value.frac
            exp = __value.exp
        return real().insert(frac, exp)
    '''빼기 연산자를 구현하는 함수이다'''
    def __sub__(self, __value):
        return self + (-__value)
    '''곱하기 연산자를 구현하는 함수이다'''
    def __mul__(self, __value):
        frac = self.frac * __value.frac
        exp = self.exp + __value.exp
        return real().insert(frac, exp)
    '''나누기 연산자를 구현하는 함수이다'''
    def __truediv__(self, __value):
        frac = self.frac / __value.frac
        exp = self.exp - __value.exp
        while frac % 1 != 0:
            frac *= 10
            exp -= 1
        return real().insert(frac, exp)
    '''real에 가수와 지수를 직접 입력하는 함수이다'''
    def insert(self, frac, exp):
        self.frac = int(frac)
        self.exp = int(exp)
        return self
    '''가수와 지수를 보여주는 함수이다'''
    def show(self):
        print('(frac, exp) =', self.frac, self.exp)

a = real(1020.0)
b = real(0.0304)
c = real(-1020.0304)
d = real(-0.0)

print('a는', a, '\nb는', b, '\nc는', c, '\nd는', d)
print('(a+b)/c-d는', (a+b)/c-d, '\n')